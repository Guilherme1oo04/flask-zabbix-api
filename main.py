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

@app.route('/problems')
def problems():

    json_problems = []
    
    result_problems = z_api.problem.get(output='extend', filter={'value': 1})

    for problem in result_problems:
        json_problems.append({"problem": problem["name"], "timestamp": problem["clock"], "opdata": problem["opdata"]})

    return json_problems

@app.route("/lastTrafegos/<host>/out/<top>")
def trafegosInterfacesOut(host, top):
    
    return controller.trafegosInterfaces(z_api, host, "out", top)

@app.route("/lastTrafegos/<host>/in/<top>")
def trafegosInterfacesIn(host, top):

    return controller.trafegosInterfaces(z_api, host, "in", top)

app.run(port=3333)