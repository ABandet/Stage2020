def getwatt(node, from_ts, to_ts):
    """Get power values from Grid'5000 Lyon Wattmetre (requires Execo)

    :param node: Node name

    :param from_ts: Time from which metric is collected, as an integer Unix timestamp

    :param from_ts: Time until which metric is collected, as an integer Unix timestamp

    :return: A list of (timestamp, value) tuples.
    """

    import datetime
    import requests
    import gzip
    import time
    from execo_g5k import get_host_attributes

    watt = []
    node_wattmetre = get_host_attributes(node)['sensors']['power']['via']['pdu']
    for i in range(len(node_wattmetre)):
        node = node_wattmetre[i]
        tmp_watt = []
        for ts in range(int(from_ts), int(to_ts)+3600, 3600):
            suffix = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H')
            if suffix != datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H'):
                suffix += ".gz"
            data=requests.get("http://wattmetre.lyon.grid5000.fr/data/"+node['uid']+"-log/power.csv."+suffix).content
            if suffix.endswith(".gz"):
                data = gzip.decompress(data)
            for l in str(data).split('\\n')[1:-1]:
                l = l.split(',')
                if l[3] == 'OK' and l[4+node['port']] != '':
                    ts, value = (float(l[2]), float(l[4+node['port']]))
                    if from_ts <= ts and ts <= to_ts:
                        tmp_watt.append((ts, value))
            if not suffix.endswith(".gz"):
                break
        watt.append(tmp_watt)

    if len(watt) > 1:
        for i in range(1, len(watt)):
            for j in range(min(len(watt[0]), len(watt[i]))):
                watt[0][j] = (watt[0][j][0], watt[0][j][1] + watt[i][j][1])

    return watt[0]


def extract_data(watt):
    try:
        time = []
        power = []
        for elem in watt:
            time.append(elem[0])
            power.append(elem[1])
        return time, power
    except Exception as e:
        print("Error, wrong watt format : {}".format(e))
        return None, None
