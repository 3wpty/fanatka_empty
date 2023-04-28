"""
PYTHON FILE WITH SOME OF LARGE MECHANICS FOR MAIN FILE
"""

import json
import random

# ==============================================================================
# OPEN JSON -> WARN (BAN) -> UPDATE JSON
def warn_mecha(user):
    user = str(user)
    flag = True
    getting_ban = False  # user isnt banned
    with open("j_warns.json", "r") as filename:
        data = json.load(filename)  # loading json file

    for key, value in data.items():
            if key == user:  # if user already in list
                data[key] = value + 1  # incrementing value
                if data[key] >= 4:  # if warns >= 4
                    data[key] = 0
                    getting_ban = True  # user gets banned

                flag = False  # user already warned
                break
    if flag:  # if user not in list
        data[user] = 1  # creating new value
                
    with open("j_warns.json", "w") as filename:
        json.dump(data, filename, indent=4)  # updating json file

    return (data[user], getting_ban)


# ==============================================================================
# OPEN JSON -> CHECK IF ALREADY EXIST -> UPDATE JSON
def role_mecha(user):
    user = str(user)
    role_already_exist = False  # user havent got custom role
    with open("j_customroles.json", "r") as filename:
        data = json.load(filename)  # loading json file

    for key, value in data.items():
            if key == user:  # if user already in list
                role_already_exist = True

    if role_already_exist == False:  # if user not in list
        data[user] = 1  # creating new value
                
    with open("j_customroles.json", "w") as filename:
        json.dump(data, filename, indent=4)  # updating json file

    return (role_already_exist)


# ==============================================================================
# OPEN JSON -> ADD NEW VALUE -> UPDATE JSON
def role_id_mecha(user, role = "420"):
    user = str(user)
    role = str(role)
    with open("j_customroles.json", "r") as filename:
        data = json.load(filename)  # loading json file

    if role == "420":  # if you want to get role id
        return int(data[user])
    data[user] = role  # creating new value
                
    with open("j_customroles.json", "w") as filename:
        json.dump(data, filename, indent=4)  # updating json file


# ==============================================================================
# OPEN JSON -> CHANGE AVI -> UPDATE JSON
def dm_avi_mecha(user):
    flag = True
    with open("j_dm_avi.json", "r") as filename:
        data = json.load(filename)  # loading json file

    for key, value in data.items():
            if key == user:
                flag = False  # user already exist
                print("already")
                break

    if flag:  # if user not in list
        # data[user] = random.choice(["⚪", "⚫", "🟤", "🟣", "🔵", "🟢", "🟡", "🟠", "🔴"])  # creating new value
        data[user] = random.choice([":white_circle:", 
                                    ":black_circle:", 
                                    ":red_circle:", 
                                    ":blue_circle:", 
                                    ":brown_circle:", 
                                    ":purple_circle:", 
                                    ":green_circle:", 
                                    ":yellow_circle:",
                                    ":orange_circle:"
                                    ])  # creating new value
        print(data[user])

    with open("j_dm_avi.json", "w") as filename:
        json.dump(data, filename, indent=4)  # updating json file

    return (data[user])


# ==============================================================================
# CONVERTING TIME
def converting_time_mecha(time):

    if time[-1] == 'm':
        time_amount_ru = 'м.'  # minutes
        # source_time = time[:-1]
        time = int(time[:-1])
        time *= 60

    elif time[-1] == 'h':
        time_amount_ru = 'ч.'  # hours
        # source_time = time[:-1]
        time = int(time[:-1])
        time *= 3600

    elif time[-1] == 'd':
        time_amount_ru = 'дн.'  # days
        # source_time = time[:-1]
        time = int(time[:-1])
        time *= 86400

    else:
        # source_time = time
        time_amount_ru = 'с.'  # seconds
        time = int(time)


    time_days = time // 86400
    time_hours = (time % 86400) // 3600
    time_minutes = (time % 86400 % 3600) // 60
    time_seconds = time % 86400 % 3600 % 60



    return (time_days, time_hours, time_minutes, time_seconds)


# ==============================================================================
# OPEN J_VOTES.TXT
def vote_number_mecha():

    # loading txt file for reading
    filename = open("j_votes.txt", "r")
    number = filename.read()
    filename.close()

    # loading txt file for writing            
    filename = open("j_votes.txt", "w")
    filename.write(str(int(number) + 1))
    filename.close()
    return number


# ==============================================================================