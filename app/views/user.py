from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.role import Role
from app.extensions import db
from app.views.auth import roles_required

view = Blueprint('user', __name__, url_prefix='/user')

@view.route('/')
@roles_required(Role.ADMIN)
def index():
    users = User.query.all()
    return render_template('/user/index.html', users=users)

@view.route('/create', methods=['GET', 'POST'])
@roles_required(Role.ADMIN)
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role = request.form.get('role')
        
        print(role)

        if User.query.filter_by(email=email).first():
            flash('A user with this email already exists.', 'danger')
            return redirect(url_for('user.create'))

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=Role[role] 
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('user.index'))

    return render_template('/user/create_or_edit.html', Role=Role)

@view.route('/edit/<int:id>', methods=['GET', 'POST'])
@roles_required(Role.ADMIN)
def edit(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.role = Role[request.form.get('role')]
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('user.index'))

    return render_template('/user/create_or_edit.html', user=user, Role=Role)

@view.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = current_user
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.role = Role[request.form.get('role')]
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('user.index'))

    return render_template('/user/create_or_edit.html', user=user, Role=Role)

@view.route('/delete/<int:id>', methods=['GET', 'POST'])
@roles_required(Role.ADMIN)
def delete(id):
    user = User.query.get_or_404(id)
    
    if User.query.count() < 2:
        flash('Create another user before deleting the last one.', 'warning')
        return redirect(url_for('user.index')) 

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        return redirect(url_for('user.index'))

    return render_template('/user/delete.html', user=user)
