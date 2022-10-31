from flask import jsonify, render_template
from app.errors import bp
from app.db import db
from werkzeug.exceptions import HTTPException

@bp.app_errorhandler(400)
def internal_error(error):
    return render_template('errors.html', error_code=400, error_type="Bad Request", error_description="Unexpected error. Your browser sent an invalid request. That's all we know."), 400

@bp.app_errorhandler(401)
def internal_error(error):
    return render_template('errors.html', error_code=401, error_type="Unauthorized", error_description="You were unauthorized to see this page as it is not publicly available."), 401

@bp.app_errorhandler(403)
def internal_error(error):
    return render_template('errors.html', error_code=403, error_type="Forbidden", error_description="The page you were trying to reach has restricted access. Contact website administrator if you think it's a mistake."), 403

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors.html', error_code=404, error_type="Page Not Found", error_description="The page you are looking for was moved, removed, renamed or might never existed."), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors.html', error_code=500, error_type="Internal Server Error", error_description="Sorry, there were some technical issues while processing your request."), 500

@bp.app_errorhandler(Exception)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
        type = error.__class__.__name__
        description = error.description
    return render_template('errors.html', error_code=code, error_type=type, error_description=description), code