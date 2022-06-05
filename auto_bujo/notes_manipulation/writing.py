import datetime
import re

import bson
from auto_bujo.utilities.terminal_colors import Bcolors
from auto_bujo.config import CURRENCY, TODAY, DB, SN, NOTES_ID, IDEAS_ID, WISHLIST_ID, EXPENSES_ID


# Writing the main note
def write_title(date):
    return f"# {date} - Have a nice day! (*・ω・)ﾉ  ♥"


def write_today_events(events: list, upcoming: list):
    message = ""
    if events:
        message += "## ( ` ω ´ ) !! Today's events !!\n"
        for event in events:
            message += f"- {event}\n"
    if upcoming:
        message += "#### Upcoming events\n" if events else "## (・ω・) Upcoming events\n"
        for index, event in enumerate(upcoming):
            message += f"- {event}"
            message += "\n" if index < len(upcoming) - 1 else ""

    return message


def write_today_chores(chores: list):
    message = ""
    if chores:
        message = "## (￣ ﹌ ￣) Today's chores \n"
        for index, chore in enumerate(chores):
            message += f"- {chore}"
            message += "\n" if index < len(chores) - 1 else ""

    return message


def write_tasks(tasks: list):
    message = "##  ヾ(=`ω´=)ノ” Your tasks \n"
    if tasks:
        for index, task in enumerate(tasks):
            message += f"- [ ] {task}"
            message += "\n" if index < len(tasks) - 1 else ""
    else:
        message += "\n\n"

    return message


def write_research(topic, description, steps):
    message = ""
    if topic:
        message = f"##  (⌐0_0) Research on: {topic}\n"
        message += "- [ ] Research completed!\n^ This will complete the research, deleting it from the database and writing " \
                   "a note about your achievement!\n\n"
        message += f"#### --- Description ---\n "
        if description:
            message += f"_{description}_\n"
        else:
            message += "\n\n"
        message += f"#### --- Steps ---\n"
        if steps:
            for index, task in enumerate(steps):
                if task["completed"]:
                    message += "- [X] " + task['task']
                    message += "\n" if index < len(steps) - 1 else ""
                else:
                    message += "- [ ] " + task['task']
                    message += "\n" if index < len(steps) - 1 else ""
        else:
            message += "\n\n"

    return message


EXTRA_MESSAGE = "## ٩(ˊᗜˋ*) Writing zone! \n\n"


# updating the secondary notes
def write_ideas(note, month=datetime.date.today().strftime("%B"), year=datetime.date.today().strftime("%Y")):
    regex = rf"(\#\#\s*{month} {year}[\s\S]*?)-[\s\S]*?\n(\*\*\*\*\*\*\*\*\*\*)"
    # matches template, leaving out the expenses and total, for substitution

    while not re.findall(regex, note):
        note += f"\n## {month} {year}\n\n**********\n\n- placeholder\n\n**********"

    range_start = datetime.datetime.strptime(f"01 {month} {year}", "%d %B %Y").replace(tzinfo=datetime.timezone.utc)

    new_month = range_start.month + 1
    new_year = range_start.year
    if new_month > 12:
        new_month = 1
        new_year += 1
    range_end = range_start.replace(month=new_month, year=new_year)

    range_start = bson.ObjectId.from_datetime(range_start)
    range_end = bson.ObjectId.from_datetime(range_end)

    db_find = DB["ideas"].find({"_id": {"$gte": range_start, "$lt": range_end}})

    new_note = ""
    for entry in db_find:
        description = f"{entry['description']} \n" if entry['description'] else ""
        new_note += f"- **{entry['concept']}** \n{description}\n\n----------\n\n"

    message = re.sub(regex, f"\\1{new_note}\\2", note)
    SN.update_note({"key": IDEAS_ID, "content": message, "systemtags": ["markdown"]})
    print(f"{Bcolors.OKGREEN}Your ideas have been updated!{Bcolors.ENDC}\n")


def write_notes(note, date: str = datetime.date.today().strftime("%A, %d %B %Y")):
    regex = rf"(\#\#\#\s*{date}[\s\S]*?\n)-[\s\S]*?\n(\s*----------)"
    while not re.findall(regex, note):
        note += f"\n\n### {date} \n\n- placeholder\n\n----------"

    range_start = datetime.datetime.strptime(date, "%A, %d %B %Y").replace(tzinfo=datetime.timezone.utc)
    range_end = range_start + datetime.timedelta(days=1)
    range_start = bson.ObjectId.from_datetime(range_start)
    range_end = bson.ObjectId.from_datetime(range_end)
    diary_notes = DB["notes"].find({"_id": {"$gte": range_start, "$lt": range_end}})
    message = ""
    for doc in diary_notes:
        # note.replace("\n", "\n    ") # uncomment if \n breaks the -
        title = f"**{doc['title']}:** " if doc['title'] else ""
        message += f"- {title}{doc['body']}\n\n"
    new_note = re.sub(regex, f"\\1{message} \\2", note)
    SN.update_note({"key": NOTES_ID, "content": new_note, "systemtags": ["markdown"]})
    print(f"{Bcolors.OKGREEN}Your diary has been updated!{Bcolors.ENDC}\n")


def write_expenses(note, month=datetime.date.today().strftime("%B"), year=datetime.date.today().strftime("%Y")):
    """Check if there is an entry for the given month/year's expenses. If not, create it. Find entries in the db
    that match the desired period of time and populate the template."""
    regex = rf"(##\s*{month}\s*{year}\s*)-\s*.*?\s*\d+[\s\S]+?(\s###\s*Total:\s*.*?)\d+(\s*?----------)"
    # matches template, leaving out the expenses and total, for substitution

    while not re.findall(regex, note):
        note += f"\n## {month} {year}\n\n- 0 placeholder\n\n### Total: {CURRENCY}0000\n\n----------"

    range_start = datetime.datetime.strptime(f"01 {month} {year}", "%d %B %Y").replace(tzinfo=datetime.timezone.utc)

    new_month = range_start.month + 1
    new_year = range_start.year
    if new_month > 12:
        new_month = 1
        new_year += 1
    range_end = range_start.replace(month=new_month, year=new_year)

    range_start = bson.ObjectId.from_datetime(range_start)
    range_end = bson.ObjectId.from_datetime(range_end)

    db_find = DB["expenses"].find({"_id": {"$gte": range_start, "$lt": range_end}})

    new_expenses = ""
    total_spent = 0
    for entry in db_find:
        price = f"- {CURRENCY} {entry['cost']}".ljust(16, "_")
        place = f"(from {entry['place']})" if entry["place"] else ""
        item = f"{entry['object bought']} {place}".ljust(40)
        new_expenses += f"{price} | {entry['_id'].generation_time.strftime('%Y-%m-%d')} | {item}\n"
        total_spent += round(float(entry['cost']))

    new_expenses = re.sub(regex, f"\\1{new_expenses} \\2 {total_spent} \\3", note)
    SN.update_note({"key": EXPENSES_ID, "content": new_expenses, "systemtags": ["markdown"]})
    print(f"{Bcolors.OKGREEN}Your expenses has been updated!{Bcolors.ENDC}\n")


def write_wishlist(note):
    for need in range(10):
        regex = r"(\#{3} ✧･ﾟ: \*✧･ﾟ:\*  high_range  \*:･ﾟ✧\*:･ﾟ✧[\s\S]*?)[\s\S]*?(-{10}\s*\#{3} ✧･ﾟ: \*✧･ﾟ:\*  low_range  \*:･ﾟ✧\*:･ﾟ✧[\s\S]*?)"
        need += 1
        items = DB["wishlist"].find({"level of need": f"{need}"})

        regex = regex.replace("high_range", f"{need}")
        regex = regex.replace("low_range", f"{need - 1}")

        group = "\n\n"
        for entry in items:
            price = f"- [ ] {CURRENCY} {entry['price']}".ljust(13)
            place = f"(from {entry['place']})" if entry["place"] else ""
            item = f"{entry['item']} {place}".ljust(40)
            final_entry = f"{price} | {item}\n"
            group += final_entry
        group += "\n"

        note = re.sub(regex, f"\\1{group}\\2", note)

    SN.update_note({"key": WISHLIST_ID, "content": note, "systemtags": ["markdown"]})
    print(f"{Bcolors.OKGREEN}Your wishlist has been updated!{Bcolors.ENDC}\n")



