import datetime

def trafegosInterfaces(z_api, host, out_X_in, top):
    
    hostInfo = z_api.host.get(filter={"name": host})[0]
    hostId = hostInfo["hostid"]
    
    key = f"net.if.{out_X_in}["
    itens_trafegos = z_api.item.get(hostids=hostId, search={"key_": key}, output=["itemid", "name"])

    trafegos_history = {}
    top_interfaces = []

    for item in itens_trafegos:

        trafegos = z_api.history.get(output="extend", itemids=item["itemid"], sortfield="clock", sortorder="DESC", limit=1)

        if (len(trafegos) != 0):
            trafegos_history.update({item["itemid"]: int(trafegos[0]["value"])})

    for interface in sorted(trafegos_history, key=trafegos_history.get, reverse=True):
        top_interfaces.append(interface)

    if (len(top_interfaces) - 1 > int(top)):
        top_interfaces = top_interfaces[:int(top)]

    trafegos_history_top = {}
    for item in top_interfaces:
        nome_item = z_api.item.get(output=["name", "itemid"], itemids=item)[0]["name"]
        nome_item = nome_item.split()[1].replace(":", "")
        trafegos = z_api.history.get(output=["clock", "value"], itemids=item, sortfield="clock", sortorder="DESC", limit=5)
        trafegosNew = []

        for trafego in trafegos:
            date_trafego = datetime.datetime.fromtimestamp(int(trafego["clock"]))
            date_trafego = date_trafego.strftime("%d/%m/%Y %H:%M:%S")
            trafegosNew.append({"clock": date_trafego, "value": int(trafego["value"]), "interface": nome_item})


        trafegos_history_top.update({nome_item: trafegosNew})

    return trafegos_history_top

def problems(z_api):
    json_problems = []
    
    result_problems = z_api.problem.get(output='extend', filter={'value': 1})

    for problem in result_problems:
        host_problem = z_api.event.get(output='extend', selectHosts='extend', objectids=problem['objectid'], eventids=problem['eventid'])

        host = host_problem[0]['hosts'][0]['name']

        dt_problem = datetime.datetime.fromtimestamp(int(problem["clock"]))
        formated_data = dt_problem.strftime("%d/%m/%Y %H:%M:%S")
        json_problems.append({"host": host, "problem": problem["name"], "severity": problem["severity"], "timestamp": formated_data, "opdata": problem["opdata"]})

    return json_problems