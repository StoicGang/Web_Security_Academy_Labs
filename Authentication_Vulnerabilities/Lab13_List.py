print('[', end ='')

with open('password.txt', 'r') as f:
        lines = f.readlines()

for pwd in lines:
        print('"' + pwd.strip('\n') + '",', end ='')

print('"random"],', end ='')