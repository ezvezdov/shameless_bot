import json
from datetime import datetime, timezone
from os import path
import re
from weakref import ref

time_format = "%Y-%m-%dT%H:%M:%S%z"


def utc_to_local(utc_dt):
    """
    Change timezone to Czech timezone.
    """
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def get_message_for_current_work(work):
    """
    Build message with current job information.
    """

    message = ""

    # Add Name to messsage
    message += "*Name*: " + work["name"] + "\n"

    message += "*Role*: " + work["role"] + "\n"

    # Add Capacity to message
    message += "*Capacity*: " + work["capacity"] + "\n"
    
    # Add work time to message
    message += work["time"] + "\n"

    # Add date to message
    message += work["date"] + "\n"

    # Add location if it is
    try:
        message += "*Location*: " + work["location"] + "\n"
    except:
        pass
    
    # Add Requirements to message
    if work['requirements'] != "":
        message += work['requirements']

    message+="\n"

    return message

def generate_refactored_data():
    count = 0

    f = open(path.join('data','parsed_data.json'))
    data = json.load(f)

    position = data["entities"]["Position"]
    shift = data["entities"]["Shift"]
    location = data["entities"]["Location"]

    refactored_data = dict()
    accepted_jobs = []
    not_accepted_jobs = []

    for value in position.values():
        count += 1
        # Continue when zaloznik 
        # 2 - zaloznik
        # 1 - crewboss
        # 0 - pracovnik
        if value["role"] == 2:
            continue
        

        tstamp_start = utc_to_local(datetime.strptime(value["startTime"], time_format))
        tstamp_end = utc_to_local(datetime.strptime(value["endTime"], time_format))
        tstamp_delta = tstamp_end - tstamp_start

        # Continue if job is 5+ hours
        if tstamp_delta.seconds > (60 * 60 * 5):
            not_accepted_jobs.append(value['id'])
            try:
                not_accepted_jobs += value['connected']
            except:
                pass
            continue

        # Skip jobs if it's full
        if value["freeCapacity"] == 0:
            continue

        work = dict()
        
        # Add Name
        work['name'] = shift[str(value["shift"])]["name"]

        # Add Capacity
        work['capacity'] = str(value["totalCapacity"] - value["freeCapacity"]) + "/" + str(value["totalCapacity"])

        # Add Location
        try:
            work['location'] = location[str(value["location"])]["address"]
        except:
            pass
        
        # Add Date
        work['date'] = "*Date*: " + tstamp_start.strftime("%d.%m.%Y %A")

        # Add Time
        if tstamp_delta.seconds % 3600 == 0:
            work['time'] = "*Time*: " + str(tstamp_delta.seconds // 3600) + " h ("
        else:
            work['time'] = "*Time*: " + str(tstamp_delta.seconds / 3600) + " h ("
        work['time'] += tstamp_start.strftime("%H:%M") + "-" + tstamp_end.strftime("%H:%M") + ")"

        # Add Requirements
        work['requirements'] = ""
        for current_requirement in value['requirements']:
            work['requirements'] += "*Requirements*: "
            work['requirements'] += current_requirement['title'] + "\n"

        # Add Connected
        try:
            work['connected'] = value['connected']
        except:
            work['connected'] = []
        
        # Add Role
        # 2 - zaloznik
        # 1 - crewboss
        # 0 - pracovnik
        work['role'] =  "Pracovn\u00edk" if value['role'] == 0 else "Crewboss"
        
        # Add whole message
        work['message'] = get_message_for_current_work(work)
        
        refactored_data[value['id']] = work
        accepted_jobs.append(value['id'])

    for id in accepted_jobs:
        if id in not_accepted_jobs:
            for id_to_del in refactored_data[id]['connected']:
                try: del refactored_data[id_to_del]
                except: pass
            try: del refactored_data[id]
            except: pass
            continue
        for connected_id in refactored_data[id]['connected']:
            if connected_id in not_accepted_jobs:
                for id_to_del in refactored_data[id]['connected']:
                    try: del refactored_data[id_to_del]
                    except: pass
                try: del refactored_data[id]
                except: pass
                continue


    

    with open(path.join('data',"refactored_data.json"), "w") as outfile:
        json.dump(refactored_data, outfile)
