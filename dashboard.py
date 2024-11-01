from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import os
import json
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from Atena.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    if not os.path.exists(current_app.config['CONFIG']):
        return redirect(url_for('dashboard.config'))
        #return render_template('config.html')


    db = get_db()
    posts = db.execute(
        'SELECT id, name, url'
        ' FROM menu'
    ).fetchall()
    return render_template('dashboard/index.html', posts=posts)

@bp.route('/config', methods=('GET', 'POST'))
def config():
    if request.method == 'POST':
        TenancyOCID = request.form['TenancyOCID']
        UserOCID = request.form['UserOCID']
        HomeRegion = request.form['HomeRegion']
        Fingerprint = request.form['Fingerprint']
        PEMKey = request.form['PEMKey']
        error = None

        dictionary='{"TenancyOCID": "'+TenancyOCID+'", "UserOCID": "'+UserOCID+'", "HomeRegion": "'+HomeRegion+'", "Fingerprint": "'+Fingerprint+'", "PEMKey": '+PEMKey+'"}'
        print(dictionary)
        json_object = json.loads(dictionary)
        with open(current_app.config['CONFIG']+'config.json', 'w') as f:
            json.dump(json_object, f)

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tenancy ( user_id, tenancy_ocid, user_ocid, home_region, fingerprint, pem_key)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (1, TenancyOCID, UserOCID, HomeRegion, Fingerprint, PEMKey)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('config.html')
