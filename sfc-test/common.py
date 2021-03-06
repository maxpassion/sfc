__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"

import requests
import json
import time

putheaders = {'content-type': 'application/json'}
getheaders = {'Accept': 'application/json'}
# ODL IP:port
ODLIP = "localhost:8181"
# Static URLs for testing
SF_URL = "http://" + ODLIP + "/restconf/config/service-function:service-functions/"
SFC_URL = "http://" + ODLIP + "/restconf/config/service-function-chain:service-function-chains/"
SFF_URL = "http://" + ODLIP + "/restconf/config/service-function-forwarder:service-function-forwarders/"
SFT_URL = "http://" + ODLIP + "/restconf/config/service-function-type:service-function-types/"
SFP_URL = "http://" + ODLIP + "/restconf/config/service-function-path:service-function-paths/"
SFF_OPER_URL = "http://" + ODLIP + "/restconf/operational/service-function-forwarder:service-function-forwarders-state/"
SF_OPER_URL = "http://" + ODLIP + "/restconf/operational/service-function:service-functions-state/"
RSP_URL = "http://" + ODLIP + "/restconf/operational/rendered-service-path:rendered-service-paths/"
SFP_ONE_URL = "http://" + ODLIP + "/restconf/config/service-function-path:service-function-paths/" \
                                  "service-function-path/{}/"
SF_ONE_URL = "http://" + ODLIP + "/restconf/config/service-function:service-functions/service-function/{}/"
IETF_ACL_URL = "http://" + ODLIP + "/restconf/config/ietf-acl:access-lists/"
RSP_RPC_URL = "http://" + ODLIP + "/restconf/operations/rendered-service-path:create-rendered-path"
SCF_URL = "http://" + ODLIP + "/restconf/config/service-function-classifier:service-function-classifiers/"

USERNAME = "admin"
PASSWORD = "admin"


def delete_configuration():
    s = requests.Session()
    print("Deleting previous config... \n")
    r = s.delete(SF_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Service Functions \n")
    else:
        print("=>Failure to delete SFs, response code = {} \n".format(r.status_code))
    r = s.delete(SFC_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Service Function Chains \n")
    else:
        print("=>Failure to delete SFCs, response code = {} \n".format(r.status_code))
    r = s.delete(SFF_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Service Function Forwarders \n")
    else:
        print("=>Failure to delete SFFs, response code = {} \n".format(r.status_code))
    r = s.delete(SFP_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Service Function Paths \n")
    else:
        print("=>Failure to delete SFPs, response code = {} \n".format(r.status_code))

    r = s.delete(IETF_ACL_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Access Lists \n")
    else:
        print("=>Failure to delete ACLs, response code = {} \n".format(r.status_code))
    r = s.delete(SCF_URL, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Deleted all Service Classifiers \n")
    else:
        print("=>Failure to delete Classifiers, response code = {} \n".format(r.status_code))


def put_and_check(url, json_req, json_resp):
    s = requests.Session()
    print("PUTing {} \n".format(url))
    r = s.put(url, data=json_req, headers=putheaders, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("Checking... \n")
        # Creation of SFPs is slow, need to pause here.
        time.sleep(2)
        r = s.get(url, stream=False, auth=(USERNAME, PASSWORD))
        if (r.status_code == 200) and (json.loads(r.text) == json.loads(json_resp)):
            print("=>Creation successfully \n")
        else:
            print("=>Creation did not pass check, error code: {}. If error code was 2XX it is "
                  "probably a false negative due to string compare \n".format(r.status_code))
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))


def check(url, json_resp, message):
    s = requests.Session()
    print(message, "\n")
    r = s.get(url, stream=False, auth=(USERNAME, PASSWORD))
    if (r.status_code == 200) and (json.loads(r.text) == json.loads(json_resp)):
        print("=>Check successful \n")
    else:
        print("=>Check not successful, error code: {}. If error code was 2XX it is "
              "probably a false negative due to string compare \n".format(r.status_code))


def post_rpc(url, json_input, ison_resp):
    s = requests.Session()
    print("POSTing RPC {} \n".format(url))
    r = s.post(url, data=json_input, headers=putheaders, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("Checking... \n")
        if (r.status_code == 200) and (json.loads(r.text) == json.loads(ison_resp)):
            print("=>RCP posted successfully \n")
        else:
            print("=>RPC unsuccessful, error code: {}. If error code was 2XX it is "
                  "probably a false negative due to string compare \n".format(r.status_code))
    else:
        print("=>Failure, status code: {} \n".format(r.status_code))


def delete_and_check(url, message):
    s = requests.Session()
    print(message, "\n")
    r = s.delete(url, stream=False, auth=(USERNAME, PASSWORD))
    if r.status_code == 200:
        print("=>Check successful \n")
    else:
        print("=>Check not successful, error code: {} \n".format(r.status_code))
