from ast import Pass
from pprint import pprint  # used later below in helper action "members"
from datetime import datetime
import os
from unittest import mock
members = []  # array to store all the members of the club
current_member = ""
global currMember
global reminder
reminder = False

#array that keeps a log of the # of members that atttended weekly. 
#Ex: [3, 4, 5, 0] 3 attended week 1, 4 attended week 2, etc,. when val 0 then week has not had meeting yet
membersAttended = [0, 0, 0, 0]
weekNumber = 1 #1 - 4 weeks. resets to 0 when > 4
monthNumber = 0
membersAttendedThisWeek = []
accountPayables = 0
memberPayments = 0

monthlyUnpaidDebt = [{'monthNumber':monthNumber, 'monthlyDebt':0}]
monthlyProfits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class Member:  # after a member registers providing the details below his account is created with the information below
    def __init__(self, first_name, last_name, email, password, mail):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mail = mail

        self.amountDue = 0 #how much money a member owes for this month
        self.weeksDue = 0 #the weeks member hasn't paid for yet
        self.attended = 0 #number of weeks a member attended. Max = 4 weeks, then resets to 0. (simulates a month passing)


Treasurer = Member("Treasurer", "", "treasurer@mem.com", "treasurer123", [])
members.append(Treasurer)
Coach = Member("Coach", "", "coach@mem.com", "coach123", [])
members.append(Coach)

members.append(Member("k", "y", "ky@mem.com", "ky", []))
members.append(Member("j", "k", "jk@mem.com", "jk", []))
members.append(Member("s", "y", "sy@mem.com", "sy", []))
members.append(Member("y", "y", "yy@mem.com", "yy", []))



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
        penalty_fee()
        welcome_page()


def welcome_page():
    print("Welcome "+current_member+"!")
    if(current_member == "Coach "):
        print("'check/send mail', 'attendees', 'remove member', 'sort members' or 'logout'")
    elif(current_member == "Treasurer "):
        print("'check mail', 'make payment', 'income statement', 'logout'")
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
    print("Your account owes for "+str(currMember.weeksDue)+" practice sessions:")

    user_inp = input("\nMake a single-time payment? ('Yes'/'No')\n> ")
    clear()

    if currMember.amountDue <= -10 and currMember.weeksDue == 0 and (user_inp == "yes" or user_inp == "Yes"):
        print("Your account owes no fees!\nTaking you to the home page!")
        welcome_page()
        return

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

        currMember.amountDue -= float(amount)
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
        return


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

# this function sends a payment reminder message to member if they attended a practise and have not made a payment
def payment_reminder():
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            global currMember
            currMember = member

            if (currMember.amountDue > 0 and current_member != "Coach " and current_member != "Treasurer "):
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                global message
                message = "You have insufficient funds for this month.\nPlease make a payment to your account.\nEnter 'make payment' to get started!"
                global reminder
                if reminder == False:
                    member.mail.append(date_time+message)
                    reminder = True
def penalty_fee():
    for member in members:
        if member.first_name+" "+member.last_name == current_member:
            if (member.amountDue > 10 and current_member != "Coach " and current_member != "Treasurer "):
                member.amountDue += 1.5
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y %H:%M") + "\n"
                message = "Your account has been charged a penalty fee of $1.50 as a result of missed payments.\nMake a payment by entering 'make payment' to avoid additional fees!"
                member.mail.append(date_time+message)
                    
#removes a member from the system
def remove_member():
    clear()
    print("Please provide the first and last name of the member you would like to remove: \n")
    memberRemoveF = input("First: ")
    memberRemoveL = input("Last: ")

    for member in members:
        found = False
        if (member.first_name == memberRemoveF) and (member.last_name == memberRemoveL):
            members.remove(member)
            found = True
            print("Successfully removed "+memberRemoveF+" "+memberRemoveL+"\n")
    if not found:
        print("Could not find "+memberRemoveF+" "+memberRemoveL+" in the system, please try again\n")


    print("Please select one of the option below:")
    print("'check/send mail', 'attendees', 'remove member', 'sort members' or 'logout'")

#sorts members by paid, not paid, or attendance
def sort_members():
    clear()
    sortType = input("Please enter if you want to sort the members by paid, not paid or attendance: ")

    if sortType == "not paid":
        new1 = sorted(members, key=lambda x: x.weeksDue, reverse =True)
        for x in new1:
            if x.amountDue>0:
                print(x.first_name+" "+x.last_name+" has not paid for "+str(x.weeksDue)+" week/s")
    if sortType == "paid":
        found = False
        new2 = sorted(members, key=lambda x: x.amountDue, reverse = False)
        for x in new2:
            if x.amountDue==0 and not x.attended == 0:
                print(x.first_name+" "+x.last_name+" has paid for "+str(x.attended)+" of the attended weeks")
                found = True
            if x.amountDue<0:
                print(x.first_name+" "+x.last_name+" has paid for "+str(x.attended)+" of the attended weeks and left $"+str(abs(x.amountDue))+" for future ones.")
                found = True
        if not found:
            print("No members have paid for a meeting this month")

    if sortType == "attendance":
        new3 = sorted(members, key=lambda x: x.attended, reverse = True)
        for x in new3:
            if not x.first_name == "Coach" and not x.first_name=="Treasurer":
                print(x.first_name+" "+x.last_name+" has attended "+str(x.attended)+" classes in one month")

    print("\nPlease select one of the option below:")
    print("'check/send mail', 'attendees', 'remove member', 'sort members' or 'logout'")


#this function simulates the next week and updates the weekly values correspondingly
def updateWeek():
    global weekNumber
    global membersAttendedThisWeek
    global membersAttended
    global accountPayables
    global memberPayments
    memberPayments = 0
    accountPayables = 0

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
    global accountPayables
    global memberPayments
    monthNumber += 1
    membersAttended = [-1, -1, -1, -1]
    membersAttendedThisWeek = []
    accountPayables = 0
    memberPayments = 0
    for member in members:
            member.attended = 0


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

#calculates the month's current revenue
def revenue():
    global accountPayables
    global memberPayments

    for member in members:
        if (member.amountDue<0):
            accountPayables += abs(member.amountDue)
        elif(member.amountDue == 0 and member.attended > 0 and member.weeksDue == 0):
            memberPayments += member.attended * 10

#calculates and returns the net income, and also updates monthlyProfits and monthlyUnpaidDebts
def net_income():
    net_income = 0
    global monthNumber
    global accountPayables
    global memberPayments
    global monthlyUnpaidDebt # [{'monthNumber':monthNumber, 'monthlyDebt':monthlyDebt}]

    revenue()

    net_income = memberPayments + accountPayables - 400 - 60 - 400


    monthlyProfits[monthNumber] = net_income

    for aMonthsDebt in range(len(monthlyUnpaidDebt)):
        if(monthlyUnpaidDebt[aMonthsDebt]['monthNumber'] == monthNumber and net_income < 0):
            monthlyUnpaidDebt[aMonthsDebt]['monthlyDebt'] = net_income
            break
        elif(monthlyUnpaidDebt[aMonthsDebt]['monthNumber'] == monthNumber and net_income >= 0):
            monthlyUnpaidDebt[aMonthsDebt]['monthlyDebt'] = 0
            break
        elif(net_income < 0):
            monthlyUnpaidDebt.append({'monthNumber':monthNumber, 'monthlyDebt':net_income})
        elif(net_income >= 0):
            monthlyUnpaidDebt.append({'monthNumber':monthNumber, 'monthlyDebt':0})


    
    return net_income


#prints the income statement
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

    print("Income Statement")
    print("=-=-=-=-=-=-=-=-\n")

    print("Revenue:")
    print("---------")
    revenue()
    print("Member payments      \t" + str(memberPayments))
    print("Account payables     \t" + str(accountPayables) + "\n")

    print("Expenses:")
    print("---------")
    print("Hall expenses        \t400")
    print("Equipment maintenance\t60")
    print("Coach's Salary       \t400\n")

    print("Net income:")
    print("---------")
    netIncome = net_income()
    print("Revenue - Expenses   \t" + str(netIncome) + "\n")

    print(monthlyProfits)
    print(monthlyUnpaidDebt)

    print("\nMonths profits:")
    print("---------")
    




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
        elif(actions=="sort members"):
            sort_members()
        elif(actions != "quit"):
            print("Action not recognized, please enter a valid input.")
        elif(actions == "quit"):
            clear()
            exit()


clear()
main()
