import os

from speakerMan import sayTheThing
def rename():
    sayTheThing('Fill required data')
    os.chdir(input('Directoty: '))

    target = input('Target Files: ')
    changeTo = input('Rename Files To: ')

    for count, f in enumerate(os.listdir()):
        f_name, f_ext = os.path.splitext(f)
        if f_ext == target:
            new_name = f'{f_name}{changeTo}'
            if input(f'{f_name}{f_ext} -> {f_name}{changeTo}: (y)') == '':
                os.rename(f, new_name)
            else:
                sayTheThing("Skipped!")

    
    return 'rename'