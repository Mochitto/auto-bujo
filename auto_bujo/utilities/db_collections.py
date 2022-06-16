db_collections = {"todo": {"parameters": ["task"],
                           "guide": [None],
                           "regex": {
                               "group": r"##\s*ヾ\(=`ω´=\)ノ”\s*Your tasks\s*([\s\S]*?)----------",
                               "item": r"-\s*(\[[xX ]\])\s*([^|]+?)\n",
                           }
                           },
                  "events": {"parameters": ["event", "date", "repeats every"],
                             "guide": [None, "when it will happen: YYYY-MM-DD",
                                       "when will it happen again?: X day(s)|month(s)|year(s). "
                                       "Can be empty, if there is no repetition"],
                             "regex": {
                                 "item": r"-\s*[eE]vent:\s*(.+?)\s*\|"
                                         r"\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*\|"
                                         r"\s*([0-9]{1,3}\s\S+)?\s*\|",
                             }
                             },
                  "chores": {"parameters": ["chore", "next occurrence", "repeats every"],
                             "guide": [None, "YYYY-MM-DD; if left empty, defaults to the next time you make a new note",
                                       "number of days; if empty, the chore will be deleted after one time"],
                             "regex": {
                                 "item": r"-\s*[cC]hore:\s*([^|]+?)\s*\|"
                                         r"\s*([0-9]{4}-[0-9]{2}-[0-9]{2})?\s*\|"
                                         r"\D*?(\d+)?\D*?\s*\|",
                             }
                             },
                  "researches": {"parameters": ["topic", "description", "steps"],
                                 "guide": [None, None, "tasks divided by a comma and a space"],
                                 "regex": {
                                     "group": r"Research on:\s*(.+)\s*"
                                              r"- (\[[xX ]]) Research completed!\s*[\s\S]*?"
                                              r"####\s*--- Description ---\s*"
                                              r"_?([\s\S]*?)_?\s*"
                                              r"####\s*--- Steps ---\s*"
                                              r"([\s\S]*?\s*?)"
                                              r"----------",
                                     "item": r"-\s*[Rr]esearch:\s*([^|]+?)\s*\|\s*([^|]+?)?\s*\|\s*\s*([^|]+?)?\s*\|",
                                 }
                                 },
                  "notes": {"parameters": ["title", "body"],
                            "guide": [None, None],
                            "regex": {
                                "item": r"-\s*[Nn]ote:\s*([^|]+?)?\s*\|\s*([^|]+?)\s*\|",
                            }
                            },
                  "ideas": {"parameters": ["concept", "description"],
                            "guide": [None, None],
                            "regex": {
                                "item": r"-\s*[Ii]dea:\s*([^|]+?)\s*\|\s*([^|]+?)?\s*\|",
                            }
                            },
                  "expenses": {"parameters": ["cost", "object bought", "place"],
                               "guide": [None, None, "where the item was bought, from:"],
                               "regex": {
                                   "item": r"-\s*[Ee]xpense:\s*\D*(\d+\.?\d?\d?).*?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)?\s*\|",
                               }
                               },
                  "wishlist": {"parameters": ["price", "item", "place", "level of need"],
                               "guide": [None, None,
                                         "where you've found the item", "how much you want/need it, from 1-10"],
                               "regex": {
                                   "item": r"-\s*[Ww]ishlist:\s*(\d+\.?\d?\d?).*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d\d?).*\s*\|",
                               }
                               },
                  }
