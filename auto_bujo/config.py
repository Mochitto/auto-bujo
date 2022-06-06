import configparser
import datetime
import sys
from configparser import ConfigParser
import os

import simplenote
import pymongo
import dotenv

from auto_bujo.utilities.terminal_colors import Bcolors
from auto_bujo.utilities.models import first_welcome_message, templates

config = ConfigParser()


def get_simplenote():
    username = input(f"{Bcolors.OKBLUE}Username:{Bcolors.ENDC} ")
    password = input(f"{Bcolors.OKBLUE}Password:{Bcolors.ENDC} ")

    dotenv.set_key(dotenv.find_dotenv(), key_to_set='SN_USERNAME', value_to_set=username)
    dotenv.set_key(dotenv.find_dotenv(), key_to_set='SN_PASSWORD', value_to_set=password)
    print(f"{Bcolors.OKGREEN}Login informations have been saved!{Bcolors.ENDC}\n")


# First login
def set_credentials(set_credentials: bool = True, create_files: bool = True):
    print(f"{Bcolors.WARNING}Your account informations will be stored locally, in a .env file.{Bcolors.ENDC}\n\n"
          f"{Bcolors.BOLD}Simplenote account:{Bcolors.ENDC} \n")
    while True:
        try:
            if set_credentials:
                get_simplenote()
            if input("Do you already have this app's notes on your Simplenote? (y/n)\n> ") == "y":
                create_files = False
            if create_files:
                print(f"{Bcolors.OKBLUE}Creating your notes' templates...{Bcolors.ENDC}")
                # dotenv.load_dotenv(dotenv.find_dotenv())
                username = dotenv.get_key(dotenv.find_dotenv(), key_to_get="SN_USERNAME")
                password = dotenv.get_key(dotenv.find_dotenv(), key_to_get="SN_PASSWORD")

                sn = simplenote.Simplenote(username=username, password=password)
                for template_key, template in templates.items():
                    add_note = sn.add_note(template)
                    note_key = add_note[0]["key"]
                    dotenv.set_key(dotenv.find_dotenv(), key_to_set=template_key, value_to_set=note_key)
                print(f"{Bcolors.OKGREEN}Creation of your notes completed!{Bcolors.ENDC}\n")
            else:
                print(f"\nPlease enter your notes' id "
                      f"(they can be found in the notes' internal link, "
                      f"which you can get from the note's menu in the top-right corner)\n"
                      f"ex. simplenote://note/{Bcolors.BOLD}e0c42e5d9e584b4187e4600297bee933{Bcolors.ENDC}\n")
                for template_key, template in templates.items():
                    note_key = input(f"{template_key}: ")
                    dotenv.set_key(dotenv.find_dotenv(), key_to_set=template_key, value_to_set=note_key)

            break
        except simplenote.simplenote.SimplenoteLoginFailed:
            print(f"{Bcolors.FAIL}There was a problem connecting to Simplenote.\n"
                  f"Please update your log-in informations and make sure you have a working internet connection."
                  f"{Bcolors.ENDC}\n")
            continue


def configure_settings(first_time: bool = True):
    config.read("config.ini")
    if first_time:
        config.add_section("main")
    # Getting start and end time
    print("\nThe app uses your computer's time to decide if to create a note with today's date or tomorrow's.\n"
          "This is done so that you can use the app in the morning, and have a note for the whole day, "
          "or use it at night, and have your note ready for the following day.\n"
          "You can think of the start time and end time as the interval "
          "in which, if you create a note, it will be for that day.\n"
          "If you create your note outside of that interval, it will be created for the following day.\n")
    while True:
        try:
            start_time = input(
                f"{Bcolors.BOLD}Pick the time at which your day starts (24 hours format, HH:MM):{Bcolors.ENDC}\n> ")
            end_time = input(
                f"{Bcolors.BOLD}Pick the time at which your day end (24 hours format, HH:MM):{Bcolors.ENDC}\n> ")
            start_time_hour = int(start_time.split(":")[0])
            start_time_minutes = int(start_time.split(":")[1])
            end_time_hour = int(end_time.split(":")[0])
            end_time_minutes = int(end_time.split(":")[1])
            datetime.time(hour=start_time_hour, minute=start_time_minutes)
            datetime.time(hour=end_time_hour, minute=end_time_minutes)
            break
        except (ValueError, IndexError):
            print(f"{Bcolors.FAIL}Bad input: make sure you are using the format HH:MM\n"
                  f"! 0 =< hour =< 23; 0 =< minutes =< 59{Bcolors.ENDC}")
            continue
    if first_time:
        config.add_section("time")
    config.set("time", "START_OF_DAY_HOUR", str(start_time_hour))
    config.set("time", "START_OF_DAY_MINUTES", str(start_time_minutes))
    config.set("time", "END_OF_DAY_HOUR", str(end_time_hour))
    config.set("time", "END_OF_DAY_MINUTES", str(end_time_minutes))

    # Get currency
    print("\n\nThe app can also store your expenses.\n"
          "To do so, it needs to know (just for display) what currency you use.\n"
          "Said currency will be put in front (before) the amount of money.\n")
    currency = input(
        f"{Bcolors.BOLD}What is the symbol of the currency you would like to save your expenses with?{Bcolors.ENDC}\n> ")
    config.set("main", "CURRENCY", currency)

    # Get save_steps
    print("\n\nWhen you complete a research (refer to tutorial note), a new entry will be created in \"Your Diary\".\n"
          "It will contain your research' topic, description, ask you if you want to link another note to it "
          "(You can find your notes' internal link in the note's menu) and, "
          "if you wish to, also show all the tasks you have completed before finishing the research.\n")
    if input(
            f"{Bcolors.BOLD}Would you like to save your researches' tasks upon completion? (y/n){Bcolors.ENDC}\n> ") == "y":
        save_steps = "True"
    else:
        save_steps = "False"
    config.set("main", "SAVE_STEPS", save_steps)

    with open('config.ini', 'w') as f:
        config.write(f)

    print(
        f"\n\n{Bcolors.OKGREEN}Configuration completed! Please start the app again to start using it :){Bcolors.ENDC}")


def get_today():
    """Check if the startup time is in the interval between day start and day end, if not change today to tomorrow.
    Return day, day iso and daily welcome message"""
    today = datetime.date.today()
    today_iso = today.isoformat()
    daily_welcome_message = f"Hello! Today is the {today_iso}."

    STARTUP_TIME = datetime.datetime.now()
    START_TIME = datetime.time(hour=config.getint("time", "START_OF_DAY_HOUR"),
                               minute=config.getint("time", "START_OF_DAY_MINUTES"))
    END_TIME = datetime.time(hour=config.getint("time", "END_OF_DAY_HOUR"),
                             minute=config.getint("time", "END_OF_DAY_MINUTES"))

    START_OF_DAY = datetime.datetime.combine(today, START_TIME)
    END_OF_DAY = datetime.datetime.combine(today, END_TIME)

    if not (START_OF_DAY < STARTUP_TIME < END_OF_DAY):
        today = today + datetime.timedelta(days=1)
        today_iso = today.isoformat()
        daily_welcome_message = f"Hello! Tomorrow will be the {today_iso}."

    return today, today_iso, daily_welcome_message


def setup_app():
    with open('.env', 'w'):
        pass
    set_credentials()
    print(f"\n{Bcolors.OKGREEN}Login and files creations completed! {Bcolors.ENDC}\n"
          f"Let's set up the app environment!\n")
    with open('config.ini', 'w'):
        pass
    configure_settings()


try:
    with open('config.ini', 'r'):
        pass
    with open(".env", "r"):
        pass
except FileNotFoundError:
    print(first_welcome_message)
    try:
        setup_app()
        sys.exit(0)
    except KeyboardInterrupt:
        print(f'{Bcolors.OKBLUE}\n\nHave a great day, Good bye! :){Bcolors.ENDC}')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

config.read("config.ini")

# CONSTANTS USED IN THE APP
_sn_username = dotenv.get_key(dotenv.find_dotenv(), "SN_USERNAME")
_sn_password = dotenv.get_key(dotenv.find_dotenv(), "SN_PASSWORD")
try:
    SN = simplenote.Simplenote(_sn_username, _sn_password)
except simplenote.SimplenoteLoginFailed:
    print(f"{Bcolors.FAIL}Couldn't connect to Simplenote. Make sure you are connected to the internet.\n")
    if input("Would you like to set again your log-in credentials? (y/n)\n> ") == "y":
        get_simplenote()
    print(f"{Bcolors.OKGREEN}Please restart the app to try again.{Bcolors.ENDC}")
    sys.exit(0)

client = pymongo.MongoClient(host="127.0.0.1", port=27017)

DB = client["routineDB"]
try:
    TODAY, TODAY_ISO, DAILY_WELCOME_MESSAGE = get_today()
    CURRENCY = config.get("main", "CURRENCY")
    SAVE_STEPS = config.getboolean("main", "SAVE_STEPS")

    MAIN_NOTE_ID = dotenv.get_key(dotenv.find_dotenv(), "SN_MAIN")
    NOTES_ID = dotenv.get_key(dotenv.find_dotenv(), "SN_NOTES")
    IDEAS_ID = dotenv.get_key(dotenv.find_dotenv(), "SN_IDEAS")
    EXPENSES_ID = dotenv.get_key(dotenv.find_dotenv(), "SN_EXPENSES")
    WISHLIST_ID = dotenv.get_key(dotenv.find_dotenv(), "SN_WISHLIST")
except configparser.NoSectionError:
    print(f"{Bcolors.FAIL}There was an error getting your settings. Please set up the app again.{Bcolors.ENDC}")
    try:
        set_credentials(create_files=False)
        configure_settings()
        sys.exit(0)
    except KeyboardInterrupt:
        print(f'{Bcolors.OKBLUE}\n\nHave a great day, Good bye! :){Bcolors.ENDC}')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
