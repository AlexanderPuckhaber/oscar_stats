from datetime import datetime
import calendar

table_labels = {'seats_capacity': 0, 'seats_actual': 1, 'seats_remaining': 2, \
                 'waitlist_capacity': 3, 'waitlist_actual': 4, 'waitlist_remaining': 5, 'timestamp': 6}

def get_table_labels():
    return table_labels

def generate_capacities_dict(capacities_list):
    capacities = {}
    for label in table_labels:
        capacities[label] = capacities_list[table_labels[label]]

    return capacities

def generate_capacities_list(capacities_dict):
    capacities_list = []
    for label in table_labels:
        capacities_list.insert(table_labels[label], capacities_dict[label])

    return capacities_list

def parse_capacities(html):
    html = str(html)
    table_entries = html.split("dddefault\">")[2:]

    capacities = {}

    for label in table_labels:
        if label is not 'timestamp':
            val = table_entries[table_labels[label]].split('<')[0]
            capacities[label] = int(val)

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())

    capacities['timestamp'] = unixtime
    #print(capacities)

    return capacities

def get_capacities(crn, http, prefix_url):
    try:
        r = http.request('GET', prefix_url + str(crn), timeout=20)

        if r.status == 200:
            # parse data

            try:
                capacities = parse_capacities(r.data)
            except:
                return r.status

            return capacities
        else:
            print('failure: ', crn, r.status)
            return r.status
    except:
        print('failure: ', crn, 'timeout')
        return None