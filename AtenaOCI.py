import oci
from flask import Flask
from flask_apscheduler import APScheduler

app = Flask('__name__')


sched = APScheduler()

def list_compart(parent_compart, identity_client):
    compartimentos = identity_client.list_compartments(parent_compart)

    # Exibe os compartimentos
    for compartimento in compartimentos.data:
        print(f"Nome do Compartimento: {compartimento.name}, ID: {compartimento.id}, Status: {compartimento.lifecycle_state}")
        list_compart(compartimento.id, identity_client)



def task():
    # Carrega a configuração do OCI
    #config = oci.config.from_file('C:\Users\Fábio Silva\Desktop\Projeto_Atena\instance\config.json')
    config_file_path = r'C:\Users\Fábio Silva\Desktop\Projeto_Atena\instance\config'
    config = oci.config.from_file(config_file_path)

    #config='{"TenancyOCID": "ocid1.tenancy.oc1..aaaaaaaaoi6b5sxlv4z773boczybqz3h2vspvvru42jysvizl77lky22ijaq", "UserOCID": "ocid1.user.oc1..aaaaaaaadxc6bvugfbn55ser2kngiompule7zdgmjb4chkljx37fdlevj2wa", "HomeRegion": "us-ashburn-1", "Fingerprint": "a8:6b:fb:bc:d3:7f:aa:9d:97:02:d1:3e:83:17:cd:78", "required_key": "-----BEGIN PRIVATE KEY-----MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDv6q4LWbOPCe8H1ptgkiJRHwtAc+krWK6dydHYQJxDu8dDHXD82EXOVrR6faWwOXTHd5cEb+zIpjQ3TJhyyVRhIf89VG2nR22rhiKuRjNBEpud8rtzmkOy7gNeF+TESmnWh2easwp9K1OQa8+sXVj5iAAfZHgLKQdH1OAde//+PezSEe2DSsq5dEjPKw2Ix/0fMw+jfXya3kyyuZQAeK4XsAgWdq7yxED1fTHrT7n0yQjTGOz4Wg9zKww/LOzIkUCAiaXogjT1oBG/6WSktQrk+i/Mip6ByqgG+nuVinXv7blambUr3xF6FbNxkcqcfe3+8A9xcyaPSCFFiNlKe3b3AgMBAAECggEAUOzeDCITuRnmsMQo4Ogp/ybziqgObHqbW8npqIISs54xVmgl5oOk+Day5eZf7xNSWr3yCKMgQYYectC5U26psaHgEHXcDuK/EW5LYHF5dGesahioNhRA5af3JtP0bGmVTbGatsnRrerhYwOap09NZc4EDJK9EzahqA8cEZX0AXOGqRe8BzpOtTBt2jSy/HIy9ft8/ur9ai7CUZ5KeNsQYoAtxQIMn1Zxvnhe6eRwjzcklVZYaKdgSZu44GwnqGQmjTOP8HLJs4WnNtYd3DRIzq/IUgihvOS+bz0WJXP/tvioizV2CZFu9VtdgZiBqDMbFXDtGCvQmj+Qv36o3ET5YQKBgQD8M9CENYnroOjlsfnkBLlwg+LdJTSe883TNGRRK7uUSnKjW5pQLHRV40scbGu2zSHWEccZZpGSe3PVyTArt/fthyxAwoT6XiAwVTesNduijWNhthyHcawN3n4aFbN73Y1vTr8AGlgQo0iYy5Uj085FHdO54d0Tt/2Frb/qFHvmSQKBgQDzh4G3gfpVwZWcwTZ5tad9M9L6EW1u87PY76dGCYFOut3T1+JB5lrWeGGYNswsngh6M6HZ4YGarAZlIP9HHXqOIpcfYw6BXl5VrhPkdWb060H0QmD7yN7NEQd4eA5RhFkFswgE6oe3Fbnqq6lHswWMqamuL5KjBK9wl/Qx/zNzPwKBgDtd6xCkFbI8r3YaXgt5vTkqIoYSEv/zvhigdZjR5Zbzq2ae0oVa4YuyNGUddIGUagmdJ7Pn/A5yNwM1F7zC0n68WgNohqr06zjVZoSILQpno+RFXRPZAzpEjISRZS2cKoXwEG/yw5YvCZDGI3ZKjnygl81iyIqyvd/w1YNBjSTZAoGBAJxaqvkD9ZLrmEAteOlJrQBgrpspZ0ZuJ1EoBRCdd6zxowypNbYzzKyYW6ibvhkDWdQDpG28MDb7LZvuRJgHIDFzme1n7t82lICUJGdwzSqAhTbrC1N80zd8MHyzMBY8T9+t438siPgOdfBqSGQlV3HJWIziNFZ/4pf6p6kV/ZWHAoGBAMFGv4sKjFQXmTaIE0nwqqEUQTXaRk+35XG8v4DKZADA0i0nxzZl+P1ynf93uG8xpK1HYcaLlDgc3hSwJyOHLZqddwzbEm6B7xGnVNOQXwCOjuupuST965VXKRMwVxCQHZ2FOfP1c+WPic4eeYm1dSGoj0Bw/3ZRpAtrh7ZlhFtk-----END PRIVATE KEY-----"}'

    print(config)

    # Cria um cliente de identidade
    identity_client = oci.identity.IdentityClient(config)

    # Lista as regiões
    regions = identity_client.list_regions()

    # Exibe as regiões
    for region in regions.data:
        print(f"Nome da Região: {region.name}")
    
    list_compart('ocid1.compartment.oc1..aaaaaaaas5ehgfqzt2cx6kzviamox2sqklgdxgc5asa6x2c7fymix2dqekwq', identity_client)


    #compartimentos = identity_client.list_compartments('ocid1.compartment.oc1..aaaaaaaacdrgb7hgy2re7ymyept4wgh43dwzqrlprbb73atjz5x7s2duzo3a', compartment_id_in_subtree=True)
    #compartimentos = identity_client.list_compartments('ocid1.compartment.oc1..aaaaaaaas5ehgfqzt2cx6kzviamox2sqklgdxgc5asa6x2c7fymix2dqekwq')

    # Exibe os compartimentos
    # for compartimento in compartimentos.data:
    #     print(f"Nome do Compartimento: {compartimento.name}, ID: {compartimento.id}, Status: {compartimento.lifecycle_state}")
    #     subs = identity_client.list_compartments(compartimento.id)
    #     for sub in subs.data:
    #         print(f"    Nome do Compartimento: {sub.name}, ID: {sub.id}, Status: {sub.lifecycle_state}")




if __name__ == '__main__':

    print('teste')

    sched.add_job(id='test task', func=task, trigger='interval', seconds=5)
    sched.start()
    app.run(debug = True, use_reloader = False)