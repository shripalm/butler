import pyttsx3

engine = pyttsx3.init()
# Set voice to female if available
voices = engine.getProperty('voices')
for v in voices:
    if 'samantha' in v.name.lower():
        engine.setProperty('voice', v.id)
        break
# Set slower speech rate
rate = engine.getProperty('rate')
engine.setProperty('rate', int(rate * 0.8))  # 70% of default speed

def sayTheThing(text, inpBool=False):
    print(text)
    engine.say(text)
    engine.runAndWait()
    if inpBool:
        return(input())