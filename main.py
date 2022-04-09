from pprint import pprint  # used later below in helper action "members"
from datetime import datetime
import os
members = []  # array to store all the members of the club
current_member = ""


class Member:  # after a member registers providing the details below his account is created with the information below
    def __init__(self, first_name, last_name, email, password, mail):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mail = mail


Treasurer = Member("Treasurer", "", "treasurer@mem.com", "treasurer123", [])
members.append(Treasurer)
Coach = Member("Coach", "", "coach@mem.com", "coach123", [])
members.append(Coach)


def clear():
    cmd = 'clear'
    if os.name in ('nt', 'dos'):
        cmd = 'cls'
    os.system(cmd)

# function below checks fn, ln, email and password, ensrues fields are not left empty/proper chars are inputted


def user_signUpError(fn, ln, email, password):
    if bool(fn and not fn.isspace()) == False:
        print("Invalid first name, field left blank")
        return False
    elif fn.isalpha() == False:
        print("Invalid first name, please only enter letters")
        return False
    elif bool(ln and not ln.isspace()) == False:
        print("Invalid last name, field left blank")
        return False
    elif ln.isalpha() == False:
        print("Invalid last name, please only enter letters")
        return False
    elif bool(email and not email.isspace()) == False:
        print("Enter a valid email, field left blank")
    elif ("@" in email) == False or ("." in email) == False:
        print("Invalid email, please enter a valid email")
        return False
    elif bool(password and not password.isspace()) == False:
        print("Enter a valid password, field left blank")
        return False
    else:
        return True

# function below registers a user and if the user entered valid information adds the user to an array of members


def user_signUp():
    clear()
    fn = input("First name : ")
    ln = input("Last name : ")
    email = input("Email : ")
    password = input("Password : ")
    if user_signUpError(fn, ln, email, password) == True:
        member = Member(fn, ln, email, password, [])
        members.append(member)
        clear()
        print("You have successfully created an account", member.first_name, "!")

# function below checks if the user has entered a valid email/password (if the user has an account)


def user_loginError(email, password):
    global current_member
    if(members == []):
        return False
    for member in members:
        if member.email == email and member.password == password:
            current_member = member.first_name+" "+member.last_name
            return True
    return False


# function gives user an interface to enter email and password and checks the information provided
# by the user and prints the information accordingly
def user_login():
    clear()
    email = input("Email : ")
    password = input("Password : ")
    if user_loginError(email, password) == False:
        print("Invalid login credentials")
    else:
        clear()
        print("Welcome back "+current_member)


def user_logout():
    clear()
    global current_member
    current_member = ""
    print(current_member)
    main()


# this function allows coach to send mail to members
def send_mail():
    clear()
    if (current_member == ""):
        print("You must be logged in to send mail!")
        main()

    send_to = input("Type 'all' to send to all members\nTo: ")
    message = input("Enter the message you would like to send: ")
    if send_to == "all":
        for member in members:
            if(member != Coach):
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                member.mail.append(date_time+message)
                print("Message sent!")
    else:
        for member in members:
            if member.email == send_to:
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                member.mail.append(date_time+message)
                print("Message sent!")


def check_mail():
    clear()
    if (current_member == ""):
        print("You must be logged in to check mail!")
        main()
    print("Welcome to your inbox! \n")
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            if not member.mail:
                print("You have no mail.")
            else:
                for i in member.mail:
                    print(i, "\n")


# this function allows the user to make a one-time payment
def make_payment():
    if (current_member == ""):
        print("You must be logged in to make a payment!\n")
        main()

    clear()
    print("Welcome to the payment page!\n")
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            currMember = member
            break
    print("Your Account Membership Fees: $", currMember.amountDue)
    print("Your Account owes this many month of rent:", currMember.monthsDue)
    user_inp = input("\nMake a single-time payment?\n")
    amount = input("Enter the amount : $")

    clear()
    if user_inp == "yes":
        payment_type = input(
            "Please select a payment type: Debit or Credit \n:")

        while payment_type != "Debit":
            payment_type = input(
                "Select a valid payment method.\nPlease select a payment type: Debit or Credit \n:")
        card_info = input("Please enter your card number: ")
        card_date = input("Please enter expiry date (XXXX): ")

        while valid_payment(card_info, card_date) == False:
            print("Your card details are incorrect, please try again!")
            card_info = input("Please enter your card number: ")
            card_date = input("Please enter expiry date (XXXX): ")

        currMember.amountDue -= int(amount)
        currMember.monthsDue -= 1
        clear()
        print("Payment was successful!")

        user_inp = input("Make Another Payment?:")
        if user_inp == "yes":
            make_payment()
        else:
            clear()
    else:
        main()


# this function tests wether the card details are correct # card digits
def valid_payment(card, date):
    if len(card) != 16:
        return False
    if len(date) != 4:
        return False
    if int(date[0]) > 1 and int(date[1]) > 12:
        return False
    for i in card:
        if isinstance(i, str) == False:
            return False


# basically like a main function where everything else happens
def main():
    print("Welcome to MEM club!\nLogin or Register\n")
    actions = ""
    while(actions != "quit"):
        actions = input()
        if(actions == "Register" or actions == "register"):
            user_signUp()
        elif(actions == "Login" or actions == "login"):
            user_login()
        # helper action for u guys to check the members
        elif(actions == "Members" or actions == "members"):
            for x in members:
                pprint(vars(x))
        elif(actions == "send" and current_member == "Coach "):
            send_mail()
        elif(actions == "check mail"):
            check_mail()
        elif(actions == "make payment"):
            make_payment()
        elif(actions == "logout"):
            user_logout()


main()
