import webbrowser
from googlesearch import search


def searchIt(data):
    new = 2  # open in a new tab, if possible
    webbrowser.get(using='google-chrome').open(data, new=new)


def googleIt(data):
    for i in search(data, tld="co.in", num=10, stop=10, pause=2):
        print(i)
