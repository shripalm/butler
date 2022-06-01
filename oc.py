import webbrowser
from googlesearch import search


def searchIt(data):
    new = 2  # open in a new tab, if possible
    webbrowser.get(using='google-chrome').open(data, new=new)


def googleIt(data):
    for i in search(data, int(input('How many results: '))):
        print(i)
