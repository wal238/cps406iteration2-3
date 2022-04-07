from pprint import pprint  # used later below in helper action "members"
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
    fn = input("First name : ")
    ln = input("Last name : ")
    email = input("Email : ")
    password = input("Password : ")
    if user_signUpError(fn, ln, email, password) == True:
        member = Member(fn, ln, email, password, [])
        members.append(member)

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
    email = input("Email : ")
    password = input("Password : ")
    if user_loginError(email, password) == False:
        print("Invalid login credentials")
    else:
        print("Welcome back "+current_member)


# basically like a main function where everything else happens
print("Welcome to MEM club!")
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
