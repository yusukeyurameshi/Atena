import oci
from flask import (
    current_app, g, Flask
)
from Atena.db import get_db, close_db

def insereCompartment(id, name, status, app):
    with app.app_context():
        db = get_db()

        db.execute('''insert into compartments (ocid, name, status) values (?,?,?)''',[id, name, status])

        db.commit()
        close_db()

def fetchCompartments(app):
    with app.app_context():
        db = get_db()

        clist = db.execute("select OCID from COMPARTMENTS").fetchall()

        close_db()
        
        return clist

def atualizaCompartments(parent_compart, config_file_path, app):
    with app.app_context():

        # Carrega a configuração do OCI
        config = oci.config.from_file(config_file_path)

        # Cria um cliente de identidade
        identity_client = oci.identity.IdentityClient(config)
        compartimentos = identity_client.list_compartments(parent_compart)

        # clist = db.execute("select OCID from COMPARTMENTS").fetchall()
        clist = fetchCompartments(app)
        comp_list = []

        for line in clist:
            comp_list.append(line[0])
        
        # Exibe os compartimentos
        for compartimento in compartimentos.data:
            if compartimento.id not in comp_list:
                # db.execute('''insert into compartments (ocid, name, status) values (?,?,?)''',[compartimento.id, compartimento.name, compartimento.lifecycle_state])
                insereCompartment(compartimento.id, compartimento.name, compartimento.lifecycle_state, app)

            atualizaCompartments(compartimento.id, config_file_path, app)

def atualizaFSDR(config_file_path, parent_compart):

    # Carrega a configuração do OCI
    config = oci.config.from_file(config_file_path)

    dr = oci.disaster_recovery.DisasterRecoveryClient(config)
    identity_client = oci.identity.IdentityClient(config)

    compartimentos = identity_client.list_compartments(parent_compart)

    for compartimento in compartimentos.data:
        fsdrs = dr.list_dr_protection_groups(compartimento.id)
        for fsdr in fsdrs:
            print(fsdr)

        





def atualizaSubscribedRegions(config_file_path, app):

    # current_app.app_context()
    # app = Flask(__name__)
    with app.app_context():
        db = get_db()

        # Carrega a configuração do OCI
        config = oci.config.from_file(config_file_path)

        # Cria um cliente de identidade
        identity_client = oci.identity.IdentityClient(config)
        
        # Lista as regiões
        regions = identity_client.list_region_subscriptions(config['tenancy'])

        cur = db.cursor()
        cur.execute("select region from regions")
        rlist = cur.fetchall()
        region_list = []

        for line in rlist:
            region_list.append(line[0])
        
        # Exibe as regiões
        for region in regions.data:
            if region.region_name not in region_list:
                print(region.region_name)
                db.execute('''insert into regions (region) values (?)''', [region.region_name])
        
        db.commit()
        close_db()
    
    # list_compart('ocid1.compartment.oc1..aaaaaaaas5ehgfqzt2cx6kzviamox2sqklgdxgc5asa6x2c7fymix2dqekwq', identity_client)


