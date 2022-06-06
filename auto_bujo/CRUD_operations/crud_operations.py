import datetime
from pprint import pprint
import re

from auto_bujo.utilities.terminal_colors import Bcolors
from auto_bujo.utilities.db_collections import db_collections
from auto_bujo.config import DB


def crud_operations():
    """Handle to execute CRUD operations from the app."""
    matching_value_message = f"{Bcolors.BOLD}Enter the value to match{Bcolors.ENDC}\n> "

    def create_entry(collection):
        while True:
            print(f"\n{Bcolors.WARNING}Please follow the instructions (given when needed) to avoid corruptions.\n"
                  f"You will be told if the entry is not valid and asked to try again.{Bcolors.ENDC}\n")

            while True:
                values_to_add = []
                for index, parameter in enumerate(db_collections[collection]["parameters"]):
                    guide = db_collections[collection]["guide"][index]
                    guide_message = f" ({guide})" if guide else ""

                    new_value = input(
                        f"{Bcolors.OKBLUE}{parameter.capitalize()}{Bcolors.ENDC}{guide_message}: ")
                    values_to_add.append(new_value)
                try:
                    if collection == "events":
                        # Check date
                        datetime.date.fromisoformat(values_to_add[1])
                        # Check repetition
                        if values_to_add[2]:
                            number, measure = re.findall(r"(\d\d?\s)(days|day|months|month|years|year)", values_to_add[2])
                            if measure in "daysmonthsyears":
                                break
                            else:
                                continue
                        break
                except ValueError:
                    print(f"{Bcolors.FAIL}Error: bad formatting, try again:{Bcolors.ENDC}\n"
                          f"\"{values_to_add[1]}\" doesn't follow the format 'YYYY-MM-DD' \n"
                          f"or \"{values_to_add[2]}\" doesn't follow the format 'X day(s)|month(s)|year(s)'\n\n")
                    continue

                try:
                    if collection == "expenses" or collection == "wishlist":
                        # Check price
                        float(values_to_add[0])
                        break
                except ValueError:
                    print(f"{Bcolors.FAIL}Error: bad formatting, try again:{Bcolors.ENDC}\n"
                          f"\"{values_to_add[0]}\" can't be converted to a float or an integer, "
                          f"make sure you are only using a number, without currency.")
                    continue

                break

            print(f"\n{Bcolors.WARNING}You will add a new entry with the following values:{Bcolors.ENDC}")
            for index, parameter in enumerate(db_collections[collection]["parameters"]):
                print(f"{parameter.capitalize()}: {values_to_add[index]}")

            if input(f"\n{Bcolors.BOLD}Add this entry to the database? (y/n){Bcolors.ENDC}").lower() == "y":
                DB[collection].insert_one(
                    dict(zip(db_collections[collection]["parameters"], values_to_add)))
                print(f"{Bcolors.OKGREEN}Entry added.{Bcolors.ENDC}\n")
            else:
                print(f"{Bcolors.OKBLUE}Entry discarded.{Bcolors.ENDC}\n")

            if input(f"Would you like to create another entry in {collection}? (y/n)").lower() != "y":
                break

    def read_entries(collection, find_all: bool = True):
        if not find_all:
            match_key = get_matching_key(collection)

            match_value = input(matching_value_message)
            to_find = {match_key: match_value}
        else:
            to_find = {}

        print(f"\n{Bcolors.OKBLUE}Matching entries...{Bcolors.ENDC}")
        found_entries = DB[collection].find(to_find)
        found_entries_list = list(found_entries)
        if len(found_entries_list) != 0:
            for doc in found_entries_list:
                print()
                pprint(doc)
        else:
            print("Nothing was found...")

        if not find_all:
            if input(f"\n{Bcolors.BOLD}Look for other entries in {collection}? (y/n){Bcolors.ENDC}\n> ") == "y":
                read_entries(collection, False)
                return
        else:
            input("\nEnter anything to continue.")

    def update_entry(collection):
        if input("\nWould you like to see all entries in this collection? (y/n)") == "y":
            read_entries(collection, True)
        match_key = get_matching_key(collection)

        match_value = input(matching_value_message)
        new_value = input(f"\n{Bcolors.BOLD}Enter the new value{Bcolors.ENDC}\n> ").capitalize()

        if match_key and match_value and new_value:
            to_find = {match_key: match_value}
            to_update = {match_key: new_value}
            old_entry = DB[collection].find(to_find)
            if len(list(old_entry)):
                DB[collection].update_one(to_find, {"$set": to_update})
                print(f"\n{Bcolors.OKGREEN}Entry updated!{Bcolors.ENDC}")
                for match in DB[collection].find(to_update):
                    print(Bcolors.OKBLUE, end="")
                    pprint(match)
                    print(Bcolors.ENDC)
            else:
                print(f"{Bcolors.WARNING}No entry with (\"{match_key}\": \"{match_value}\") was found...{Bcolors.ENDC}")
        else:
            print(f"{Bcolors.FAIL}"
                  f"Missing input.\n"
                  f"Matching key:{match_value}\n"
                  f"Matching value: {match_value}\n"
                  f"New value: {new_value}"
                  f"{Bcolors.ENDC}\n")

        if input(f"\n{Bcolors.BOLD} Would you like to update another entry in {collection}? (y/n){Bcolors.ENDC}\n"
                 f"> ") == "y":
            update_entry(collection)

    def delete_entries(collection, delete_all: bool = False):
        if delete_all:
            if input(f"{Bcolors.WARNING}"
                     f"Are you sure you want to delete the whole collection? This cannot be undone. (y/n)"
                     f"{Bcolors.ENDC}\n> ") != "y":
                print(f"{Bcolors.OKBLUE}Operation Aborted.{Bcolors.ENDC}")
                return
            else:
                DB[collection].delete_many({})
                print(f"{Bcolors.OKGREEN}Deleted all entries in {collection}.{Bcolors.ENDC}")
        else:
            if input("\nWould you like to see all entries in this collection? (y/n)") == "y":
                read_entries(collection, True)
            match_key = get_matching_key(collection)

            match_value = input(matching_value_message)
            if match_key and match_value:
                matching_entry = DB[collection].find_one({match_key: match_value})
                if matching_entry:
                    print(f"\n{Bcolors.OKBLUE}Deleting this entry:")
                    pprint(matching_entry)

                    DB[collection].delete_one({match_key: match_value})
                    print(f"\n{Bcolors.OKGREEN}Entry deleted!{Bcolors.ENDC}")
                else:
                    print("Entry not found... Nothing was deleted.")

            if input(f"\n{Bcolors.BOLD} Would you like to delete another entry in {collection}? (y/n){Bcolors.ENDC}\n"
                     f"> ") == "y":
                delete_entries(collection, False)

    def get_matching_key(collection):
        print(f"\n{Bcolors.BOLD}Enter the key you would like to match from the following:{Bcolors.ENDC}")
        collections_parameters = db_collections[collection]["parameters"]
        for index, parameter in enumerate(collections_parameters):
            print(f"--- {parameter} ({db_collections[collection]['guide'][index]}).")
        while True:
            user_input = input("> ").lower()
            if user_input in collections_parameters:
                return user_input
            else:
                print(f"{Bcolors.FAIL}Invalid key. Check your input and try again{Bcolors.ENDC}")

    numbers = "0 1 2 3 4 5 6"
    print(f"\n{Bcolors.BOLD}CRUD operations:{Bcolors.ENDC}\n"
          "--- 0. Create\n"
          "--- 1. Read All\n"
          "--- 2. Read One/More\n"
          "--- 3. Update\n"
          "--- 4. Delete One\n"
          "--- 5. Delete Collection\n"
          "--- 6. Go back"
          )

    while True:
        second_input = input("> ")
        if second_input not in numbers:
            print(f"{Bcolors.FAIL}Invalid input. Please use one of the given numbers.{Bcolors.ENDC}")
            continue
        else:
            break

    if second_input == "6":
        return
    else:
        print(f"\n{Bcolors.BOLD}From/to what collection?{Bcolors.ENDC}\n"
              "- todo\n"
              "- events\n"
              "- chores\n"
              "- researches\n"
              "- notes\n"
              "- ideas\n"
              "- expenses\n"
              "- wishlist\n"
              "(default = go back to main menu)")

        while True:  # Input validation ------------------------------------------------ #
            collection_pick = input("> ")

            if not collection_pick:  # default
                return
            elif collection_pick not in db_collections.keys():
                print(f"{Bcolors.FAIL}Collection not in the database.{Bcolors.ENDC}")
                continue
            else:
                break

        # ------------------------------- CRUD OPERATIONS ------------------------------- #
        if second_input == "0":
            create_entry(collection_pick)

        elif second_input == "1" or second_input == "2":
            read_entries(collection_pick, second_input == "1")

        elif second_input == "3":
            update_entry(collection_pick)

        elif second_input == "4" or second_input == "5":
            delete_entries(collection_pick, second_input == "5")

        else:  # Catch unexpected errors ------------------------------------------------- #
            print(f"{Bcolors.FAIL}Something went wrong °.°·(((p(≧□≦)q)))·°.°\n"
                  f"Collection: \"{collection_pick}\", operation's index: \"{second_input}\"{Bcolors.ENDC}\n"
                  f"Please let me know what happened on Github, to make sure this doesn't happen again :)\n"
                  f"--- Twitter: @MochiDeveloper\n")
