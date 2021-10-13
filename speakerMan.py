import pyttsx3

engine = pyttsx3.init()

def sayTheThing(text, inpBool=False):
    print(text)
    engine.say(text)
    engine.runAndWait()
    if inpBool:
        return(input())