from ast import Pass
from pprint import pprint  # used later below in helper action "members"
from datetime import datetime
import os
from unittest import mock
members = []  # array to store all the members of the club
current_member = ""
global currMember

#array that keeps a log of the # of members that atttended weekly. 
#Ex: [3, 4, 5, -1] 3 attended week 1, 4 attended week 2, etc,. when val -1 then week has not had meeting yet
membersAttended = [0, 0, 0, 0] 
weekNumber = 1
monthNumber = 0
membersAttendedThisWeek = []


class Member:  # after a member registers providing the details below his account is created with the information below
    def __init__(self, first_name, last_name, email, password, mail):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mail = mail

        self.amountDue = 0 #how much money a member owes for this month
        self.weeksDue = 0 #the weeks member hasn't paid for yet
        self.attended = 0 #total weeks member attended


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
    fn = input("First name: ")
    ln = input("Last name: ")
    email = input("Email: ")
    password = input("Password: ")
    if user_signUpError(fn, ln, email, password) == True:
        member = Member(fn, ln, email, password, [])
        members.append(member)
        clear()
        print("You have successfully created an account", member.first_name, "!")
        print("'Login' to access your account.")


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
        payment_reminder()
        welcome_page()


def welcome_page():
    print("Welcome "+current_member+"!")
    if(current_member == "Coach "):
        print("'check/send mail', 'attendees', 'remove member' or 'logout'")
    else:
        print("'check mail', 'make payment', 'logout'")


def user_logout():
    clear()
    global current_member
    current_member = ""
    main()


# this function allows coach to send mail to members
def send_mail():
    clear()
    if (current_member == ""):
        print("You must be logged in to send mail!")
        main()
        return

    if (current_member != "Coach "):
        print("You do not have access to perform this action")
        welcome_page()
        return

    send_to = input("Type 'all' to send to all members\nTo: ")
    message = input("Enter the message you would like to send: ")
    if send_to == "all":
        for member in members:
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
            fr = "From:" + current_member+"\n"
            member.mail.append(date_time+fr+message)
        print("Message sent!")
    else:
        for member in members:
            if member.email == send_to:
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                fr = "From: " + current_member+"\n"
                member.mail.append(date_time+fr+message)
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
    print("\nPlease select one of the options below:")
    print("'check mail', 'make payment', 'logout'")


# this function allows the user to make a one-time payment
def make_payment():
    if (current_member == ""):
        print("You must be logged in to make a payment!\n")
        main()

    clear()
    print("Welcome to the payment page!\n")
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            global currMember
            currMember = member
            break
    print("Your Account Membership Fees: $", currMember.amountDue)
    print("Your account owes for "+str(currMember.weeksDue)+" practise sessions:")

    user_inp = input("\nMake a single-time payment? ('Yes'/'No')\n> ")
    clear()

    if currMember.amountDue == 0 and currMember.weeksDue == 0 and (user_inp == "yes" or user_inp == "Yes"):
        print("Your account owes no fees!\nTaking you to the home page!")
        welcome_page()

    if user_inp == "yes" or user_inp == "Yes":
        amount = input("Enter the amount: $")
        payment_type = input(
            "Please select a payment type: Debit or Credit \n> ")

        while ((payment_type != "Debit") and (payment_type != "Credit")):
            payment_type = input(
                "Select a valid payment method.\nPlease select a payment type: 'Debit' or 'Credit' \n> ")
        card_info = input("Please enter your card number (xxxxXXXXxxxxXXXX): ")
        card_date = input("Please enter expiry date (XXXX): ")

        while valid_payment(card_info, card_date) == False:
            print("Your card details are incorrect, please try again!")
            card_info = input("Please enter your card number: ")
            card_date = input("Please enter expiry date (XXXX): ")

        currMember.amountDue -= int(amount)
        currMember.weeksDue -= 1
        clear()
        print("Payment was successful!")

        user_inp = input("Make Another Payment? (yes|no)\n> ")
        if user_inp == "yes":
            make_payment()
        elif user_inp == "no":
            welcome_page()
            return
    else:
        welcome_page()


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


def payment_reminder():
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            global currMember
            currMember = member
            if (currMember.weeksDue > 0 and current_member != "Coach " and current_member != "Treasurer "):
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                message = "You have insufficient funds for this month.\nPlease make a payment to your account.\nEnter 'make payment' to get started!"
                member.mail.append(date_time+message)

#removes a member from the system
def remove_member():
    clear()
    print("Please provide the first and last name of the member you would like to remove: \n")
    memberRemoveF = input("First: ")
    memberRemoveL = input("Last: ")

    for x in members:
        found = False
        if (x.first_name == memberRemoveF) and (x.last_name == memberRemoveL):
            members.remove(x)
            found = True
            print("Successfully removed "+memberRemoveF+" "+memberRemoveL+"\n")
    if not found:
        print("Could not find "+memberRemoveF+" "+memberRemoveL+" in the system, please try again\n")


    print("Please select one of the option below:")
    print("'check/send mail', 'attendees', 'remove member' or 'logout'")


#this function simulates the next week and updates the weekly values correspondingly
def updateWeek():
    global weekNumber
    global membersAttendedThisWeek
    global membersAttended
    if weekNumber == 4:
        updateMonth()
        weekNumber = 1
    else:
        weekNumber += 1
        membersAttended = [-1, -1, -1, -1]
        membersAttendedThisWeek = []
        

#this function simulates the next month and updates the monthly values correspondingly
def updateMonth():
    global monthNumber
    global membersAttendedThisWeek
    global membersAttended
    monthNumber += 1
    membersAttended = [-1, -1, -1, -1]
    membersAttendedThisWeek = []


def updateAttendees():
    
    clear()
    if (current_member == ""):
        print("You must be logged in to send mail!")
        main()
        return

    if (current_member != "Coach "):
        print("You do not have access to perform this action!")
        welcome_page()
        return

    global weekNumber
    global membersAttended
    global membersAttendedThisWeek
    print("Members who attended todays meet: " + str(membersAttendedThisWeek) + "\n")

    member = input("Enter member's first and last name. Ex: 'John Doe'. Enter done when finished.\n> ")
    while(member != 'Done'):
        for mem in members:
            if mem.first_name+" "+mem.last_name == member:
                membersAttendedThisWeek.append(mem)
                mem.attended += 1
                mem.amountDue += 10
                mem.weeksDue += 1
                membersAttended[weekNumber-1] = (membersAttended[weekNumber-1] + 1)

                
        member = input("> ")
    
    print("List of members who attended: " + str(membersAttendedThisWeek) + "\nWant to add more? (Yes/No)")
    action = input("> ")
    if (action == "Yes"):
        updateAttendees()
    else:
        clear()
        welcome_page()

def income_statement():
    clear()
    if (current_member == ""):
        print("You must be logged in to send mail!")
        main()
        return

    if (current_member != "Treasurer "):
        print("You do not have access to perform this action!")
        welcome_page()
        return

    print("Income Statement: \n")

    print("Revenue: \n")
    accountPayables = 0
    for x in members:
        if (x.amountDue<0):
            accountPayables += abs(x.amountDue)
    print(accountPayables)

            
    

    

    print("Expenses: \n")

    print("Net income: \n")

    print("Months profits: \n")
    



    





# basically like a main function where everything else happens
def main():
    print("Welcome to MEM club!\nLogin or Register\n")
    actions = ""
    options = "Register, Login, Members, send mail, check mail, make payment, logout"

    while(actions != "quit"):
        actions = input("> ")
        if(actions == "Register" or actions == "register"):
            user_signUp()
        elif(actions == "Login" or actions == "login"):
            user_login()
        # helper action for u guys to check the members
        elif(actions == "Members" or actions == "members"):
            for x in members:
                pprint(vars(x))
        #helper action to simulate a week passing
        elif(actions == "next week"):
            updateWeek()
        #helper action to simulate a month passing
        elif(actions == "next month"):
            updateMonth()
        elif(actions == "send mail"):
            send_mail()
        elif(actions == "check mail"):
            check_mail()
        elif(actions == "make payment"):
            make_payment()
        elif(actions == "logout"):
            user_logout()
        elif(actions == "options"):
            print(f"\nOptions Available:\n{options}")
        elif(actions == "attendees") :
            updateAttendees()
        elif(actions == "remove member"):
            remove_member()
        elif(actions=="income statement"):
            income_statement()
        elif(actions != "quit"):
            print("Action not recognized, please enter a valid input.")


clear()
main()