from flask import Flask
from pyzabbix import ZabbixAPI
import configparser
import controller
    
config = configparser.ConfigParser()
config.read("config.ini")

server = config.get("zabbix", "server")
token = config.get("zabbix", "token")

z_api = ZabbixAPI(server)
z_api.login(api_token=token)

app = Flask(__name__)

@app.route('/')
def indexPage():
    return {"status": "ok"}

@app.route('/problems')
def problems():

    return controller.problems(z_api)

@app.route("/lastTrafegos/<host>/out/<top>")
def trafegosInterfacesOut(host, top):
    
    return controller.trafegosInterfaces(z_api, host, "out", top)

@app.route("/lastTrafegos/<host>/in/<top>")
def trafegosInterfacesIn(host, top):

    return controller.trafegosInterfaces(z_api, host, "in", top)

@app.route("/availability")
def availability():

    return controller.availability(z_api)

app.run(port=3333)