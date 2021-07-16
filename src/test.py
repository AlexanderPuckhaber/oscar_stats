from get_capacities import get_capacities, generate_capacities_dict, generate_capacities_list
from refresh_capacities import refresh_capacities
from datetime import date
import urllib.request, json
import os

semester = '202108'

today = date.today()

prefix_url = f'https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in={semester}&crn_in='

with urllib.request.urlopen(f'https://gt-scheduler.github.io/crawler/{semester}.json') as url:
    course_json = json.loads(url.read().decode())
    #print(course_json)

    capacities_filename = f'{semester}_{today.strftime("%Y-%m-%d")}.json'

    capacities_json = refresh_capacities(course_json, capacities_filename, prefix_url)

    # save course_json and capacities_json to files in output

    with open(os.path.join('..', 'output', 'gt-scheduler-crawler-mirror', capacities_filename), 'w') as f:
        json.dump(course_json, f)

    with open(os.path.join('..', 'output', 'capacities_json-files', capacities_filename), 'w') as f:
        json.dump(capacities_json, f)

