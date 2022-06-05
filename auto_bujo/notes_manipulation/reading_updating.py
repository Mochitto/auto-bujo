import re

from auto_bujo.utilities.db_collections import db_collections
from auto_bujo.utilities.terminal_colors import Bcolors
from auto_bujo.config import DB, SN, SAVE_STEPS, NOTES_ID, WISHLIST_ID, EXPENSES_ID, \
    IDEAS_ID
from auto_bujo.notes_manipulation.writing import write_notes, write_ideas, write_expenses, write_wishlist


def find_and_format(collection, note: str):
    """Look for matches depending on the collecton's regex, from the given note.
    Format the entries for that collection so that they can be put in the database without further manipulation."""
    entries = []
    regex = db_collections[collection]["regex"]["item"]
    parameters = db_collections[collection]["parameters"]

    for match in re.findall(regex, note):
        new_entry = {}

        if collection == "researches":
            match = [match[0], match[1], match[2]]
            if match[2]:
                match[2] = [{"completed": False, "task": task} for task in match[2].split(", ")]

        for index, parameter in enumerate(parameters):
            try:
                new_entry[parameter] = match[index]
            except IndexError:
                new_entry[parameter] = ""
        entries.append(new_entry)

    return entries


def get_new_entries(note):
    """Get all the collections' (apart from to do) new entires and put them in the database."""
    for collection in db_collections.keys():
        if collection != "todo":
            entries = find_and_format(collection, note)
            print(f"{Bcolors.BOLD}--- New entries for \"{collection}\": {Bcolors.ENDC}{len(entries)}")
            try:
                result = DB[collection].insert_many(entries, ordered=True).acknowledged
                if result:
                    print(
                        f"{Bcolors.OKGREEN}The new entries for \"{collection}\" have been saved in the DB!{Bcolors.ENDC}")
                    if collection == "notes":
                        print(f"{Bcolors.OKBLUE}Getting your diary...{Bcolors.ENDC}")
                        get_note = SN.get_note(NOTES_ID)
                        note_to_read = get_note[0]["content"]
                        write_notes(note=note_to_read)
                    elif collection == "ideas":
                        print(f"{Bcolors.OKBLUE}Getting your ideas...{Bcolors.ENDC}")
                        get_note = SN.get_note(IDEAS_ID)
                        note_to_read = get_note[0]["content"]
                        write_ideas(note_to_read)
                    elif collection == "expenses":
                        print(f"{Bcolors.OKBLUE}Getting your expenses...{Bcolors.ENDC}")
                        get_note = SN.get_note(EXPENSES_ID)
                        note_to_read = get_note[0]["content"]
                        write_expenses(note_to_read)
                    elif collection == "wishlist":
                        print(f"{Bcolors.OKBLUE}Getting your expenses...{Bcolors.ENDC}")
                        get_note = SN.get_note(WISHLIST_ID)
                        note_to_read = get_note[0]["content"]
                        write_wishlist(note_to_read)

            except TypeError:
                pass


def read_and_update(note):
    """Get matches from the todos and researches regexes and update the respective collections."""
    # check todos
    tasks_regex = db_collections["todo"]["regex"]["item"]
    todo_group_regex = db_collections["todo"]["regex"]["group"]
    todo_group = re.findall(todo_group_regex, note)
    if todo_group:
        todo_matches = re.findall(tasks_regex, todo_group[0])
    else:
        return

    for box, task in todo_matches:
        if box == "[x]" or box == "[X]":
            DB["todo"].delete_one({"task": task})
            print(f"{Bcolors.OKGREEN}Task Completed! \"{task}\"{Bcolors.ENDC}")
        else:
            if not DB["todo"].find_one({"task": task}):
                DB["todo"].insert_one({"task": task})
                print(f"{Bcolors.OKGREEN}New task added! \"{task}\"{Bcolors.ENDC}")

    # check researches
    completed_researches = False
    researches_to_update = []
    tasks_regex = db_collections["todo"]["regex"]["item"]
    research_group_regex = db_collections["researches"]["regex"]["group"]
    research_groups = re.findall(research_group_regex, note)
    for topic, research_completed, description, steps_group in research_groups:
        db_match = {"topic": topic}
        if research_completed == "[ ]":
            to_update = {
                "topics": topic,
                "description": description,
                "steps": [{"completed": box != "[ ]", "task": task} for box, task in
                          re.findall(tasks_regex, steps_group)]
            }
            researches_to_update.append((db_match, to_update))
        else:
            print(f"{Bcolors.OKGREEN}Research on \"{topic}\" completed!!{Bcolors.ENDC}")
            if input(f"{Bcolors.BOLD}Would you like to add a link to your research' note? (y/n){Bcolors.ENDC}") == "y":
                hyperlink = input("The note's internal link (complete, with the note's name in square brackets):\n> ")
                hyperlink = f"\n**This is where I've collected my thoughts! :** {hyperlink}"
            else:
                hyperlink = ""
            if SAVE_STEPS:
                note_steps = [task for box, task in re.findall(tasks_regex, steps_group)]
                if note_steps:
                    steps_message = "\n**steps:** \n - "
                    if len(note_steps) > 1:
                        steps_message += "\n - ".join(note_steps)
                    else:
                        steps_message += note_steps[0]
                else:
                    steps_message = ""
            else:
                steps_message = ""
            description_message = ""
            if description:
                description_message = "\n**description:** {description}"
            note_body = f"\n**topic:** {topic}{description_message}{hyperlink}{steps_message}"
            DB["notes"].insert_one({"title": "Research completed", "body": note_body})
            DB["researches"].delete_one(db_match)
            completed_researches = True
    for match, data in researches_to_update:
        print(f"{Bcolors.BOLD}This/these research/es will be updated!{Bcolors.ENDC}")
        DB["researches"].update_one(match, {"$set": data})
    if completed_researches:
        diary = SN.get_note(NOTES_ID)[0]["content"]
        write_notes(diary)


def check_wishlist(note):
    """Delete bought items from wishlist"""
    regex = r"-\s*(\[[xX ]\])\s*.*?\|\s*(.*?)\s*(\(.+\))?\s*\n"
    del_count = 0
    for box, match, trash in re.findall(regex, note):
        if box != "[ ]":
            deleted = DB["wishlist"].delete_one({"item": f"{match}"})
            del_count += deleted.deleted_count
    if del_count:
        print(f"{Bcolors.OKGREEN}Deleted {del_count} entry(s) from wishlist!{Bcolors.ENDC}")
        return True
