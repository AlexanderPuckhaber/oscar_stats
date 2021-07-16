import urllib3
import requests

all_the_crns = []


def parse():
    pass
    pass


for crn in all_the_crns:
    resp = requests.get('https://oscar.gatech.edu/pls/bprod/'
                        + 'bwckschd.p_disp_detail_sched?term_in=202102&crn_in='
                        + crn)
    parse(resp)
