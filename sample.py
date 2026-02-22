

data=[{"name": "yashodip", "age": 22, "phonenumber": "8010041580", "email": "yash", "pin": "1234", "accountno": "ZEU65L92", "balance": 0}]


accountno = input("enter acc : ")
pin = input("enter pin : ")

user_data = [i for i in data if i["accountno"] == accountno and i["pin"] == pin]
print(user_data)

if user_data==False:
    print("user not found")

else:
    balance=int(input("amount"))
    user_data[0]["balance"]+=balance
    print(user_data)
    



