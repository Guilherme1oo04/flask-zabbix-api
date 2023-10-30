def trafegosInterfaces(z_api, host, out_X_in, top):
    
    hostInfo = z_api.host.get(filter={"name": host})[0]
    hostId = hostInfo["hostid"]
    
    key = f"net.if.{out_X_in}["
    itens_trafegos = z_api.item.get(hostids=hostId, search={"key_": key}, output=["itemid", "name"])

    trafegos_history = {}
    top_interfaces = []

    for item in itens_trafegos:

        trafegos = z_api.history.get(output="extend", itemids=item["itemid"], sortfield="clock", sortorder="DESC", limit=10)

        if (len(trafegos) != 0):
            trafegos_history.update({item["itemid"]: int(trafegos[0]["value"])})

    for interface in sorted(trafegos_history, key=trafegos_history.get, reverse=True):
        top_interfaces.append(interface)

    if (len(top_interfaces) - 1 > int(top)):
        top_interfaces = top_interfaces[:int(top)]

    trafegos_history_top = {}
    for item in top_interfaces:
        nome_item = z_api.item.get(output=["name", "itemid"], itemids=item)[0]["name"]
        trafegos = z_api.history.get(output="extend", itemids=item, sortfield="clock", sortorder="DESC", limit=10)

        trafegos_history_top.update({nome_item: trafegos})

    return trafegos_history_top