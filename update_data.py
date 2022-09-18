import json
from os import path

NO_JOBS_MESSAGE = "Сорач, пока что смен няма 😢"

new_data = dict()

def update_data():
    f = open(path.join('data','refactored_data.json'))
    global new_data
    new_data = json.load(f)

def get_all_works():
    """
    Get message with all jobs.
    """

    message = ""
    for work in new_data.values():
        message += work['message']

    if message == "":
        message = NO_JOBS_MESSAGE
    
    return message

def get_new_works():
    """
    Get message with new jobs.
    """

    f = open(path.join('data','old_data.json'))
    old_data = json.load(f)

    difference = list(set(new_data) - set(old_data))
    
    if len(difference) == 0:
        with open(path.join('data',"old_data.json"), "w") as outfile:
            json.dump(new_data, outfile)
        return NO_JOBS_MESSAGE

    message = "А что это у нас такое, новыe паушальчики?\n\n"

    for key in difference:
        message += new_data[key]['message']

    with open(path.join('data',"old_data.json"), "w") as outfile:
        json.dump(new_data, outfile)

    return message

    