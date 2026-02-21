from pay_app import app, db
from flask import render_template, redirect, url_for, flash, request
from pay_app.models import Item, Bill, User
from pay_app.forms import SignupForm, SigninForm
from flask_login import login_user, logout_user, login_required, UserMixin, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/pay')
@login_required
def pay_page():
    bills = Bill.query.all()
    return render_template('pay.html', bills=bills)

@app.route('/shop')
@login_required
def shop_page():    
    items = Item.query.all()
    return render_template('shop.html', items=items)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully! Please log in.', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are validation errors
        for err_msg in form.errors.values():
            flash(f"Error creating account: {err_msg}", category='danger')
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    form = SigninForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Successfully logged in as {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
    return render_template('signin.html', form=form)

@app.route('/signout')
@login_required
def sign_out():
    logout_user()
    flash('You have been signed out.', category='info')
    return redirect(url_for('home_page'))

#Admin routes for admin role to manage bills and items can be added here in the future
@app.route('/add_items)', methods=['GET', 'POST'])
@login_required
def add_items():
    if current_user.role == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            description = request.form.get('description')
            new_item = Item(name=name, price=price, description=description, owner_id=None)
            db.session.add(new_item)
            db.session.commit()
            flash(f'Item "{name}" created successfully!', category='success')
            return redirect(url_for('shop_page'))
        return render_template('add_items.html')
    else:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('home_page'))

@app.route('/delete_items/<int:bill_id>', methods=['POST'])
@login_required
def delete_items(bill_id):
    if current_user.role == 'admin':
        item_to_delete = Item.query.get_or_404(bill_id)
        db.session.delete(item_to_delete)
        db.session.commit()
        flash(f'Item "{item_to_delete.name}" deleted successfully!', category='success')
        return redirect(url_for('shop_page'))
    else:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('home_page'))
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    if current_user.role == 'admin':
        item = Item.query.get_or_404(id)
        if request.method == 'POST':
            item.name = request.form.get('name')
            item.price = request.form.get('price')
            item.description = request.form.get('description')
            db.session.commit()
            flash(f'Item "{item.name}" updated successfully!', category='success')
            return redirect(url_for('shop_page'))
        return render_template('update_item.html', item=item)
    else:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('home_page'))

@app.route('/add_bills', methods=['GET', 'POST'])
@login_required 
def add_bills():
    if current_user.role == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            month = request.form.get('month')
            amount = request.form.get('amount')
            due_date = request.form.get('due_date')
            new_bill = Bill(name=name, month=month, amount=amount, due_date=due_date, owner_id=current_user.id)
            db.session.add(new_bill)
            db.session.commit()
            flash(f'Bill "{name}" created successfully!', category='success')
            return redirect(url_for('pay_page'))
        return render_template('add_bills.html')
    else:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('home_page'))
    

            
    