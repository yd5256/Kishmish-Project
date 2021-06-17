import cgi
import webbrowser
import os
import smtplib, ssl
import sys

#--------------------------------------------
#FUNCTION DEFS
#--------------------------------------------

#This function is used in the displayWebsite function, and depending on the input parameter
#isOverwriting, it will either overwrite the chosen file, or will just add to it, then it will
#do whichever option was chosen by either adding to or replacing the file contents with the htmlCode string
def writeWebsite(htmlCode,filename,isOverwriting):
    if isOverwriting == True:
        f = open(filename,'w')
    else:
        f = open(filename,'a')
    f.write(htmlCode)
    f.close

#This function creates an html document to store html code, then displays it as a website on a browser
#This function uses a relative path to get to the file on any computer,
#rather than an absolute path to get to a file on a specific computer (This is normally required on Mac,
#but by using the os library, a relative path can still be used
#Takes in a boolean parameter isDisplaying to know whether or not to just change the html file or to both change it and display it
def displayWebsite(theHtmlCode,theFilename,overwriting,isDisplaying):
    writeWebsite(theHtmlCode,theFilename,overwriting)
    if isDisplaying == True:
        webName = 'file:///'+os.getcwd()+'/' + theFilename
        webbrowser.open_new_tab(webName)

#Sends an email securely using ssl and an smtp server
#Sends the email to a given email by being given a sender email and that email's password
def sendEmail(theServer,portNum,sender,receiver,senderPassword,theMessage):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(theServer, portNum, context=context) as server:
        server.login(sender, senderPassword)
        server.sendmail(sender, receiver, theMessage)

#Function that checks to see if what the user inputted is an integer using a try, except, and else statement
#If not an integer, keeps prompting user until they enter an integer
#Returns the input as an integer
def user_input(theInput):
    while isinstance(theInput,int) == False:
        try:
            int(theInput)
        except:
            theInput = input('\nINVALID INPUT. Please enter a number: ')
        else:
            theInput = int(theInput)
      
    return int(theInput)

#Checks if the user typed "y" or "n" as input using a while loop, then keeps prompting until they
#type "y" or "n"
#Lowers the input just in case user types the capital form of these letters
def y_or_n_checker(theInput):
    theInput = theInput.lower()
    while theInput != 'y' and theInput != "n":
        theInput = input("\nINVALID INPUT. Please type y or n: ")
        theInput = theInput.lower()
    return theInput

#--------------------------------------------
#MAIN CODE
#--------------------------------------------


#Opens/Creates the history website file since it will be accessed before it can first be created
temporaryHistory = open("reverse_parenthesis_history.html",'a')
temporaryHistory.close

#Welcome message and directions
print("Welcome to the Parenthesis Phrase Reverser!")
print("Type in a phrase with balanced parenthesis (Example: \"(u(love)i)\")")
print("and it will be reversed starting from the innermost set of parenthesis (Ex: Result of previous example would be \"iloveu\").")
print("\nPlease allow the program access to a folder on your device to create documents, as it will not function otherwise. Thank you!")

#Prompts how many phrases to be reversed
numCases = input("\nHow many phrases would you like reversed? ")
numCases = user_input(numCases)

#Some strings and a list are set up beforehand to be added to later
resultCode = """<html>
<head><title>Parenthesis Reverser Results</title></head>
<body><h1>Results:</h1>"""

historyCode = """<html>
<head><title>Parenthesis Reverser History</title></head>
<body>"""
if os.stat("reverse_parenthesis_history.html").st_size == 0:
    historyCode += """<h1>History:</h1>"""
    
results = []

emailMessage = """\
Subject: Program Result

Your Results Are:

    """

#The main algorithm that reverses the phrases
for i in range(0, numCases):
    
    #Prompts the user for a phrase
    case = input("\nPlease type phrase #" + str(i+1) + ": ")
    #Finds the last ( in the phrase given
    while case.count('(') != 0:
        theIndex = 0
        leftP = 0
        for i in range(len(case)):
            if case[i] == '(':
                leftP = i
            if case[i] == ')':
                rightP = i
                break
            
        #Reverses the characters in the innermost set of parenthesis, then deletes those parenthesis
        temp = case[leftP+1:rightP]
        temp = temp[::-1]
        case = case.replace(case[leftP:rightP+1],temp)
        
    #Stores the result in the history text file
    stdoutOrigin=sys.stdout 
    sys.stdout = open("reverse_parenthesis_storage.txt", "a")
    
    print(case)

    sys.stdout.close()
    sys.stdout=stdoutOrigin

    #Adds the result to multiple strings which will be used later to display those results
    historyCode += """<p>""" + case + """</p>"""
    resultCode += """<p>""" + case + """</p>"""
    results.append(case)
    emailMessage += case + """
    """

#Now that the processing is done, the string being added to are completed
resultCode += """</body></html>"""
historyCode += """</body></html>"""
emailMessage += """
Thank You."""



#The result section, the user can either view their results through a website or the terminal
#One of the string files being added to before is used to display the website
resultChoice = input("\nFinished! Would you like to see your results through a website (y/n)? ")
resultChoice = y_or_n_checker(resultChoice)

if resultChoice == 'y':
    print("\nOk, opening a webpage with your results now!")
    displayWebsite(resultCode,'reverse_parenthesis_website.html',True,True)
    errorCheck = input("\nDone! Did you see your results (y/n)? ")
    errorCheck = y_or_n_checker(errorCheck)
    if errorCheck == "n":
        print("\nOk, then here are your results:\n ")
        for i in range(len(results)):
            print(results[i])
        print("\nDone! Time to move on to the next step.")
    else:
        print("\nGreat! Time to move on to the next step.") 
else:
    print("\nOk, then here are your results:\n ")
    for i in range(len(results)):
        print(results[i])

        

#The email section, the user can choose to be sent an email with their results by typing in their email address
emailChoice = input("\nWould you like to receive an email with your results (y/n)? ")
emailChoice = y_or_n_checker(emailChoice)

if emailChoice == "y":
    userEmail = input('\nOk! Please type your email address: ')

    #When testing this, the program would give an error when certificates were not installed using a file from IDLE, so this message to the user makes sure that they install certificates before using the email feature
    print('\n(If an invalid input prompt keeps showing when you type in a valid address, you may have to verify certificates on your device. If running this on IDLE, please go to the Python folder and click the Install Certificates.command file. If using a different software, you will need to look up how to install certificates with your software. Don\'t worry, this is a one time action! Then, you can be sent emails!)')

    #Checks if the user input is a valid email address, keeps prompting again until it is valid
    emailSentChecker = False
    while emailSentChecker == False:
        try:
            sendEmail("smtp.gmail.com",465,"reverseparenthesisprogram@gmail.com",userEmail,"KishmishIsCool",emailMessage)
        except:
            userEmail = input('\nINVALID INPUT. Please enter a valid email address: ')
        else:
            emailSentChecker = True      
    print("\nDone! Your email has been sent! Time to move on to the next step.")
else:
    print("\nOk, let\'s move on to the next step.")



#The history section, the user can choose to view their result history through a website,
#or the terminal if they can't see the website
#One of the string being added to before is used for the website, another is used for the terminal view
#This is also where the history html file is added to or cleared
historyChoice = input('\nWould you like to see your result history (on a webpage) (y/n)? ')
historyChoice = y_or_n_checker(historyChoice)

if historyChoice == 'y':
    displayWebsite(historyCode,'reverse_parenthesis_history.html',False,True)
    historyCheck = input("\nDone! Did you see your history? ")
    historyCheck = y_or_n_checker(historyCheck)
    if historyCheck == 'n':
            print("\nOk, then here is your history: \n")
            historyText = open('reverse_parenthesis_storage.txt', 'r')
            history_contents = historyText.read()
            print(history_contents)
            historyText.close
    else:
        print("\nGreat! Time to move on to the next step.")

    #If the user does view their history, they can choose to clear it, which will delete all data in both the html and txt files for history
    deleteHistory = input("\nAfter seeing your history, would you like to clear it (y/n)? ")
    deleteHistory = y_or_n_checker(deleteHistory)
    if deleteHistory == "y":
        historyDeleteTxt = open("reverse_parenthesis_storage.txt", "w")
        historyDeleteTxt.close
        historyDeleteHtml = open("reverse_parenthesis_history.html","w")
        historyDeleteHtml.close
        print("\nOk, your result history has been cleared!")
    else:
        print("\nOk, sounds good!")
else:
    displayWebsite(historyCode,'reverse_parenthesis_history.html',False,False)
    print('\nOk, sounds good!')

#Goodbye message
print("\nThat's everything! Thank you for using the Parenthesis Phrase Reverser! Have a great day!")
print('\nPROGRAM TERMINATED')













