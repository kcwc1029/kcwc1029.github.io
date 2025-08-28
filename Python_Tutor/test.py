arr = {'Apple': "22233", 'Orange': "202020", 'Banana': "3030303"}



username = input("請輸入帳號：")
passwd = input("請輸入密碼：")
# print(username, passwd)



if username in arr:
    if arr[username] == passwd:
        print("使用者你好")
    else:
        print("沒有這個帳號")    
else:
    print("沒有這個帳號")



# if()

# if()


# 
# 帳號不存在
