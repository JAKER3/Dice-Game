import random
import time
import os
import uuid
import hashlib
import operator

def see_leaderboard():
    see = True
    while see == True:
        reply = input("Would you like to see the whole leader board, enter y/n or \nq to completely quit the game: ")
        if reply == 'q':
            assure = input("Press enter to quit or n to go back: ")
            if assure == 'n':
                print("Returning...")
            else:
                print("Quitting game...")
                exit()
        if reply == 'y':
            board = open('Winner.txt', 'r')
            file_contents = board.read()
            print(file_contents)
            break
        elif reply == 'n':
            break
        else:
            print("Error, please enter y or n!")
        

i = 0
Player1Points = 0
Player2Points = 0
Winner_Points = 0
user1 = ''
user2 = ''

def hash_string(myString): # used to make the passwords unreadable in the txt file, to keep account protected
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + myString.encode()).hexdigest() + ':' + salt
    
def check_hashes(hashed_string, myString):   #   used to make the passwords readable for the code so it can chaeck if the password entered mataches
    new_string, salt = hashed_string.split(':')
    return new_string == hashlib.sha256(salt.encode() + myString.encode()).hexdigest()


def login(playerNo): #defines login
    reg = False
    #Get list of users
    lines = ()
    try:
        file = open('Login.txt', 'r') #  open file
        lines = list(file) # read all lines in file
        file.close()
    except IOError:
        ab = open('Login.txt', 'w')
        ab.close()
    UserList = {}   
    #Build a dictionary
    for line in lines:
        line = line.replace('\n', '').replace('\r', '')   # uses this to format so the system can check user credentials later
        if line and line.find(","):
            username, password = line.split(',')  # so the code knows which side is the password and username
            if username.lower() in UserList:
                print("Duplicate Registered User detected")   # checks if more than 1 user has the same name in the file
            else:
                UserList.update( {username.lower() : password} )
    while reg == False:
        username1 = input("Player " + playerNo + ", Enter your username:").lower()
        if username1.lower() in UserList:
            password1 = input("Enter Password: ")
            if check_hashes(UserList[username1.lower()], password1):   # uses check_hashes to make the password readable
                reg = True
                return(username1.lower())
            else:
                print("password doesnt match registered user, choose a differnt username or try password again")  
            
        else:
            register = input("Username " + username1 + " Not found would you like to register for the game yet? y/n ")  # if username doesn't exist it prompts user to make an account 
            if register == 'y':    
                ab = open('Login.txt', 'a')
                passwrd = input("Now enter a password: ")
                ab.write(username1.lower()) # writes credentials to the file
                ab.write(',')
                ab.write(hash_string(passwrd))
                ab.write(os.linesep)
                ab.close()
                reg = True
                return(username1.lower())
             


def roll(myUser, mytotal, tied):  # defines roll
    input('\nPress enter for your turn :')  # asks user to press enter to roll their dice
    if tied:  
        die1 = random.randint(1,6)
        dietotal = mytotal + die1
        print(myUser, 'you rolled a',die1,'in you tied challenge. Your new total: ', dietotal)
        return(dietotal)
    else:
        die1 = random.randint(1,6) # rolls both the dice
        die2 = random.randint(1,6)
        die3 = 0
        if die1 == die2:  # checks if the user rolled a double
            die3 = random.randint(1,6)
            
        dietotal = mytotal + die1 + die2 + die3
        if die3 > 0:  # checks if die3 was rolled, if it was it outputs the following messages
            time.sleep(0.2)
            print(myUser, 'you rolled a',die1,'and a', die2, ', You rolled a double!')
            time.sleep(0.2)
            print(myUser, 'Your bonus roll was', die3, 'Extra roll of the dice. Your new total: ', dietotal)
        else:
            time.sleep(0.2)
            print(myUser, 'you rolled a',die1,'and a', die2, 'making your new total: ', dietotal)
            
    if dietotal % 2 == 0:   # checks to see if the total is odd or even
        dietotal += 10 # This is even so it adds 10
        time.sleep(0.2)
        print(myUser, 'your total is even so you get bonus 10 points making your score: ', dietotal)
    else:
        if (dietotal - 5) < 0:  # This is odd, it checks to see if it will go under 0, if so it will make it 0 
            time.sleep(0.2)
            print(myUser, 'your total is odd so you lose', dietotal, 'making your score zero')
            dietotal = 0
        else:
            dietotal -= 5   # Odd so it takes 5 as it knows it will not go under 0
            time.sleep(0.2)
            print(myUser, 'your total is odd so you lose 5 points  making your score: ', dietotal)
    return(dietotal)

see_leaderboard()

user1 = login("1") # makes the value of the variable
if user1 != '':
    user2 = login("2") # makes the value of the second variable
else:
    print("No")

print("Users ", user1, user2)

for i in range(0,5):  # rolls for both players 5 times
    Player1Points = roll(user1,Player1Points,0)
    time.sleep(1)
    Player2Points = roll(user2,Player2Points,0)
    time.sleep(1)

    #Player1Points = 10, this was used to test the draw system at the end of the game
    #Player2Points = 10
while Player1Points == Player2Points:  # checks if the players are tied and enters game to decide winner
    time.sleep(0.2)
    print('Tied scores entering roll off, highest roll wins')
    Player1Points = roll(user1,Player1Points,1)
    time.sleep(1)
    Player2Points = roll(user2,Player2Points,1)
    time.sleep(1)

if Player1Points>Player2Points: #checks who the winner is and defines the varibles for the leader board
    Winner_Points = Player1Points
    winner_User = user1
    winner = (Winner_Points, user1)
elif Player2Points>Player1Points:
    Winner_Points = Player2Points
    winner = (Winner_Points, user2)
    winner_User = user2

time.sleep(0.2)
print('Well done,', winner_User,'you won with',Winner_Points,'Points') # oututs winner for users to see


#winner = (Winner_Points, winner_User)
line = ()
try:
    file = open('Winner.txt', 'r')
    lines = list(file)
    file.close()
except IOError:
    ab = open('Winner.txt', 'w')
    ab.close()
HighScoreTable = {}
#Build a dictionary
for line in lines:
    line = line.replace('\n', '').replace('\r', '')
    if line and line.find(","):
        score, user = line.split(',')
        if user in HighScoreTable: # checks if the user is in the leader board more than once
            print("Duplicate User detected in high score table")
        else:
            HighScoreTable.update( {user : int(score)} )

if winner_User in HighScoreTable: # checks if the user is already in the file
    if HighScoreTable[winner_User] <= Winner_Points: # checks if their new score is larger than their old score
        HighScoreTable.update( {winner_User : Winner_Points} ) # if it is then it updates the file with the new score
else:
    HighScoreTable.update( {winner_User : Winner_Points} )

#Update file
f = open('Winner.txt', 'w')
for usr, val in HighScoreTable.items():  # formats the file with the information
    f.write(str(val))
    f.write(',')
    f.write(str(usr))
    f.write(os.linesep)
f.close()

#Print high scores
HighScore_by_value = sorted(HighScoreTable.items(), key=operator.itemgetter(0),reverse=True)# sorting the txt file by score
d = sorted(HighScoreTable.items(),key=lambda x: (x[1], x[0]), reverse=True)  # Value then Key
print("\nTop 5 Scores")
topcnt = 0
for usr, val in d:
    topcnt += 1
    print(val,usr)
    if topcnt > 4: # outputs top users until it reaches 5
        break
