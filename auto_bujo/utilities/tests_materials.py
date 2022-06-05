import pymongo
import datetime
import re

note = """ 01 June 2022, Wednesday - Have a nice day! (*・ω・)ﾉ  ♥

----------

## (・ω・) Upcoming events
- 2022-06-02 (tomorrow) - Test upcoming, day after tomorrow
- 2022-06-05 (in 4 days) - Test upcoming, 5 days

----------

##  ヾ(=`ω´=)ノ” Your tasks 
- [ ] Wash the dishes
- [ ] Change bed sheets
- [ ] task1
- [ ] task2
- [x] ciao
- [x] ciao

----------

##  (⌐0_0) Research on: Linux
- [ ] Research completed!
#### --- Description ---
 _Linux is pretty cool_
#### --- Steps ---
- [x] Find out what it is
- [x] Install linux
- [x] Another step
- [ ] yet another step


----------

##  (⌐0_0) Research on: Tailwind CSS
- [X] Research completed!
#### --- Description ---
 _This is a CSS framework_
#### --- Steps ---
- [x] Find out what it is
- [ ] Another step

----------

## ٩(ˊᗜˋ*) Writing zone!

- event: event | 2000-01-01 | 1 year |
-Event:     event | 1233-98-43 ||

-chore: chore |  | 34 |
- Chore:   chore | 2022-32-32 | 2 |

- [ ] shouldn't pick this
- [] not match
- [x] shouldn't match

- Note: A nice day | Today I went to the park.
It was a lot of fun: there were fungi that made funny jokes. |
-note: |throwed out the trash|

-idea: Pomodoro app | it rewards you with cat pictures on every break, using a cat API |
- Idea: Bujo app |   |

- Research: topic | something | task1, task2, task3, task4 |
-research: linux |desciption||

- Expense: 2500 yen | sweater | Amazon |
-expense: ￥400 |matcha latte| a store, Tokyo |
- expense: ￥200 | pencil |       |

-Wishlist: cute sweater | Store near home | 1|
-wishlist: another cute thing | florist | 10 |
 


----------"""

expenses = """
----------
## April 2020

- ￥900 | Sweater (from X) | 2020-03-23
- ￥900 | Sweater (from X) | 2020-03-23
- ￥900 | Sweater (from X) | 2020-03-23
- ￥900 | Sweater (from X) | 2020-03-23
- ￥900 | Sweater (from X) | 2020-03-23
- ￥900 | Sweater (from X) | 2020-03-23

### Total: ￥6400

----------
"""

wishlist = """### ✧･ﾟ: *✧･ﾟ:*  10  *:･ﾟ✧*:･ﾟ✧

something

----------
### ✧･ﾟ: *✧･ﾟ:*  9  *:･ﾟ✧*:･ﾟ✧

- [x] ￥ 3000  | teddy bear (from new york)   

----------
### ✧･ﾟ: *✧･ﾟ:*  8  *:･ﾟ✧*:･ﾟ✧

- [x] ￥ 20000 | flowers (from kindergarden)    

----------
### ✧･ﾟ: *✧･ﾟ:*  7  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  6  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  5  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  4  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  3  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  2  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  1  *:･ﾟ✧*:･ﾟ✧

----------
### ✧･ﾟ: *✧･ﾟ:*  0  *:･ﾟ✧*:･ﾟ✧"""

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
today = datetime.date.today().isoformat()
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
day_after_tomorrow = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
long_ago = (datetime.date.today().replace(year=1990) + datetime.timedelta(days=1)).isoformat()

with pymongo.MongoClient(host="127.0.0.1", port=27017) as client:
    db = client["routineDB"]

    todo_collection = db["todo"]
    events_collection = db["events"]
    chores_collection = db["chores"]
    research_collection = db["researches"]
    notes_collection = db["notes"]
    ideas_collection = db["ideas"]
    expenses_collection = db["expenses"]

    # todo_collection.insert_one({"task": "Wash the dishes"})
    # todo_collection.insert_one({"task": "Change bed sheets"})

    # events_collection.insert_one({"event": "Test years ago, 1 year", "repeats every": "2 years", "date": long_ago})
    # events_collection.insert_one({"event": "Test today", "repeats every": "", "date": today})
    # events_collection.insert_one({"event": "Test yestearday", "repeats every": "", "date": yesterday})
    # events_collection.insert_one({"event": "Test long ago, 4 months", "repeats every": "4 months", "date": long_ago})
    # events_collection.insert_one({"event": "Test yesterday, 5 days", "repeats every": "5 days", "date": yesterday})
    # events_collection.insert_one(
    #     {"event": "Test upcoming, day after tomorrow", "repeats every": "5 days", "date": day_after_tomorrow})
    # events_collection.insert_one({"event": "Test upcoming, 5 days", "repeats every": "None",
    #                               "date": (datetime.date.today() + datetime.timedelta(days=5)).isoformat()})
    #
    # chores_collection.insert_one({"chore": "Shower", "repeats every": "1", "next occurrence": yesterday})
    # chores_collection.insert_one({"chore": "Laundry", "repeats every": "30", "next occurrence": long_ago})
    # chores_collection.insert_one({"chore": "vacuum", "repeats every": "None", "next occurrence": today})
    # chores_collection.insert_one({"chore": "fish", "repeats every": "None", "next occurrence": yesterday})
    # events_collection.insert_one({"event": "Test yestearday, 1 year", "repeats every": "1 year", "date": "ababa"})
    # chores_collection.insert_one({"chore": "fish", "repeats every": "None", "next occurrence": "pachaba"})

    # research_collection.insert_one({"topic": "Linux",
    #                                 "description": "Linux is pretty cool",
    #                                 "steps": [{"task": "Find out what it is", "completed": False},
    #                                           {"task": "Install linux", "completed": True},
    #                                           {"task": "Another step", "completed": False}]})
    # research_collection.insert_one({"topic": "Tailwind CSS",
    #                                 "description": "This is a CSS framework",
    #                                 "steps": [{"task": "Find out what it is", "completed": True},
    #                                           {"task": "Another step", "completed": False}]})

# from .db_collections import db_collections
#
# events_regex = db_collections["events"]["regex"]["item"]
# # match: - (event|Event): (event description) | (next occurrance: YYYY-MM-DD) | N (day/s|month/s|year/s) |
#
# chores_regex = db_collections["chores"]["regex"]["item"]
# # match: - (chore|Chore): (chore description) | (next occurrance: YYYY-MM-DD) | (every X days) |
#
# task_regex = db_collections["todo"]["regex"]["item"]
# # match: - ([ ])|([x]) (your task)
#
# task_group_regex = db_collections["todo"]["regex"]["group"]
# # Get tasks group, from header to <hr>
#
# research_regex = db_collections["researches"]["regex"]["item"]
# # match: - (research|Research): (topic) | (description) | (tasks/steps to completion) |
#
# research_group_regex = db_collections["researches"]["regex"]["group"]
# # Get topic of research and research group, from header to <hr>
#
# research_description_regex = db_collections["researches"]["regex"]["description"]
# # match anything between the description and steps headers
#
# notes_regex = db_collections["notes"]["regex"]["item"]
# # match: - (note|Note): (note title)? | (note body) |
#
# ideas_regex = db_collections["ideas"]["regex"]["item"]
# # match: - (idea|Idea): (project idea) | (description)? |
#
# expenses_regex = db_collections["expenses"]["regex"]["item"]
# # match: - (expenses|Expenses): (item) | (place) | (cost) |
#
# wishlist_regex = db_collections["wishlist"]["regex"]["item"]
# # match: - (wishlist/Wishlist): (item) | (place) | (need level: 1-10) |

Test = """
- event: event | 2000-01-01 | 1 year |
-Event:     event | 1233-98-43 ||

-chore: chore | | 34 |
- Chore:   chore | 2022-32-02 | 23 days |

- [ ] task1
- [] task2
- [x] task3
- [x] task4

- Note: A nice day | Today I've gone to the park.
It was a lot of fun: there was a fungi that made funny jokes. |
-note: throwed out the trash ||

-idea: Pomodoro app | it rewards you with cat pictures on every break, using a cat API |
- Idea: Bujo app |   |

- Research: new topic | something | list of things, item 1, item 2, item 3 |
-research: linux |desciption||

- Expense: 25.99 | cat tree | Amazon |
-expense: 2 | chocolate | Store, Milan |

-Wishlist: 12 | cute sweater | Store near home | 1|
-wishlist: 43 | another cute thing | | 10 |



"""

# if __name__ == "__main__":
    # print(re.findall(events_regex, Test))
    # print(re.findall(chores_regex, Test))
    # print(re.findall(task_regex, Test))
    # print(re.findall(research_regex, Test))
    # print(re.findall(notes_regex, Test))
    # print(re.findall(expenses_regex, Test))
    # print(re.findall(wishlist_regex, Test))
    # print(re.findall(ideas_regex, Test))