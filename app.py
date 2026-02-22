import streamlit as st
import json
import random
import string
from pathlib import Path

# ---------- Page Config ----------
st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>
.big-title {
    font-size:40px;
    font-weight:bold;
    text-align:center;
    background: linear-gradient(to right, #1f4037, #99f2c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stButton>button {
    background-color:#1f4037;
    color:white;
    border-radius:10px;
    height:3em;
    width:100%;
    font-size:16px;
}
.stButton>button:hover {
    background-color:#99f2c8;
    color:black;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🏦 Bank Management System</p>', unsafe_allow_html=True)

# ---------- Database ----------
DATABASE = "data.json"

if Path(DATABASE).exists():
    with open(DATABASE) as f:
        data = json.load(f)
else:
    data = []

def save_data():
    with open(DATABASE, "w") as f:
        json.dump(data, f)

def generate_account():
    digits = random.choices(string.digits, k=4)
    alpha = random.choices(string.ascii_letters, k=4)
    acc = digits + alpha
    random.shuffle(acc)
    return "".join(acc)

# ---------- Sidebar ----------
menu = st.sidebar.selectbox("Navigation", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Account Details",
    "Update Account",
    "Delete Account"
])

# ---------- Create Account ----------
if menu == "Create Account":
    st.subheader("📝 Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100)
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):
        if len(pin) == 4 and pin.isdigit():
            account = {
                "name": name,
                "age": age,
                "phone": phone,
                "email": email,
                "pin": int(pin),
                "account": generate_account(),
                "balance": 0
            }
            data.append(account)
            save_data()
            st.success("✅ Account Created Successfully!")
            st.info(f"Your Account Number: {account['account']}")
        else:
            st.error("❌ PIN must be 4 digits")

# ---------- Deposit ----------
elif menu == "Deposit":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = [i for i in data if i["account"] == acc and str(i["pin"]) == pin]
        if user:
            user[0]["balance"] += amount
            save_data()
            st.success("💵 Amount Deposited Successfully")
        else:
            st.error("Invalid Account or PIN")

# ---------- Withdraw ----------
elif menu == "Withdraw":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = [i for i in data if i["account"] == acc and str(i["pin"]) == pin]
        if user:
            if user[0]["balance"] >= amount:
                user[0]["balance"] -= amount
                save_data()
                st.success("💸 Amount Withdrawn Successfully")
            else:
                st.error("Insufficient Balance")
        else:
            st.error("Invalid Account or PIN")

# ---------- Account Details ----------
elif menu == "Account Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = [i for i in data if i["account"] == acc and str(i["pin"]) == pin]
        if user:
            st.json(user[0])
        else:
            st.error("Invalid Account or PIN")

# ---------- Update Account ----------
elif menu == "Update Account":
    st.subheader("✏ Update Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = [i for i in data if i["account"] == acc and str(i["pin"]) == pin]

    if user:
        name = st.text_input("New Name", value=user[0]["name"])
        email = st.text_input("New Email", value=user[0]["email"])
        phone = st.text_input("New Phone", value=user[0]["phone"])

        if st.button("Update"):
            user[0]["name"] = name
            user[0]["email"] = email
            user[0]["phone"] = phone
            save_data()
            st.success("✅ Account Updated Successfully")
    else:
        st.warning("Enter valid account details")

# ---------- Delete Account ----------
elif menu == "Delete Account":
    st.subheader("❌ Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = [i for i in data if i["account"] == acc and str(i["pin"]) == pin]
        if user:
            data.remove(user[0])
            save_data()
            st.success("Account Deleted Successfully")
        else:
            st.error("Invalid Account or PIN")