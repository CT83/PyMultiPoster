from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

posters = Blueprint('PostersBlueprint', __name__)


@posters.route('/poster')
def temporary():
    try:
        return render_template('temp.html')
    except TemplateNotFound:
        return "Failed to find template"
