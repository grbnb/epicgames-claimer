import importlib
import time

import schedule
import update_check
from pyppeteer.errors import BrowserError

import epicgames_claimer

args = epicgames_claimer.get_args(include_auto_update=True)

def is_up_to_date() -> bool:
    try:
        up_to_date = update_check.isUpToDate("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py")
        return up_to_date
    except Exception as e:
        epicgames_claimer.log("Check for update failed. {}".format(e), level="warning")
        return True

def update() -> None:
    try:
        update_check.update("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py")
        importlib.reload(epicgames_claimer)
        epicgames_claimer.log("\"epicgames_claimer.py\" has been updated.")
    except Exception as e:
        epicgames_claimer.log("Update \"epicgames_claimer.py\" failed. {}: {}".format(e.__class__.__name__, e), level="warning")

def run() -> None:
    if args.auto_update and not is_up_to_date():
        update()
    for i in range(3):
        try:
            claimer_notifications = epicgames_claimer.notifications(serverchan_sendkey=args.push_serverchan_sendkey)
            claimer = epicgames_claimer.epicgames_claimer(args.data_dir, headless=not args.no_headless, chromium_path=args.chromium_path, notifications=claimer_notifications)
            claimer.add_quit_signal()
            claimer.run_once(args.interactive, args.email, args.password)
            break
        except BrowserError as e:
            epicgames_claimer.log(str(e).replace("\n", " "), "warning")
            if i == 2:
                epicgames_claimer.log("Failed to open the browser.", "error")
                return

def scheduled_run(at: str):
    schedule.every().day.at(at).do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main() -> None:
    epicgames_claimer.log("Claimer is starting...")
    if args.auto_update and not is_up_to_date():
        update()
    claimer_notifications = epicgames_claimer.notifications(serverchan_sendkey=args.push_serverchan_sendkey)
    claimer = epicgames_claimer.epicgames_claimer(args.data_dir, headless=not args.no_headless, chromium_path=args.chromium_path, notifications=claimer_notifications)
    if args.once == True:
        epicgames_claimer.log("Claimer started.")
        claimer.run_once(args.interactive, args.email, args.password)
        epicgames_claimer.log("Claim completed.")
    else:
        epicgames_claimer.log("Claimer started.".format(args.run_at))
        claimer.run_once(args.interactive, args.email, args.password)
        claimer.add_quit_signal()
        scheduled_run(args.run_at)

if __name__ == "__main__":
    main()
