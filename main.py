from pprint import pprint
members = []  # array to store all the members of the club
current_member = ""


class Member:  # after a member registers providing the details below his account is created with the information below
    def __init__(self, first_name, last_name, email, password, mail):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mail = mail


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
    elif ("@" in email) == False or ("." in email) == False:
        print("Invalid email, please enter a valid email")
        return False
    else:
        return True


def user_signUp():
    fn = input("First name : ")
    ln = input("Last name : ")
    email = input("Email : ")
    password = input("Password : ")
    if user_signUpError(fn, ln, email, password) == True:
        member = Member(fn, ln, email, password, [])
        members.append(member)


def user_loginError(email, password):
    global current_member
    if(members == []):
        return False
    for member in members:
        if member.email == email and member.password == password:
            current_member = member.first_name+" "+member.last_name
            return True
    return False


def user_login():
    email = input("Email : ")
    password = input("Password : ")
    if user_loginError(email, password) == False:
        print("Invalid login credentials")
    else:
        print("Welcome back "+current_member)


print("Welcome to MEM club!")
actions = ""
while(actions != "quit"):
    actions = input()
    if(actions == "Register" or actions == "register"):
        user_signUp()
    elif(actions == "Login" or actions == "login"):
        user_login()
    elif(actions == "Members" or actions == "members"):
        for x in members:
            pprint(vars(x))
