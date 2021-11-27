import argparse
import json
import os
import re
import shutil
import sys
import time
from typing import List, Tuple

import requests
import schedule


CLAIMER_FILE_NAME = "epicgames_claimer.py"
CLAIMER_FILE_BAK_NAME = "epicgames_claimer.py.bak"


API_TAGS = "https://api.github.com/repos/luminoleon/epicgames-claimer/tags"
API_LATEST = "https://api.github.com/repos/luminoleon/epicgames-claimer/releases/latest"


MESSAGE_START = "Claimer started"
MESSAGE_END = "Claim completed"
MESSAGE_UPDATING = "Found a new version. Updating ..."
MESSAGE_UPDATE_FAILED = "Update failed: "
MESSAGE_UPDATE_COMPLETED = "Update completed"
MESSAGE_RUN_FAILED = f"Failed to run {CLAIMER_FILE_NAME}: "


try:
    import epicgames_claimer
except:
    shutil.copy(CLAIMER_FILE_BAK_NAME, CLAIMER_FILE_NAME)
    import epicgames_claimer


args = epicgames_claimer.get_args(run_by_main_script=True)


def get_current_version() -> List[str]:
    result = os.popen(f"{sys.executable} {CLAIMER_FILE_NAME} --version").read()
    version_string = re.findall(r"\d+\.(?:\d+\.)*\d+", result)[0]
    version = version_string.split(".")
    return version


def get_latest_version() -> Tuple[List[str], str]:
    response = json.loads(requests.get(API_LATEST).text)
    tag_name = response["tag_name"]
    version_string = re.findall(r"\d+\.(?:\d+\.)*\d+", tag_name)[0]
    version = version_string.split(".")
    url = ""
    for item in response["assets"]:
        if item["name"] == CLAIMER_FILE_NAME:
            url = item["browser_download_url"]
    return version, url


def need_update() -> Tuple[bool, str]:
    current_ver = get_current_version()
    latest_ver, latest_download_url = get_latest_version()
    if not os.path.exists(CLAIMER_FILE_NAME):
        return True
    if latest_ver[0] != current_ver[0]:
        return False, latest_download_url
    found_a_new_version = False
    if int(latest_ver[1]) > int(current_ver[1]):
        found_a_new_version = True
    elif int(latest_ver[1]) == int(current_ver[1]) and int(latest_ver[2]) > int(current_ver[2]):
        found_a_new_version = True
    return found_a_new_version, latest_download_url


def update() -> None:
    try:
        found_a_new_version, latest_download_url = need_update()
        if found_a_new_version:
            shutil.copy(CLAIMER_FILE_NAME, CLAIMER_FILE_BAK_NAME)
            response = requests.get(latest_download_url)
            epicgames_claimer.log(MESSAGE_UPDATING)
            with open(CLAIMER_FILE_NAME,"wb") as f:
                f.write(response.content)
            epicgames_claimer.log(MESSAGE_UPDATE_COMPLETED)
    except Exception as e:
        epicgames_claimer.log(f"{MESSAGE_UPDATE_FAILED}{e}", level="warning")


def get_args_string(namespace: argparse.Namespace, exclude_keys: List[str] = ["interactive", "data_dir", "auto_update", "external_schedule"]) -> str:
    args_string = ""
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
                if " " in str(value):
                    args_string += "\"{}\" ".format(value)
                else:
                    args_string += "{} ".format(value)
    return args_string


def run_once() -> None:
    try:
        if args.auto_update:
            update()
        os.system(f"{sys.executable} {CLAIMER_FILE_NAME} --external-schedule {get_args_string(args)}")
        args.no_startup_notification = True
    except Exception as e:
        epicgames_claimer.log(f"{MESSAGE_RUN_FAILED}{e}", "error")


def run_forever():
    run_once()
    schedule.every().day.at(args.run_at).do(run_once)
    while True:
        schedule.run_pending()
        time.sleep(1)


def main() -> None:
    epicgames_claimer.log(MESSAGE_START)
    run_once() if args.once else run_forever()
    epicgames_claimer.log(MESSAGE_END)


if __name__ == "__main__":
    main()
