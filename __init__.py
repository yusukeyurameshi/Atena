import os
from Atena.dashboard import readConfigFile

from flask import Flask, current_app

from flask_apscheduler import APScheduler
from Atena.AtenaOCI import atualizaSubscribedRegions

sched = APScheduler()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    ParentCompartment = None
    compIntervalScan = None
    serviceIntervalScan = None

    if os.path.exists(os.path.join(app.instance_path, 'interval.ini')):
        valuestr = readConfigFile(os.path.join(app.instance_path, 'interval.ini'))

        for item in valuestr:
            if item[0] == 'parentcompartment':
                ParentCompartment = item[1]
            elif item[0] == 'compintervalscan':
                compIntervalScan = item[1]
            elif item[0] == 'serviceintervalscan':
                serviceIntervalScan = item[1]

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CONFIG=os.path.join(app.instance_path, 'config'),
        CONFIGINTERVAL=os.path.join(app.instance_path, 'interval.ini'),
        PRIVATEKEY=os.path.join(app.instance_path,'privatekey.pem'),
        PARENTCOMPARTMENT = ParentCompartment,
        COMPINTERVALSCAN = compIntervalScan,
        SERVICEINTERVALSCAN = serviceIntervalScan
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    with app.app_context():

        if not os.path.exists(current_app.config['DATABASE']):
            # ensure the instance folder exists
            try:
                os.makedirs(app.instance_path)
            except OSError:
                pass

            db.init_db()

    # sched.add_job(id='Region Scan', func=AtenaOCI.atualizaSubscribedRegions, args = [app.config['CONFIG'], app], trigger='cron', day_of_week='0-6', hour=0)
    # sched.add_job(id='Compartment Scan', func=AtenaOCI.atualizaCompartments, args = [app.config['PARENTCOMPARTMENT'], app.config['CONFIG'], app], trigger='interval', seconds=int(compIntervalScan))
    # sched.start()
    AtenaOCI.atualizaSubscribedRegions(app.config['CONFIG'], app)
    AtenaOCI.atualizaCompartments(app.config['PARENTCOMPARTMENT'], app.config['CONFIG'], app, 0)


    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    return app