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
    os.system('cls')
    fn = input("First name : ")
    ln = input("Last name : ")
    email = input("Email : ")
    password = input("Password : ")
    if user_signUpError(fn, ln, email, password) == True:
        member = Member(fn, ln, email, password, [])
        members.append(member)
        os.system('cls')
        print("You have successfully created an account",member.first_name,"!")

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
    os.system('cls')
    email = input("Email : ")
    password = input("Password : ")
    if user_loginError(email, password) == False:
        print("Invalid login credentials")
    else:
        os.system('cls')
        print("Welcome back "+current_member)

def user_logout():
    os.system('cls')
    global current_member
    current_member = ""
    print(current_member)
    main()

        
# this function allows coach to send mail to members 
def send_mail():
    os.system('cls')
    if (current_member == ""):
        print("You must be logged in to send mail!")
        main()
    
    send_to= input("Type 'all' to send to all members\nTo: ")
    message = input("Enter the message you would like to send: ")
    if send_to == "all":
        for member in members:
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
    os.system('cls')
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
                    print(i,"\n")
        


# basically like a main function where everything else happens
def main():
    #os.system('cls')
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
        elif(actions == "send"):
            send_mail()
        elif(actions == "check mail"):
            check_mail()
        elif(actions == "logout"):
            user_logout()
main()
