from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('entries.db')


def clear_screen():
    """clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')


class Entry(Model):
    """creates database columns"""
    emp_name_clm = TextField()
    task_clm = TextField()
    time_spent_clm = TextField()
    timestamp = DateField(default=datetime.datetime.today, formats=['%Y-%m-%d'])
    notes_clm = TextField()

    class Meta:
        database = db


def initialize():
    """Creates the database and table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Shows the first menu"""
    clear_screen()
    choice = None

    while choice != 'q':
        print('-'*10+'WORK LOG'+'-'*10)
        print(' '*5+'-'*5+'MAIN MENU'+'-'*5)
        print()
        print('Enter q to quit.')
        for key, value in menu.items():
            print('Enter {} to {}'.format(key, value.__doc__))
        choice = input('> ').lower().strip()

        while choice not in menu and choice not in ['q', 'Q']:
            print('Not a valid choice. Please try again.')
            choice = input('> ').lower().strip()

        if choice == ('q' or 'Q'):
            print()
            print('Thanks for using the work log! See you later :)')
            sys.exit()

        menu[choice]()


def search_menu_loop():
    """Shows the search menu."""
    choice = None
    choice = None

    while not choice == 'r':
        clear_screen()
        print('-'*10+'SEARCH MENU'+'-'*10)
        print()
        print('Enter r to return to main menu.')
        for key, value in search_menu.items():
            print('Enter {} to {}'.format(key, value.__doc__))
        choice = input('> ').lower().strip()

        while True:
            try:
                if choice == ('r' or 'R'):
                    break
                search_menu[choice]()
            except KeyError:
                print('Not a valid choice. Please try again.')
                choice = input('> ').lower().strip()
            else:
                break
        # if the choice was 'r' we only got out of the first loop,
        # and we need to get out from the second, too.
        if choice == ('r' or 'R'):
            break


def add_entry():
    """add an entry"""
    clear_screen()
    emp_name = None
    task = None
    time_spent = None
    while not emp_name or not task or not time_spent:
        print()
        print(' ----!Name, task and time spent are not optional, please enter all the information!-----')
        print()
        emp_name = input("What's your name? ")
        task = input("What's the name of the task? ")
        while True:
            time_spent = input("How much time have you spent on this task?(in min) ") # TODO: check for negative numbers
            try:
                fake_timespent = int(time_spent)
                if fake_timespent <= 0:
                    raise ValueError('Time spent needs to be positive.')
            except ValueError:
                print('Not a positive integer. Please try again.')
            else:
                break

        notes = input('Any additional notes you would like to add? (Optional)')

    if notes is None:
        notes = ''

    entry_created = Entry.create(emp_name_clm=emp_name,
                                 task_clm=task,
                                 time_spent_clm=time_spent,
                                 notes_clm=notes)

    print('\n->Content successfully created!')
    input('Press enter to return to main menu.')
    menu_loop()


def view_entry(name_query=None, timespent_query=None, date_query=None, term_query=None):
    """view entries created."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if name_query:
        entries = entries.where(Entry.emp_name_clm.contains(name_query))

    if timespent_query:
        entries = entries.where(Entry.time_spent_clm == timespent_query)

    if date_query:
        entries = Entry.select().where(Entry.timestamp.contains(date_query))

    if term_query:
        entries = entries.where(Entry.task_clm.contains(term_query)
                                | Entry.notes_clm.contains(term_query))

    if len(entries) > 0:
        format_entries(entries)
    else:
        print('There are no such entries to view. '
              'Please try adding or searching something different.')


def format_entries(entries):
    """formats entries for a nice display"""
    i = 0
    while not i > len(entries):
        clear_screen()
        list_of_actions = ['r']
        i += 1
        entry = entries[i-1]
        print('DATE: '+entry.timestamp.strftime('%B %d, %Y'))
        print("Employee name: "+entry.emp_name_clm)
        print("Task: "+entry.task_clm)
        print("Time spent: " + entry.time_spent_clm + " min")
        print("Notes: "+entry.notes_clm)
        print("-"*10+"Result {} of {}".format(i, len(entries))+'-'*10)
        if len(entries) > 1 and i < len(entries):
            print('n) Next')
            list_of_actions.append('n')
        if i > 1:
            print('p) Previous')
            list_of_actions.append('p')
        print('r) Return to main/search menu')

        action = input('Action: ').lower().strip()
        if action == 'r':
            break
        if action == 'p':
            i -= 2
        if action not in list_of_actions:
            print('Not a valid option! Please try again.')
            input('Press enter to continue.')
            i -= 1


def search_entry():
    """search entry"""
    search_menu_loop()
    # when pressed r, the method will end and menu_loop method will run.
    menu_loop()


def search_name():
    """search employee's name"""
    clear_screen()
    view_entry(name_query=input('Please enter name of the employee: '))


def search_date():
    """to search date the entry created."""
    clear_screen()
    entries = Entry.select().order_by(Entry.timestamp.desc())
    for entry, i in zip(entries, range(len(entries))):
        print(str(i) + '. date:' + entry.timestamp.strftime('%Y-%m-%d'))
    while True:
        try:
            print('Please use YYYY-MM-DD format')
            date = input('Enter a date: ')
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print('Invalid date type. Please try again.')
        else:
            break
    view_entry(date_query=date)


def search_timespent():
    """to search time spent on the entry."""
    clear_screen()
    while True:
        try:
            time = input('Please enter the time spent in minutes: ').strip()
            int(time)
        except ValueError:
            print('Time spent is supposed to be integer. Please try again.')
        else:
            break
    view_entry(timespent_query=time)


def search_term():
    """to search any term in tasks and notes."""
    clear_screen()
    term = None
    while term is None:
        term = input('Please enter the term: ')
    view_entry(term_query=term)


search_menu = OrderedDict([
        ('n', search_name),
        ('d', search_date),
        ('ts', search_timespent),
        ('t', search_term)
    ])


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('s', search_entry)
])


if __name__ == '__main__':
    initialize()
    menu_loop()
