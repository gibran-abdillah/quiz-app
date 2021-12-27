from app.dashboard import dashboard_blueprint as dashboard 
from flask import render_template, redirect
from app.modules.decorators import admin_required


@dashboard.route('/manage-users')
@admin_required
def manage_users():
    return render_template('dashboard/admin/manage-users.html')


