print('**************Following is the list of Usernames*****************')
for i in range(150):
    if i % 3:
        print('carlos')
    else:
        print('wiener')

print('****************Following are the passwords*******************')
with open("passwords.txt", 'r') as file:
    lines = file.readlines()

i=0
for pwd in lines:
    if i % 2:
        print(pwd.strip('\n'))
    else:
        print("peter")
        print(pwd.strip('\n'))
        i = i + 1
    i = i + 1