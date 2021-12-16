
import requests
import sys
import json


# Next lines turn off messages about missing SSL certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from fmc_groups import create_full_group

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FMC(object):
    """
    Initialisation for the class dealing with all calls to the FMC API
    """

    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json'}
        self.api_base_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f"
        self.json_resp = {}

    def authentication(self):
        """
        Passes user and password to get a token for requests
        """

        api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
        auth_url = self.server + api_auth_path

        try:
            r = requests.post(auth_url, headers=self.headers,
                              auth=requests.auth.HTTPBasicAuth(self.username, self.password), verify=False)
            auth_headers = r.headers
            auth_token = auth_headers.get('X-auth-access-token', default=None)
            if auth_token == None:
                print("auth_token not found. Exiting...")
                sys.exit()
        except Exception as err:
            print("Error in generating auth token --> " + str(err))
            sys.exit()

        self.headers['X-auth-access-token'] = auth_token

        return self.headers

    def GetApiCall(self, url):
        """
        Generic GET request to the FMC API with exception handling
        """
        r = requests.get(url, headers=self.headers, verify=False)
        try:
            status_code = r.status_code
            resp = r.text
            if (status_code == 200):
                self.json_resp = json.loads(resp)
                return self.json_resp
                print("WAHOO")
            else:
                r.raise_for_status()
                print("Error occurred in GET --> " + resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> " + str(err))
        finally:
            if r:
                r.close()

    def PostApiCall(self, url, post_data):
        """
        Generic POST request to the FMC API with exception handling
        """
        r = requests.post(url, data=json.dumps(post_data), headers=self.headers, verify=False)
        try:
            status_code = r.status_code
            resp = r.text
            if status_code == 201 or status_code == 202:
                # print ("The rule has now been implemented. The time is %s" % time.ctime())
                # print "This rule will be in place for %i seconds" % iLength
                # print "It worked"
                self.json_resp = json.loads(resp)
                return self.json_resp

            else:
                r.raise_for_status()
                print("Error occurred in POST --> " + resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> " + str(err))
        finally:
            if r:
                r.close()

    def PutApiCall(self, url, put_data):
        """
        Generic PUT request to the FMC API with exception handling
        """

        try:
            r = requests.put(url, data=json.dumps(put_data), headers=self.headers, verify=False)
            status_code = r.status_code
            resp = r.text
            if (status_code == 200):
                self.json_resp = json.loads(resp)
                print("Done")
            else:
                r.raise_for_status()
                print("Status code:-->" + status_code)
                print("Error occurred in PUT --> " + resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> " + str(err))

    # finally:
    #   if r: r.close()

    def DeleteApiCall(self, url):
        """
        Generic DELETE request to the FMC API with exception handling
        """

        try:
            r = requests.delete(url, headers=self.headers, verify=False)
            status_code = r.status_code
            resp = r.text
            if (status_code == 200):
                # print "The rule has been deleted."
                self.json_resp = json.loads(resp)
                return True
            else:
                r.raise_for_status()
                print("Error occurred in DELETE --> " + resp)
        except requests.exceptions.HTTPError as err:
            print("Error in connection --> " + str(err))
        finally:
            if r: r.close()

    def printItems(self):
        """
        Iterate over items from GET request and return their friendly names
        """
        if len(self.json_resp) == 0:
            return None
        for i in range(len(self.json_resp["items"])):
            print(self.json_resp["items"][i]["name"])

    def FindID(self, choice):
        """
        Take a name as input and find the associated object ID
        """
        for i in range(len(self.json_resp["items"])):
            if choice in self.json_resp["items"][i].values():
                object_id = self.json_resp["items"][i]["id"]
        return object_id





if __name__ == '__main__':
    # Read in file with parsing
    # Create global dictionary
    with open('groups.csv', 'r', encoding='utf-8-sig') as c:
        csv = c.readlines()
    objects = {}
    group = ''
    for c in csv:
        split = c.split(',')
        if split[0] != '':
            group = split[0].strip()
            objects.update({group: []})
        if split[3].endswith('\n'):
            split[3] = split[3][:-1]
        objects[group].append([split[1], split[2], split[3]])
    for k, v in objects.items():
        create_full_group(k, v)
    # net = fmc.PostApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networks', net_obj)
    # obj = fmc.GetApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networks')
    # net = fmc.PostApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networkgroups', net_group)
