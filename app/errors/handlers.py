from flask import jsonify, render_template
from app.errors import bp
from app.db import db
from werkzeug.exceptions import HTTPException

@bp.app_errorhandler(400)
def internal_error(error):
    return render_template('errors/400.html'), 400

@bp.app_errorhandler(401)
def internal_error(error):
    return render_template('errors/401.html'), 401

@bp.app_errorhandler(403)
def internal_error(error):
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(Exception)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
        type = error.__class__.__name__
        description = error.description
    return render_template('errors/default-error.html', error_code=code, error_type=type, error_description=description), code