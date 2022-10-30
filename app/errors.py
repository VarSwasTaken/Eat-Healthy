from flask import jsonify, render_template
from app import app
from app.db import db
from werkzeug.exceptions import HTTPException

@app.errorhandler(400)
def internal_error(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def internal_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def internal_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
        type = error.__class__.__name__
        description = error.description
    return render_template('errors/default-error.html', error_code=code, error_type=type, error_description=description), code