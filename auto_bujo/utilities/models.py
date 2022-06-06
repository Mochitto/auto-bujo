from auto_bujo.utilities.terminal_colors import Bcolors


# creating the secondary documents
NOTES_TEMPLATE = "# Your diary:\n----------\n"
IDEAS_TEMPLATE = "# Your ideas:\n----------\n"
EXPENSES_TEMPLATE = "# Your expenses:\n----------\n"
WISHLIST_TEMPLATE = "# Your wishlist:\n\n----------\n"
for n in range(10, -1, -1):
    post_message = "\n\n\n----------\n" if n != 0 else ""
    WISHLIST_TEMPLATE += f"### ✧･ﾟ: *✧･ﾟ:*  {n}  *:･ﾟ✧*:･ﾟ✧{post_message}"


TUTORIAL_TEMPLATE = r"""
# Welcome to auto-bujo!  (*・ω・)ﾉ  ♥

------------
The aim of this project is to let people organise their days with the least amount of effort and time.

When creating this app, I've been inspired by bullet-journals. 
The main functionality is the same: letting the user "dump" different kind of entries in one place, but with a core difference.
Unlike the traditional, paper-based bujos, the need of taking your time to put those entries in the right place is taken away.

The main note (which gets read and changed on every app-use) has five "zones": events, chores, tasks, researches and a writing zone.
Some of those can also be missing, if there are no entires to populate them on that specific day.

------------

# Usage 

------------

TL;DR: 
Please read the "Writing zone" section to understand how to use the app to automatically update the database.
You can directly add tasks to your daily tasks and your researches' steps to add them to the database.

You can check checkboxes in "Your wishlist" to delete them from the list.

**Warning:** Directly modifying the text in the secondary notes (Your diary, Your expenses, Your ideas, Your wishlist) is not safe.
Your direct modifications might get deleted if any of the entries in the same group (same day, for "Your diary", or same month, for "your expenses" and "your ideas") gets updated, forcing a re-write.
This can happen both automatically, when adding a new entry, or when updating entries. 
To modify entries in a safe way, you should update the specific entries you would like to change from the "CRUD operations" menu.
If you still modify them directly on the note, make sure to avoid re-writes and always copy your secondary note before updating an entry that could cause your modifications to get lost.

Enjoy! :)

------------

------------

# The main note

-----------
## Events

This zone is dedicated to events, such as appointments, deadlines, exams, birthdays and everything that occours on a specific date and might repeat at regular intervals.

This zone gets populated with events that are due and upcoming events (up to 10 days from the current date).

If the due events are set up to repeat themselves (in days, months or years), their countdown will be updated, otherwise the event will be considered completed and get deleted when the note is updated.

-----------
Example:


## ( ` ω ´ ) !! Today's events !! 
- Maths exams, 2:00 PM, West Building
- John's birthday!
#### Upcoming events
- 2022-05-31 Pay rent ( in 3 days)
- 2022-06-02 Eye examination, 3:15 PM ( in 5 days)


-----------
## Chores

This zone is similar to "events": it is used to remind you of chores that happen regularly, such as cleaning your room or buying groceries.

Unlike "events",  you will only see the chores that are due, not those that are upcoming.

They can also lack repetition and be one-time tasks, getting deleted when they are due.

------------
Example:

## (￣ ﹌ ￣) Today's chores 
- Clean your bedroom
- Laundry


------------
## Tasks

This zone is dedicated to general tasks, that could be put in a todo-list.
When you start the app and update the main note, you will be asked which tasks to put in this zone (taken from the batabase).

The tasks that get checked in this zone will be automatically removed from the database, as they are considered completed.

In this particular zone, creating tasks is as easy as just adding one to the list: when the note gets read, they will be automatically put in the database, ready to be chosen.

-----------
Example:

##  ヾ(=`ω´=)ノ” Your tasks: 
- [ ] something     
- [ ] something else    < These two notes were picked from the database
- [x] go do this      < This note will be deleted on the next update
- [ ] go do that      < This note has been added


-----------
## Researches

This zone is dedicated to your researches. Those can also be used as to-do Lists.

A research is composed by a topic, a completion button, a description and a to-do list (named "Steps",  as in steps missing to complete your research).
Only the topic is mandatory: the description and to-do list can be left empty and are for user's reference.

Researches get read in a similar way as the "Tasks" zone, meaning that modifications (changing or adding the description, adding tasks to "steps") get automatically put in the database.
Steps do not get deleted when you complete them, but their status does get stored.

The completion button is used to mark the research as complete: this will delete it from the researches database and create a note in your diary with all of the information from it (topic, description and steps).

You can have more than one research on your main note.

-----------
Example:

##  (⌐0_0) Research on: Linux
- [ ] Research completed!

#### --- Description ---
 _Linux seems pretty cool, but I do not know how it works or how to use it..._

#### --- Steps ---
- [x] Read [this article](https://opensource.com/resources/linux)
- [ ] Install linux
- [ ] Learn basic [shell commands](https://ubuntu.com/tutorials/command-line-for-beginners#3-opening-a-terminal) 


-----------
## Writing zone and creating new entries

This zone is dedicated to creating new entries.
From here, using specific formatting, you can create entries that get put in the database and in the other notes.

Entries are usually composed like this: "- [entry_group] field1 | field2 | field3 | field4 |"
Depending on the entry group, there can be two or four diffrent fields.

Entry groups can be capitalized or lowercase.

**! Please follow the given instructions. If there are formatting mistakes in the entries, they might be ignored.

When there is a ? next to a field, it means it can be left empty, but it's still necessary to add | in its place, as if the field was present, to make sure the entry gets saved. !**



These are the examples:


#### Adding an event entry:
- event: event text | date: (YYYY-MM-DD) | repetition: (X day(s)/month(s)/year(s) ) ? |

Example:
- Event: Mariko's Birthday! | 2022-03-14 | 1 year |
- Event: Graduation ceremony, 9:00 AM  | 2022-05-20 | | 


#### Adding a chore:
- chore: chore text |  next occurrence: (YYYY-MM-DD) ? | repetition in days: (X) ? | 
Note: if next occurrence is left empty, it will defaut to the day you create a new note in.

Example:
- chore: vacuum the floor |  2022-06-02 | 2 |
- Chore: buy a cake for the party | 2022-07-01 | |


#### Adding a research:
- research: research topic | description ? | steps: (divided by commas) ? |

Example:
- research: Linux | | |
- Research: Hand stretches | I've learnt that they are very important to avoid RSI! | find good videos, get notes on the best exercises,  get used to doing them | 


#### Adding a diary entry:
- note: title? | body | 

Example: 
- Note: Picnic | I've had a lovely picnic today! |
- note: | Today I don't feel like working -_- |


#### Adding an idea:
- idea: concept | description ? |

Example:
- idea: A website that gives you inspiring quotes | |
- idea: AI that can detect squids | that would be kind of cool! |


#### Adding an expense:
- expense: price (number) | item | place ? |

Example:
(with yen)
- Expense: 1200 | teddy bear | |

(with dollars)
- expense: 4000.00 | a frog | a pond |


#### Adding an item to the wishlist:
- wishlist: price | item | place ? | level of need (from 1-10) |

Example:
- wishlist: 7000.00 | another frog | | 10 |
- wishlist: 2000 | a t-shirt with a frog on it | Shinjuku | 8 |


------------

# Other notes

-----------

-----------

There are also five other notes that get created when the app starts: the tutorial (this note), your diary (where notes are stored), your ideas (where ideas entries are stored), your wishlist and your expenses.

In this version, the only note that can be modified from simplenote is the wishlist, as in ticking any checkbox will delete the entry. Other modifications will not be read from these files, as they are updated only through database and only when there are changes to it, to avoid long processing times at startup.

This means that, to modify entries, you have to use the "CRUD operations" menu from the app (next chapter)

-----------

## Your diary

This note is used to store your notes and your progresses.
Every time you create a note or complete a research, those will be added to the corresponding day in the diary, if already existing, or get added to a new date, after it gets created.

In this version of the app, this area is write only: direct modifications to this area are not saved in the database, meaning they could get deleted if the specific day in which the note is gets updated by the app.

To make sure modifications are saved, it's necessary to find it in the database and updating it, using the "CRUD operations" menu.
Note: Updating entires from the CRUD operations menu will force an update also on the notes, updating the whole day. 


Note: you can decide if to add the researches' steps to the notes or if to avoid it.

-------------
Example:


### Friday, 03 June 2022

- **A fun day outside**: Today I've had a beautiful picnic at the park!
The sun was very nice and I ate a lot of cookies :)
- A cute frog came to meet us! We gave it a chicken wing >_<

### Saturday, 04 June 2022

- **Research completed!** 
_topic_: Linux
_description_: It seemed pretty complex..! It kinda was...!
_steps that I took to get there_: look it up, install linux, learn the basic commands, get used to the terminal.


----------

## Your ideas

This note is used to store your ideas. I've added it to store my ideas for new apps, but I think it can also be used to store concepts that you want to revise later.

In this version of the app, this area is write only: direct modifications to this area are not saved in the database, meaning they could get deleted if the specific month in which the modified idea is gets updated by the app.

To make sure modifications are saved, it's necessary to find it in the database and updating it, using the "CRUD operations" menu.
Note: Updating entires from the CRUD operations menu will force an update also on the notes, updating the whole month. 

------------
Example:

## June 2022

**********

- **Let my cat pursue world domination** 
if so dangerous, why so cute?? Let them at it!!

-----------

- **Getting all of the achievements in Overcooked!** 

-----------

**********

## July 2022

- **Stop my cat from dominating the world** 
It got out of hand-

------------

## Your Wishlist

This note is used to keep track of the items you would like to buy. They are ordered depending on the "need level".

This note is the only one, apart from the main note, that gets written AND read, meaning that if you check an item, it will automatically delete the entry from the database, showing that you have bought or dismissed the entry.

-----------
Example:

✧･ﾟ: \*✧･ﾟ:\*  10  \*:･ﾟ✧\*:･ﾟ✧

- [ ] ￥3000 | A cat tree for my cat (from Amazon)
- [ ] ￥500 | New matcha tea

-----------

✧･ﾟ: \*✧･ﾟ:\*  9  \*:･ﾟ✧\*:･ﾟ✧

- [ ] ￥ 120000 | A bicycle to get to work

-----------

✧･ﾟ: \*✧･ﾟ:\*  8  \*:･ﾟ✧\*:･ﾟ✧

-----------

## Your expenses

This note is used to keep track of your expenses. It gets automatically updated when new expenses get added.

In this version of the app, this area is write only: direct modifications to this area are not saved in the database, meaning they could get deleted if the specific month gets updated by the database, or a full sync is forced onto the diary from the app. 

------------
Example:

## April 2022

- ￥1500 | 2022-04-10 | A nice meal (from the local restaurant)
- ￥2500 | 2022-04-14 | A new desk lamp (from Amazon)
- ￥200   | 2022-04-10 | A pencil

### Total: ￥4200

------------

------------

# CRUD Operations

------------

This app also gives you an interface to carry out MongoDB CRUD operations.
By selecting "Modify the DB" from the main menu, you can see all of your data stored in the database, just as you would see it from the mongoDB shell.

There is a guide and description on every operation, to help you through creating, updating, reading and deleting (CRUD) your data.

This menu can be useful when you want to update entries, delete something or just review your database.

--------------

--------------

## Thank you

For using this app! This is one of my first projects, but I hope you will find it useful and will help you stay organized!

--------------

### Contacts:

**Twitter:** @MochiDeveloper
**Email:**    mochittodeveloper@gmail.com
"""

MAIN_TEMPLATE = "This will be your daily note"

templates = {"SN_MAIN": MAIN_TEMPLATE,
             "SN_NOTES": NOTES_TEMPLATE,
             "SN_IDEAS": IDEAS_TEMPLATE,
             "SN_EXPENSES": EXPENSES_TEMPLATE,
             "SN_WISHLIST": WISHLIST_TEMPLATE,
             "SN_TUTORIAL": TUTORIAL_TEMPLATE}

# First login messages
mongo_download = "https://www.mongodb.com/docs/manual/administration/install-community/"
mongo_installation = "https://www.youtube.com/watch?v=wcx3f0eUiAw"
simplenote_download = "https://simplenote.com/#available-on-all-your-devices"
simplenote_signup = "https://app.simplenote.com/signup/"

first_welcome_message = f"{Bcolors.BOLD}Welcome to auto-bujo!{Bcolors.ENDC}\n\n" \
                        f"This app is designed to need a " \
                        f"{Bcolors.FAIL}mongoDB server and a Simplenote account{Bcolors.ENDC} " \
                        "to store your information and have your notes in the right place.\n\n" \
                        "MongoDB is used as a local database for your data, while simplenote is a markdown editor and viewer" \
                        " that gives you the possibility to sync your notes across different devices. \n\n" \
                        f"{Bcolors.BOLD}You can download them at these urls:{Bcolors.ENDC}\n" \
                        f"Mongo: {Bcolors.OKBLUE}{mongo_download}{Bcolors.ENDC} \n" \
                        f"For installation, refer to: {Bcolors.OKBLUE}{mongo_installation}{Bcolors.ENDC}\n\n" \
                        f"Simplenote: {Bcolors.OKBLUE}{simplenote_download}{Bcolors.ENDC} \n" \
                        f"Sign-up: {Bcolors.OKBLUE}{simplenote_signup}{Bcolors.ENDC}\n" \
                        "Note: the phone app has a small problem visualizing checkboxes in preview mode. " \
                        "This, however, has no impact on your editing. \n\n"
