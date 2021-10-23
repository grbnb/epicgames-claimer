import argparse
import importlib
import json
import os
import shutil
import sys
import time
from typing import List, Tuple

import requests
import schedule

try:
    import epicgames_claimer
except:
    shutil.copy("epicgames_claimer.py.bak", "epicgames_claimer.py")
    import epicgames_claimer

args = epicgames_claimer.get_args(include_auto_update=True)

def has_newer_version() -> Tuple[bool, str]:
    response = requests.get("https://api.github.com/repos/luminoleon/epicgames-claimer/tags").text
    response_json = json.loads(response)
    local_ver = epicgames_claimer.__version__.split(".")
    latest_ver = "{}.0.0".format(local_ver[0]).split(".")
    latest_sha = ""
    for item in response_json:
        item_ver = item["name"].lstrip("Vv").split(".")
        if item_ver[0] == latest_ver[0]:
            if int(item_ver[1]) > int(latest_ver[1]):
                latest_ver = item_ver
                latest_sha = item["commit"]["sha"]
    for item in response_json:
        item_ver = item["name"].lstrip("Vv").split(".")
        if item_ver[0] == latest_ver[0]:
            if int(latest_ver[1]) == int(item_ver[1]):
                if int(item_ver[2]) > int(latest_ver[2]):
                    latest_ver = item_ver
                    latest_sha = item["commit"]["sha"]
    if latest_ver[0] == local_ver[0]:
        if int(latest_ver[1]) > int(local_ver[1]):
            return True, latest_sha
        elif int(latest_ver[1]) == int(local_ver[1]) and int(latest_ver[2]) > int(local_ver[2]):
            return True, latest_sha
    return False, latest_sha

def reload_module() -> None:
    successed = False
    try:
        importlib.reload(epicgames_claimer)
        successed = True
    except:
        shutil.copy("epicgames_claimer.py.bak", "epicgames_claimer.py")
        importlib.reload(epicgames_claimer)
    if not successed:
        raise ValueError("Failed to reload epicgames_claimer.py.")

def update_reload_module() -> None:
    shutil.copy("epicgames_claimer.py", "epicgames_claimer.py.bak")
    response = requests.get("https://luminoleon.github.io/epicgames-claimer/epicgames_claimer.py")
    with open("epicgames_claimer.py","wb") as f:
        f.write(response.content)
    reload_module()

def update() -> None:
    try:
        need_update = has_newer_version()[0]
        if need_update:
            update_reload_module()
            epicgames_claimer.log("epicgames_claimer.py has been updated.")
    except Exception as e:
        epicgames_claimer.log("Update epicgames_claimer.py failed. {}: {}".format(e.__class__.__name__, e), level="warning")

def get_args_string(namespace: argparse.Namespace, exclude_keys: List[str] = ["interactive", "data_dir", "once", "auto_update"]) -> str:
    args_string = " "
    for key, value in namespace.__dict__.items():
        if not key in exclude_keys:
            if value == None:
                pass
            elif type(value) == bool:
                if value == True:
                    args_string += "--{} ".format(key.replace("_", "-"))
                elif value == False:
                    pass
            else:
                args_string += "--{} ".format(key.replace("_", "-"))
                args_string += "{} ".format(value)
    return args_string

def run() -> None:
    if args.auto_update:
        update()
    try:
        os.system(sys.executable + " epicgames_claimer.py -o " + get_args_string(args))
    except Exception as e:
        epicgames_claimer.log("Failed to run epicgames_claimer.py. {}".format(e), "error")

def scheduled_run(at: str):
    schedule.every().day.at(at).do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main() -> None:
    epicgames_claimer.log("Claimer started.")
    run()
    if not args.once:
        scheduled_run(args.run_at)
    epicgames_claimer.log("Claim completed.")

if __name__ == "__main__":
    main()
