from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import os
from werkzeug.exceptions import abort

#from flaskr.auth import login_required
from Atena.db import get_db, close_db
from Atena.configFile import writeConfigFile, readConfigFile

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    if not os.path.exists(current_app.config['CONFIG']):
        return redirect(url_for('dashboard.config'))

    db = get_db()
    posts = db.execute(
        'SELECT id_menu, name, url'
        ' FROM menu'
    ).fetchall()

    regions = db.execute('select id_region, region from regions order by 2').fetchall()
    # print(regions)
    compartments = db.execute('select ocid, name, status from compartments order by 2').fetchall()
    # print(compartments)

    return render_template('dashboard/index.html',posts=[posts, regions, compartments])#, compartments=compartments)

@bp.route('/config', methods=('GET', 'POST'))
def config():
    if request.method == 'POST':
        if request.form['TAB'] == 'OCIAccess':
            TenancyOCID = request.form['TenancyOCID']
            UserOCID = request.form['UserOCID']
            HomeRegion = request.form['HomeRegion']
            Fingerprint = request.form['Fingerprint']
            PEMKey = request.form['PEMKey']

            dictionary={'user': UserOCID, 'fingerprint': Fingerprint, 'key_file': current_app.config['PRIVATEKEY'], 'tenancy': TenancyOCID, 'region': HomeRegion}

            writeConfigFile(current_app.config['CONFIG'], dictionary)


            with open(current_app.config['PRIVATEKEY'], 'w') as f:
                f.write(PEMKey)

            return redirect(url_for('dashboard.index'))
        elif request.form['ParentCompartment'] !=None:
            ParentCompartment = request.form['ParentCompartment']
            compIntervalScan = request.form['compIntervalScan']
            serviceIntervalScan = request.form['serviceIntervalScan']
            error = None

            dictionary={'ParentCompartment': ParentCompartment, 'compIntervalScan': compIntervalScan, 'serviceIntervalScan': serviceIntervalScan}

            writeConfigFile(current_app.config['CONFIGINTERVAL'], dictionary)

            # with open(current_app.config['CONFIGINTERVAL'], 'w') as f:
            #     for line in dictionary:
            #         f.write(line)
            #         f.write('\n')


            return redirect(url_for('dashboard.index'))
    else:
        valuestr = readConfigFile(current_app.config['CONFIGINTERVAL'])

        ParentCompartment = None
        compIntervalScan = None
        serviceIntervalScan = None
        UserOCID = None
        Fingerprint = None
        TenancyOCID = None
        HomeRegion = None

        for item in valuestr:
            if item[0] == 'parentcompartment':
                ParentCompartment = item[1]
            elif item[0] == 'compintervalscan':
                compIntervalScan = item[1]
            elif item[0] == 'serviceintervalscan':
                serviceIntervalScan = item[1]

        valuestr = readConfigFile(current_app.config['CONFIG'])

        for item in valuestr:
            if item[0] == 'user':
                UserOCID = item[1]
            elif item[0] == 'fingerprint':
                Fingerprint = item[1]
            elif item[0] == 'tenancy':
                TenancyOCID = item[1]
            elif item[0] == 'region':
                HomeRegion = item[1]

        if ParentCompartment is None and UserOCID is None:
            return render_template('config.html')

        elif UserOCID is None:

            return render_template('config.html', 
                                serviceIntervalScan = serviceIntervalScan, 
                                compIntervalScan = compIntervalScan, 
                                ParentCompartment = ParentCompartment)

        elif ParentCompartment is None:
            return render_template('config.html', 
                                UserOCID = UserOCID,
                                HomeRegion = HomeRegion,
                                Fingerprint = Fingerprint,
                                TenancyOCID = TenancyOCID)
        
        else:
            return render_template('config.html', 
                        serviceIntervalScan = serviceIntervalScan, 
                        compIntervalScan = compIntervalScan, 
                        ParentCompartment = ParentCompartment,
                        UserOCID = UserOCID,
                        HomeRegion = HomeRegion,
                        Fingerprint = Fingerprint,
                        TenancyOCID = TenancyOCID)
