from flask import Blueprint, flash, redirect, url_for, render_template, request, jsonify, abort
from datetime import datetime
from acsystem import db
from acsystem.models import Sales, SalesItem, Customer, Product, Company
from acsystem.transactions.forms import SalesForm
from flask_login import login_required, current_user

transactions = Blueprint('transactions',__name__)

@transactions.route('/invoice')
@login_required
def invoice():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))
    page = request.args.get('page', 1, type=int)
    sales = Sales.query.filter_by(company_id = current_user.activecompany).order_by(Sales.date.desc()).paginate(page=page, per_page=10)
    return render_template('transactiontemplate/invoice.html', title='Invoice', sales = sales)

@transactions.route('/invoice/createinvoice', methods=['GET','POST'])
@login_required
def createinvoice():
    if current_user.activecompany == 0:
        flash(f"No Company is Activated! ","warning")
        return redirect(url_for('company.companies'))

    form1 = SalesForm()
    for item in form1.items:
        item.product.choices += [(str(prod.id),prod.name) for prod in Product.query.filter_by(company_id = current_user.activecompany).all()]
    if form1.validate_on_submit():
        c = Company.query.get_or_404(current_user.activecompany)
        customer = Customer.query.filter(Customer.company_id == current_user.activecompany).filter(Customer.name == form1.customer.data).first()
        if not customer:
            print("customer not found")
            fullname = form1.customer.data
            first_name = " ".join(fullname.split(' ')[:1])
            last_name = " ".join(fullname.split(' ')[1:])
            customer = Customer(name = fullname, first= first_name, last = last_name, phoneno = form1.cust_phone.data
                    , mailingname = first_name, address = form1.cust_address.data, country = form1.cust_country.data, state = form1.cust_state.data
                    ,  email = "", gstno = "", description = "", company_id = current_user.activecompany)
            db.session.add(customer)
            db.session.commit()
            flash(f"New Customer {fullname} Created Succefully!","info")
        else:
            customer.address = form1.cust_address.data
            customer.state = form1.cust_state.data
            customer.country = form1.cust_country.data
            customer.phone = form1.cust_phone.data
        sale = Sales(customer = customer.id, date = form1.date.data, 
                    invoiceno = form1.invoiceno.data, totalamount = form1.totalamount.data,
                    description = form1.description.data, company_id = current_user.activecompany)
        db.session.add(sale)
        c.invoiceno = int(form1.invoiceno.data)
        if customer:
            customer.currentbalance += form1.totalamount.data
        db.session.commit()
        for entry in form1.items.entries:
            saleitem = SalesItem(product = entry.form.product.data, 
                                quantity = entry.form.quantity.data,
                                rate = entry.form.rate.data, undersales=sale.id)
            p = Product.query.get_or_404(entry.form.product.data)
            p.quantity -= entry.form.quantity.data
            db.session.add(saleitem)
            db.session.commit()
            print(saleitem)    
        print(sale)
        flash(f"Invoice Generated","success")
        return redirect(url_for('transactions.invoice'))
    if form1.errors:
        print("rows are " + str(form1.rows.data))
        form1.items.min_entries= form1.rows.data
    if request.method == 'GET':
        form1.date.data = datetime.now()
        lastentry = Company.query.get_or_404(current_user.activecompany)
        form1.invoiceno.data = lastentry.invoiceno+1
    return render_template('transactiontemplate/addinvoice.html', title='Create Invoice', form1=form1)

@transactions.route('/invoice/loadcustomer')
@login_required
def loadcustomer():
    custarr = []
    for c in Customer.query.filter_by(company_id = current_user.activecompany).all():
        cust = {}
        cust["id"] = c.id
        cust["name"] = c.name
        custarr.append(cust)
    return jsonify({'customer': custarr})

@transactions.route('/invoice/loadproductdetail/<product_id>')
@login_required
def loadproductdetail(product_id):
    product = Product.query.get_or_404(product_id)
    if(product.company_id != current_user.activecompany):
        abort(403);
    productobj = {
        "quantity":product.quantity,
        "rate" : product.salesprice,
        "unit": product.underunit.symbol
    }
    return jsonify({'product':productobj})

@transactions.route('/invoice/loadcustomerdetail/<customer_name>')
@login_required
def loadcustomerdetail(customer_name):
    # customer = Customer.query.get_or_404(customer_id)
    customer = Customer.query.filter_by(name=customer_name).first()
    if customer:
        if(customer.company_id != current_user.activecompany):
            abort(403);
        customerobj = {
            "name":customer.name,
            "mailingname" : customer.mailingname,
            "address": customer.address,
            "country": customer.country,
            "state": customer.state,
            "pin": customer.pin,
            "email": customer.email,
            "phone": customer.phoneno,
            "gstno": customer.gstno,
            "currentbalance": customer.currentbalance
        }
        return jsonify({'customer':customerobj})
    return jsonify({'customer':"nothing"})


@transactions.route("/invoice/<int:invoice_id>")
@login_required
def invoice_detail(invoice_id):
    invoice = Sales.query.get_or_404(invoice_id)
    if invoice.company_id != current_user.activecompany:
        abort(403)
    return render_template('transactiontemplate/invoicedetail.html', title=invoice.customer, invoice = invoice)

@transactions.route("/invoice/<int:invoice_id>/download")
@login_required
def invoice_download(invoice_id):
    invoice = Sales.query.get_or_404(invoice_id)
    if invoice.company_id != current_user.activecompany:
        abort(403)
    return render_template('transactiontemplate/invoicepdfdownload.html',title = invoice.invoiceno, invoice = invoice)

@transactions.route("/invoice/<int:invoice_id>/delete", methods=['POST','GET'])
@login_required
def delete_invoice(invoice_id):
    invoice = Sales.query.get_or_404(invoice_id)
    if invoice.company_id != current_user.activecompany:
        abort(403)
    db.session.delete(invoice)
    db.session.commit()
    flash(f"Inovice {invoice.invoiceno} deleted Successfully","success")
    return redirect(url_for('transactions.invoice'))
