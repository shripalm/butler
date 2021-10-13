from oc import googleIt, searchIt
import datetime
from speakerMan import sayTheThing
from filerenamer import rename


def greet():
    currHour = (datetime.datetime.now()).hour
    if currHour > 6 and currHour < 12:
        sayTheThing("Good Morning")
    elif currHour >= 12 and currHour < 5:
        sayTheThing("Good After Noon")
    elif currHour >= 5 and currHour < 8:
        sayTheThing("Good Evening")
    else:
        sayTheThing("Hope you had a great day")
    askforhelp('greet')


def farewell():
    currHour = (datetime.datetime.now()).hour
    if currHour > 6 and currHour < 12:
        sayTheThing("Have a good day")
    elif currHour >= 12 and currHour < 5:
        sayTheThing("Hope you have a great Noon")
    elif currHour >= 5 and currHour < 8:
        sayTheThing("Stay tight in eve")
    else:
        sayTheThing("Good Night")
    return 'farewell'


def askforhelp(fromFunc='indipendant'):
    sayTheThing('How May i help you?')
    task = input('At last we did ' + fromFunc + ', What Now: ')
    response = eval(identifyTask(task))()
    if response != 'farewell':
        askforhelp(response)

def closeapp():
    return 'farewell'

def identifyTask(task):
    if task == 'exit' or task == 'bye' or task == 'farewell':
        return 'farewell'
    elif task == 'rename':
        return 'rename'
    else:
        ch = sayTheThing("Would you like to google it?", True)
        if ch == 'yes' or ch == 'y' or ch == True:
            googleIt(task)
            sayTheThing("Glad to help")
            askforhelp('Search Task')
        else:
            askforhelp('Wrong Task')
        return 'closeapp'


greet()
