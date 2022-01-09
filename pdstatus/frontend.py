# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

import os
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

# from .forms import SignupForm
from .nav import nav
from .pagerduty import top_level_services, fetch_impacting, fetch_impactors, fetch_incident, fetch_incident_log, fetch_business_service

frontend = Blueprint('frontend', __name__)

BASE_PD_URL=os.getenv('PDSTATUS_PD_URL')

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Status', '.index'),
    #View('Home', '.index'),
    #View('Forms Example', '.example_form'),
    #View('Debug-Info', 'debug.debug_root'),
    #Subgroup(
    #    'Docs',
    #    Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
    #    Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
    #    Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
    #    Separator(),
    #    Text('Bootstrap'),
    #    Link('Getting started', 'http://getbootstrap.com/getting-started/'),
    #    Link('CSS', 'http://getbootstrap.com/css/'),
    #    Link('Components', 'http://getbootstrap.com/components/'),
    #    Link('Javascript', 'http://getbootstrap.com/javascript/'),
    #    Link('Customize', 'http://getbootstrap.com/customize/'), ),
    #Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)),
    ))


@frontend.route('/service/<service_id>')
def impacting(service_id):
    svc = fetch_impacting(service_id)['services']
    biz_service = fetch_business_service(service_id)
    # Augment impacted services with incidents that are causing it
    for i, s in enumerate(svc):
        if s['status'] == 'impacted':
            impactors = fetch_impactors(s['id'])['impactors']
            for idx, impactor in enumerate(impactors):
                incident = fetch_incident(impactor['id'])['incident']
                incident_log = []
                log = fetch_incident_log(impactor['id'])['log_entries']
                for item in log:
                    if item['type'] == 'status_update_log_entry':
                        incident_log.append(item)
                impactors[idx]['info'] = incident
                impactors[idx]['log'] = incident_log
            svc[i]['impactors'] = impactors
    return render_template('impacting.html', services=svc, pd=BASE_PD_URL, biz_service=biz_service['business_service'])

@frontend.route('/')
def index():
    svc = top_level_services()['services']

    # Augment impacted services with incidents that are causing it
    for i, s in enumerate(svc):
        if s['status'] == 'impacted':
            impactors = fetch_impactors(s['id'])['impactors']
            for idx, impactor in enumerate(impactors):
                incident = fetch_incident(impactor['id'])['incident']
                incident_log = []
                log = fetch_incident_log(impactor['id'])['log_entries']
                for item in log:
                    if item['type'] == 'status_update_log_entry':
                        incident_log.append(item)
                impactors[idx]['info'] = incident
                impactors[idx]['log'] = incident_log
            svc[i]['impactors'] = impactors
    return render_template('index.html', services=svc, pd=BASE_PD_URL)