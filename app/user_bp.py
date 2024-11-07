from flask import Blueprint, request, redirect, url_for, render_template, flash
from .models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        team_color = request.form['team_color']
        
        # Skapa en ny användare
        new_user = User(name=name, team_color=team_color)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Användaren har registrerats!')
        return redirect(url_for('user.list_users'))
    
    return render_template('register.html')

@user_bp.route('/set_agent/<int:user_id>', methods=['POST'])
def set_agent(user_id):
    """Sätt en användare som agent och se till att ingen annan är agent."""
    # Återställ alla användares agentstatus
    User.query.update({User.is_agent: False})
    db.session.commit()
    
    # Sätt den valda användaren som agent
    user = User.query.get(user_id)
    if user:
        user.is_agent = True
        db.session.commit()
        flash(f'{user.name} är nu agent.')
    else:
        flash('Användare hittades inte.')
    
    return redirect(url_for('user.list_users'))

@user_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)
