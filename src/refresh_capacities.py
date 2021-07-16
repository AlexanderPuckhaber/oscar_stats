import json
import urllib3
from get_capacities import get_capacities, generate_capacities_dict, generate_capacities_list
import time

urllib3_http = urllib3.PoolManager()

def request_wrapper(crn, urllib3_http, prefix_url):
    response = get_capacities(crn, urllib3_http, prefix_url)

    if response is None:
        #print('response for crn', crn, 'timed out')
        return 'timed out'
    elif type(response) is dict:
        return response
    else:
        #print('response for crn', crn, 'parse error with response', response)
        return 'parse error'



def refresh_capacities(courses_json, capacities_json, prefix_url):
    data = courses_json

    capacities_map = {}

    allDone = False

    num_tries = 10

    try:
        while not allDone and num_tries > 0:
            allDone = True
            num_tries = num_tries - 1

            for course in data['courses']:
                #print(course)
                #print(data['courses'][course])
                for course_deets in data['courses'][course]:
                    #print("COURSE DEETS")
                    #print(course_deets)
                    if type(course_deets) is dict:
                        for entry in course_deets:
                            crn = course_deets[entry][0]

                            if crn not in capacities_map.keys():
                                allDone = False
                                #time.sleep(0.1)

                                try:
                                    resp = request_wrapper(crn, urllib3_http, prefix_url)
                                except:
                                    resp = None
                                    #print("resp = None crn:", crn)

                                if resp == 'parse error':
                                    pass
                                elif resp == 'timed out':
                                    time.sleep(6)
                                else:
                                    capacities = generate_capacities_list(resp)
                                    capacities_map[crn] = capacities
                                    print(course, entry, "crn:", crn, capacities)

                            else:
                                pass
                                #print(course, entry, 'crn:', crn, 'skipped', capacities_map[crn])

        return capacities_map
    except:
        print("error")
        return None
