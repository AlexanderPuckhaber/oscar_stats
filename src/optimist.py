import json

capacities_json = '202102_jan22_capacities.json'

with open(capacities_json) as f:
    capacities_data = json.load(f)

    total = 0
    total_f = 0

    for caps in capacities_data:
        print(caps)
        print(capacities_data[caps])

        capacity = float(capacities_data[caps][0])
        taken = float(capacities_data[caps][1])

        if taken/(capacity+0.0001) > 0.75:
            total_f = total_f + 1

        total = total + 1

    print('total:', total, 'total_f:', total_f, 'frac:', total_f/total)