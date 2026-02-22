import streamlit as st
import json
import random
import string
from pathlib import Path

# ==========================================
#                BANK CLASS
# ==========================================

class Bank:
    database = "data.json"
    data = []

    # Load database safely
    if Path(database).exists():
        try:
            with open(database, "r") as file:
                data = json.load(file)
        except:
            data = []
    else:
        with open(database, "w") as file:
            json.dump([], file)

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as file:
            json.dump(cls.data, file, indent=4)

    @staticmethod
    def generate_account():
        digits = random.choices(string.digits, k=4)
        letters = random.choices(string.ascii_letters, k=4)
        acc = digits + letters
        random.shuffle(acc)
        return "".join(acc)

    # CREATE ACCOUNT
    @classmethod
    def create_account(cls, name, age, phone, email, pin):

        if age < 18:
            return False, "Age must be 18+"

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must be exactly 4 digits"

        new_user = {
            "name": name,
            "age": age,
            "phone": phone,
            "email": email,
            "pin": int(pin),
            "account_no": cls.generate_account(),
            "balance": 0,
            "transactions": []
        }

        cls.data.append(new_user)
        cls.save_data()
        return True, new_user

    # GET USER
    @classmethod
    def get_user(cls, acc_no, pin):
        for user in cls.data:
            if user.get("account_no") == acc_no and user.get("pin") == int(pin):
                return user
        return None

    # UPDATE USER
    @classmethod
    def update_user(cls, user, name, age, phone, email):
        user["name"] = name
        user["age"] = age
        user["phone"] = phone
        user["email"] = email
        cls.save_data()

    # DELETE USER
    @classmethod
    def delete_user(cls, user):
        cls.data.remove(user)
        cls.save_data()

    # DEPOSIT
    @classmethod
    def deposit(cls, user, amount):
        user["balance"] += amount
        user["transactions"].append(f"Deposited ₹{amount}")
        cls.save_data()

    # WITHDRAW
    @classmethod
    def withdraw(cls, user, amount):
        if user["balance"] >= amount:
            user["balance"] -= amount
            user["transactions"].append(f"Withdrew ₹{amount}")
            cls.save_data()
            return True
        return False


# ==========================================
#                STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Bankify", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #00c6ff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 BANKIFY - Secure Digital Bank")
st.write("### Smart. Secure. Simple Banking.")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.radio(
    "Navigation",
    ["Create Account", "Login", "Delete Account"]
)

# ==========================================
# CREATE ACCOUNT
# ==========================================

if menu == "Create Account":

    st.subheader("Create New Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1)
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):
        if name and phone and email and pin:
            success, result = Bank.create_account(name, age, phone, email, pin)

            if success:
                st.success("Account Created Successfully!")
                st.info(f"Your Account Number: {result['account_no']}")
            else:
                st.error(result)
        else:
            st.warning("All fields are required")

# ==========================================
# LOGIN
# ==========================================

elif menu == "Login":

    if st.session_state.user is None:

        st.subheader("Login to Your Account")

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")

        if st.button("Login"):
            if acc and pin:
                user = Bank.get_user(acc, pin)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome {user['name']}")
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
            else:
                st.warning("Enter Account Number and PIN")

    else:
        user = st.session_state.user

        st.success(f"Welcome {user['name']}")
        st.write("💰 Current Balance:", f"₹ {user['balance']}")

        action = st.selectbox(
            "Choose Action",
            ["Deposit", "Withdraw", "View Details", "Update Details", "Transaction History", "Logout"]
        )

        if action == "Deposit":
            amount = st.number_input("Enter Amount", min_value=1)
            if st.button("Confirm Deposit"):
                Bank.deposit(user, amount)
                st.success("Deposit Successful")
                st.rerun()

        elif action == "Withdraw":
            amount = st.number_input("Enter Amount", min_value=1)
            if st.button("Confirm Withdraw"):
                if Bank.withdraw(user, amount):
                    st.success("Withdrawal Successful")
                else:
                    st.error("Insufficient Balance")
                st.rerun()

        elif action == "View Details":
            st.json(user)

        elif action == "Update Details":

            new_name = st.text_input("Name", value=user["name"])
            new_age = st.number_input("Age", value=user["age"])
            new_phone = st.text_input("Phone", value=user["phone"])
            new_email = st.text_input("Email", value=user["email"])

            if st.button("Update Details"):
                Bank.update_user(user, new_name, new_age, new_phone, new_email)
                st.success("Details Updated Successfully")
                st.rerun()

        elif action == "Transaction History":
            st.write("### 📜 Transaction History")
            if user["transactions"]:
                for t in user["transactions"]:
                    st.write("-", t)
            else:
                st.info("No transactions yet.")

        elif action == "Logout":
            st.session_state.user = None
            st.success("Logged Out Successfully")
            st.rerun()

# ==========================================
# DELETE ACCOUNT
# ==========================================

elif menu == "Delete Account":

    st.subheader("Delete Your Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        if acc and pin:
            user = Bank.get_user(acc, pin)
            if user:
                Bank.delete_user(user)
                st.success("Account Deleted Successfully")
            else:
                st.error("Invalid Credentials")
        else:
            st.warning("Enter Account Number and PIN")

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(90deg,#1f77b4,#00c6ff);
        text-align: center;
        padding: 10px;
        color: white;
        font-weight: bold;">
        🚀 Made with ❤️ by Yashodip | Bankify © 2026
    </div>
""", unsafe_allow_html=True)
