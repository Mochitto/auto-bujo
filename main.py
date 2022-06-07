import sys
import os
import time
from calendar import monthrange
import datetime

import pymongo
import simplenote

from auto_bujo.notes_manipulation.writing import write_tasks, write_research, write_today_chores, write_today_events, write_title, \
    EXTRA_MESSAGE, write_wishlist, write_notes, write_ideas, write_expenses
from auto_bujo.notes_manipulation.reading_updating import get_new_entries, read_and_update, check_wishlist
from auto_bujo.utilities.terminal_colors import Bcolors
from auto_bujo.CRUD_operations.crud_operations import crud_operations
from auto_bujo.config import DAILY_WELCOME_MESSAGE, DB, SN, MAIN_NOTE_ID, WISHLIST_ID, NOTES_ID, IDEAS_ID, EXPENSES_ID, \
    set_credentials, configure_settings, TODAY, get_simplenote


# TODO: add tests to check everything works
# TODO: Tracking degli habits (as chores + "tracking": bool)
# TODO: Add unit tests to check right functioning of regex, database etc.


def get_upcoming_events(given_data: pymongo.CursorType = None, print_messages: bool = True):
    """Retrieve upcoming events and print them out."""
    docs = {}  # Number of days missing: array of events' messages
    missing_days = []  # Used to sort the messages
    print(f"This is the data: ")
    data = given_data if given_data else DB["events"].find({})

    for index, doc in enumerate(data):
        events_date = datetime.date.fromisoformat(doc["date"])
        days_to_event = (events_date - TODAY).days

        if 10 >= days_to_event > 0:
            missing_days_message = f"in {days_to_event} days" if days_to_event != 1 else "tomorrow"
            if days_to_event not in missing_days:
                missing_days.append(days_to_event)
            try:
                docs[days_to_event].append(f"---- {doc['date']} ({missing_days_message}) - {doc['event']}")
            except KeyError:
                docs[days_to_event] = [f"---- {doc['date']} ({missing_days_message}) - {doc['event']}"]

    missing_days.sort()

    if print_messages:
        print(f"{Bcolors.BOLD} \nThese are your events! {Bcolors.ENDC}")

    ordered_upcoming = []
    for day in missing_days:
        for message in docs[day]:
            if print_messages:
                print(message)
            else:
                ordered_upcoming.append(message)

    if not print_messages:
        return ordered_upcoming
    else:
        input("\nEnter anything to continue.")


def get_operation():
    print(f"\n{Bcolors.HEADER}{DAILY_WELCOME_MESSAGE}{Bcolors.ENDC}")

    while True:  # App closes only with exit or KEYINT
        numbers = "0 1 2 3 4"
        print(f"\n{Bcolors.BOLD}What would you like to do?{Bcolors.ENDC}\n"
              "--- 0. Update the main note (Default)\n"
              "--- 1. Upcoming events\n"
              "--- 2. CRUD operations\n"
              "--- 3. settings\n"
              "--- 4. exit\n")

        while True:
            first_input = input(f"> ")
            if first_input not in numbers:
                print(f"{Bcolors.FAIL}Invalid input. Please use one of the given numbers.{Bcolors.ENDC}")
                continue
            break

        if not first_input or first_input == "0":
            # Update note
            content = write_main()

            SN.update_note({
                "content": content,
                "key": MAIN_NOTE_ID,
                'systemTags': ['markdown'],
            })

            print(f"\n\n{Bcolors.OKGREEN}Main note updated!{Bcolors.ENDC}\n")
            input("Enter anything to continue")

        elif first_input == "1":  # Get upcoming events
            get_events(only_print_upcoming=True)

        elif first_input == "2":  # CRUD operations
            crud_operations()

        elif first_input == "3":
            print(f"\n{Bcolors.BOLD}What would you like to do?{Bcolors.ENDC}\n"
                  "--- 0. Set your Simplenote credentials\n"
                  "--- 1. Re-Link your notes to the app\n"
                  "--- 2. App Set-up\n"
                  "--- 3. Update a specific date in the diary's, the expenses' or the ideas' note\n"
                  "--- 4. Return to the menu (Default)\n")

            while True:
                choice = input(f"> ")
                if choice not in "0 1 2 3 4":
                    print(f"{Bcolors.FAIL}Invalid input. Please use one of the given numbers.{Bcolors.ENDC}")
                    continue
                break

            if choice == "0":
                get_simplenote()

            elif choice == "1":
                set_credentials(set_credentials=False, create_files=False)
                print(f"{Bcolors.OKGREEN}Your Notes have been re-linked{Bcolors.ENDC}")

            elif choice == "2":
                configure_settings(first_time=False)

            elif choice == "3":
                while True:
                    which_note = input("Which note-kind?\n"
                                       "0. Your Diary\n"
                                       "1. Your Expenses\n"
                                       "2. Your Ideas\n"
                                       "3. Go back (Default)\n"
                                       "> ")
                    if which_note not in "0 1 2 3":
                        print(f"{Bcolors.FAIL}Invalid Input{Bcolors.ENDC}")
                        continue
                    elif which_note == "0":
                        while True:
                            try:
                                work_date = input("Which day would you like to update? (YYYY-MM-DD)\n> ")
                                work_date = datetime.date.fromisoformat(work_date)
                                work_date = work_date.strftime("%A, %d %B %Y")
                                print(f"{Bcolors.OKBLUE}Updating your note...{Bcolors.ENDC}")
                                break
                            except ValueError:
                                print(f"{Bcolors.FAIL}Invalid Input{Bcolors.ENDC}")
                                continue
                        work_note = SN.get_note(NOTES_ID)[0]["content"]
                        write_notes(work_note, work_date)
                        break
                    elif which_note == "1":
                        while True:
                            try:
                                work_date = input("Which Month and year would you like to update? (YYYY-MM)\n> ")
                                datetime.datetime.strptime(work_date, "%Y-%m")
                                work_year, work_month = work_date.split("-")
                                print(f"{Bcolors.OKBLUE}Updating your note...{Bcolors.ENDC}")
                                break
                            except ValueError:
                                print(f"{Bcolors.FAIL}Invalid Input{Bcolors.ENDC}")
                                continue
                        work_note = SN.get_note(EXPENSES_ID)[0]["content"]
                        write_expenses(work_note, month=work_month, year=work_year)
                        break
                    elif which_note == "2":
                        while True:
                            try:
                                work_date = input("Which Month and year would you like to update? (YYYY-MM)\n> ")
                                datetime.datetime.strptime(work_date, "%Y-%m")
                                work_year, work_month = work_date.split("-")
                                print(f"{Bcolors.OKBLUE}Updating your note...{Bcolors.ENDC}")
                                break
                            except ValueError:
                                print(f"{Bcolors.FAIL}Invalid Input{Bcolors.ENDC}")
                                continue
                        work_note = SN.get_note(IDEAS_ID)[0]["content"]
                        write_ideas(work_note, month=work_month, year=work_year)
                        break
                    else:
                        break
            else:
                pass

        elif first_input == "4":  # Exit the app
            raise KeyboardInterrupt


def write_main():
    global TODAY
    final_message = ""
    messages_pieces = []

    # ------------------------------------- Get events ---------------------------------------- #
    print(f"\n{Bcolors.BOLD}Checking for events...{Bcolors.ENDC}")
    to_write_events, to_write_upcoming = get_events()
    time.sleep(1)

    # Get chores
    print(f"\n{Bcolors.BOLD}Checking for chores...{Bcolors.ENDC}")
    to_write_chores = get_chores()

    input(f"\n{Bcolors.BOLD}Enter anything to continue.{Bcolors.ENDC}")

    # Get tasks
    print(f"\n{Bcolors.BOLD}These are your stored tasks:{Bcolors.ENDC}")
    to_write_tasks = get_tasks()
    time.sleep(1)

    # Get Research
    print(f"\n{Bcolors.BOLD}These are your stored researches:{Bcolors.ENDC}")
    to_write_researches = get_researches()
    time.sleep(1)

    # Journal entry construction ------------------------------------------------------------
    header = write_title(TODAY.strftime('%d %B %Y, %A'))
    messages_pieces.append(header)

    if to_write_events or to_write_upcoming:
        messages_pieces.append(write_today_events(to_write_events, to_write_upcoming))

    if to_write_chores:
        messages_pieces.append(write_today_chores(to_write_chores))

    messages_pieces.append(write_tasks(to_write_tasks))

    if to_write_researches:
        researches_piece = ""
        for index, research in enumerate(to_write_researches):
            researches_piece += research
            if index < len(to_write_researches) - 1:
                researches_piece += "\n\n----------\n\n"
        messages_pieces.append(researches_piece)

    messages_pieces.append(EXTRA_MESSAGE)

    for message in messages_pieces:
        final_message += f"{message}\n\n----------\n\n"

    return final_message


def get_events(only_print_upcoming: bool = False):
    """Return two arrays, containing today's events and the upcoming events.
     If only_print_upcoming is True, only print the upcoming events, returning None."""
    if not only_print_upcoming:
        print(f"Events will be displayed like this:\n"
              f"Due today: {Bcolors.OKGREEN}+++ event {Bcolors.ENDC}\n"
              f"Updated: {Bcolors.OKBLUE}>>> event {Bcolors.ENDC}\n"
              f"Deleted: {Bcolors.FAIL}XXX event {Bcolors.ENDC}\n")
    todays_events = []
    docs = {}  # {Number of days missing: array of upcoming events' messages}
    missing_days = []  # Used to sort the upcomings' messages

    found_events = list(DB["events"].find({}))
    for doc in found_events:
        try:
            events_date = datetime.date.fromisoformat(doc["date"])
        except ValueError:
            print(f"\n{Bcolors.FAIL}ERROR: wrong formatting.\n"
                  f"Bad entry: {doc}\n\n"
                  f"This is your entry's date: {doc['date']}.{Bcolors.ENDC}")
            if input(
                    f"{Bcolors.WARNING}If you leave the date like this, the entry will be deleted.{Bcolors.ENDC}\n"
                    "Would you like to fix it? (y/n)\n> ") != "y":
                DB["events"].delete_one(doc)
                print(f"{Bcolors.FAIL}Entry deleted.{Bcolors.ENDC}\n")
                continue
            else:
                new_date = input("Use the format YYYY-MM-DD. New date: ")
                DB["events"].update_one(doc, {"$set": {"date": new_date}})
                print(f"{Bcolors.OKGREEN}Entry updated.{Bcolors.ENDC}\n")
                doc["date"] = new_date
                found_events.append(doc)
                continue

        days_to_event = (events_date - TODAY).days

        while True:
            # Get upcoming events ----------------------------------------------------------------
            if 10 >= days_to_event > 0:
                missing_days_message = f"in {days_to_event} days" if days_to_event != 1 else "tomorrow"
                if days_to_event not in missing_days:
                    missing_days.append(days_to_event)
                try:
                    docs[days_to_event].append(f"{doc['date']} ({missing_days_message}) - {doc['event']}")
                    break
                except KeyError:
                    docs[days_to_event] = [f"{doc['date']} ({missing_days_message}) - {doc['event']}"]
                    break

            # Get today's events and update the database -----------------------------------------
            elif days_to_event == 0:
                if not only_print_upcoming:
                    print(f"{Bcolors.OKGREEN}+++ '{doc['event']}'{Bcolors.ENDC}")
                    todays_events.append(f"{doc['event']}")
                    break
                else:
                    break

            elif days_to_event < 0:
                if not only_print_upcoming:
                    try:
                        repeating_quantity, repeating_measure = doc["repeats every"].split(" ")
                    except ValueError:  # Invalid input or missing repetition data
                        repeating_quantity, repeating_measure = "", ""

                    while (events_date - TODAY).days < 0:
                        # Process years increment
                        if "year" in repeating_measure:
                            new_year = events_date.year + int(repeating_quantity)
                            try:
                                events_date = events_date.replace(year=new_year)
                            except ValueError:  # (ex. 28 feb => 29 feb and viceversa)
                                last_day = monthrange(new_year, events_date.month)[1]
                                events_date = events_date.replace(year=new_year, day=last_day)

                        # Process months increment
                        elif "month" in repeating_measure:
                            months_sum = events_date.month + int(repeating_quantity)
                            new_year = events_date.year
                            if months_sum > 12:
                                years_to_add = months_sum // 12
                                months_sum -= 12 * years_to_add
                                new_year += years_to_add
                            try:
                                if events_date.day == monthrange(events_date.year, events_date.month)[1]:
                                    # Keep using last day of the month (ex. 31 May => 30 June)
                                    last_day = monthrange(new_year, months_sum)[1]
                                    events_date = events_date.replace(year=new_year, month=months_sum, day=last_day)
                                else:
                                    # Simple update
                                    events_date = events_date.replace(year=new_year, month=months_sum)

                            except ValueError:  # When the given day isn't in next month's range (ex. 30 May => 30 Feb)
                                last_day = monthrange(new_year, months_sum)[1]
                                events_date = events_date.replace(year=new_year, month=months_sum, day=last_day)
                                print(f"{Bcolors.WARNING}MONTH ERROR: '{doc['event']}': DATE UPDATED TO NEAREST DAY\n"
                                      f"from {events_date.year}-{events_date.month}-{events_date.day} to "
                                      f"{events_date.year}-{events_date.month}-{last_day}{Bcolors.ENDC}")

                        # Process days increments
                        elif "day" in repeating_measure:
                            events_date = events_date + datetime.timedelta(days=int(repeating_quantity))

                        # Delete event
                        else:
                            events_date = None
                            break

                    if events_date:
                        DB['events'].update_one({"event": doc["event"]}, {"$set": {"date": events_date.isoformat()}})
                        print(
                            f"{Bcolors.OKBLUE}>>> '{doc['event']}' updated to {events_date.isoformat()}{Bcolors.ENDC}")
                        days_to_event = (events_date - TODAY).days
                    else:
                        DB['events'].delete_one({"event": doc["event"]})
                        print(f"{Bcolors.FAIL}XXX '{doc['event']}' deleted, no repetition found.{Bcolors.ENDC}")
                        break
                else:
                    break
            else:
                break

    missing_days.sort()

    if missing_days:
        print(f"{Bcolors.OKBLUE} \nThese are your upcoming events! {Bcolors.ENDC}")
    else:
        print(f"{Bcolors.OKBLUE}\n--- No upcoming events in the next 10 days.{Bcolors.ENDC}")

    ordered_upcoming = []
    for day in missing_days:
        for message in docs[day]:
            print(f"--- {message}")
            if not only_print_upcoming:
                ordered_upcoming.append(message)

    if not only_print_upcoming:
        return todays_events, ordered_upcoming
    else:
        input("\nEnter anything to continue.")


def get_chores():
    print(f""
          f"Chores will be displayed like this:\n"
          f"Due today: {Bcolors.OKGREEN}+++ chore {Bcolors.ENDC}\n"
          f"Updated: {Bcolors.OKBLUE}>>> chore {Bcolors.ENDC}\n"
          f"Deleted: {Bcolors.FAIL}XXX chore {Bcolors.ENDC}\n")

    chores = []

    found_chores = DB["chores"].find({})
    for doc in found_chores:
        if doc["next occurrence"]:
            try:
                events_date = datetime.date.fromisoformat(doc["next occurrence"])
            except ValueError:
                print(f"\n{Bcolors.FAIL}ERROR: wrong formatting.\n"
                      f"Bad entry: {doc}\n\n"
                      f"This is your entry's date: {doc['next occurrence']}.{Bcolors.ENDC}")
                if input(
                        f"{Bcolors.WARNING}If you leave the date like this, the entry will be deleted.{Bcolors.ENDC}\n"
                        "Would you like to fix it? (y/n)\n> ") != "y":
                    DB["chores"].delete_one(doc)
                    print(f"{Bcolors.FAIL}Entry deleted.{Bcolors.ENDC}")
                    continue
                else:
                    new_date = input("Use the format YYYY-MM-DD. New date: ")
                    DB["chores"].update_one(doc, {"$set": {"date": new_date}})
                    print(f"{Bcolors.OKGREEN}Entry updated.{Bcolors.ENDC}\n")
                    doc["next occurrence"] = new_date
                    found_chores.append(doc)
                    continue
        else:
            events_date = TODAY

        while True:
            if TODAY - events_date == datetime.timedelta(0):
                print(f"{Bcolors.OKGREEN}+++ {doc['chore']}{Bcolors.ENDC}")
                chores.append(f"{doc['chore']}")
                break

            elif TODAY > events_date:
                try:
                    while TODAY > events_date:
                        days = int(doc["repeats every"])
                        events_date = (events_date + datetime.timedelta(days=days))
                    DB['chores'].update_one({"chore": doc["chore"]},
                                            {"$set": {"next occurrence": events_date.isoformat()}})
                    print(f"{Bcolors.OKBLUE}>>> '{doc['chore']}' updated to {events_date.isoformat()}{Bcolors.ENDC}")
                except ValueError:  # Value missing or incorrect type
                    DB["chores"].delete_one({"chore": doc["chore"]})
                    print(f"{Bcolors.FAIL}XXX '{doc['chore']}' deleted, no repetition was found. {Bcolors.ENDC}")
                    break
            else:
                break

    if not chores:
        print(f"{Bcolors.OKBLUE}\n--- No chores today!  o((*^▽^*))o{Bcolors.ENDC}")
    return chores


def get_tasks():
    tasks = []  # For task selection

    for n, doc in enumerate(DB["todo"].find({})):
        print(f"--- {n}. {doc['task']}")
        tasks.append(doc['task'])
    while True:
        choice = input(f"\n{Bcolors.BOLD}"
                       f"Please select the desired tasks' number, separated by a space."
                       f"{Bcolors.ENDC}\n> ")
        if choice:
            try:
                choice = choice.split(" ")
                if len(set(choice)) != len(choice):
                    raise ValueError
                to_write_todo = [f"{tasks[int(index)]}" for index in choice]
                print(f"{Bcolors.OKGREEN}{len(to_write_todo)} tasks selected.{Bcolors.ENDC}")
                return to_write_todo
            except (ValueError, IndexError):
                print(f"{Bcolors.FAIL}Error: invalid input.{Bcolors.ENDC}")
                continue
        else:
            print(f"{Bcolors.OKBLUE}--- Skipped tasks selection.{Bcolors.ENDC}\n")
            break


def get_researches():
    topics = []
    to_write = []
    for n, doc in enumerate(DB["researches"].find({})):
        print(f"--- {n}. {doc['topic']}")
        topics.append(doc)

    while True:
        choice = input(
            f"\n{Bcolors.BOLD}Please select the desired topics' number, separated by a space.{Bcolors.ENDC}\n> ")
        if choice:
            try:
                if len(set(choice)) != len(choice):
                    raise ValueError
                choice = choice.split(" ")
                for index in choice:
                    index = int(index)
                    to_write.append(write_research(topics[index]["topic"],
                                                   topics[index]["description"],
                                                   topics[index]["steps"]))

                print(f"{Bcolors.OKGREEN}{len(to_write)} topics selected.{Bcolors.ENDC}")
                return to_write
            except (ValueError, IndexError):
                print(f"{Bcolors.FAIL}Error: invalid input.{Bcolors.ENDC}\n")
                continue
        else:
            print(f"{Bcolors.OKBLUE}--- Skipped research topic selection.{Bcolors.ENDC}\n")
            break


def main():
    if input("Hello there!\nRead your notes and update the database? (y/n)\n"
             f"{Bcolors.WARNING}Always remember to update before creating a new daily note{Bcolors.ENDC}\n> ") == "y":
        print(f"{Bcolors.OKBLUE}Looking in the notes...{Bcolors.ENDC}")
        try:
            main_note = SN.get_note(MAIN_NOTE_ID)[0]["content"]
            wishlist_note = SN.get_note(WISHLIST_ID)[0]["content"]
        except (simplenote.SimplenoteLoginFailed, TypeError):
            print(f"{Bcolors.FAIL}Couldn't connect to Simplenote. Make sure you are connected to the internet.\n")
            if input("Would you like to also set again your log-in credentials? (y/n)\n> ") == "y":
                get_simplenote()
            print(f"{Bcolors.OKGREEN}Please restart the app to try again.{Bcolors.ENDC}")
            sys.exit(0)

        read_and_update(main_note)
        if check_wishlist(wishlist_note):
            write_wishlist(wishlist_note)
        get_new_entries(main_note)
        SN.update_note({"key": MAIN_NOTE_ID,
                        "content": "Seems that you have updated your notes!\n\n"
                                   "The auto-bujo automatically deletes your main note when that happens: "
                                   "this way you can be sure that you won't be creating duplicates "
                                   "in your database!\n\n"
                                   "This note will be again populated with your template whenever you create a new "
                                   "main note!\n\n"
                                   "But you can still add entries: all of this document is a \"Writing zone\" (∩´∀｀)∩ ",
                        'systemTags': ['markdown']
                        })

    get_operation()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'{Bcolors.OKBLUE}\n\nHave a great day, Good bye! :){Bcolors.ENDC}')
        try:
            DB.client.close()
            sys.exit(0)
        except SystemExit:
            DB.client.close()
            os._exit(0)
