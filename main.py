import json
import datetime
import subprocess
import time

def send_notification(title, message):
    """ Send a notification on macOS using AppleScript via subprocess. """
    try:
        applescript_cmd = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.run(["osascript", "-e", applescript_cmd])
    except Exception as e:
        print(f"Error sending notification: {e}")

def read_schedule_from_json():
    try:
        with open('/Users/arbutus/Desktop/Code/2023/task-notifier/schedule.json', 'r') as file:
            schedule = json.load(file)
        return schedule
    except FileNotFoundError:
        send_notification("Error", "The schedule JSON file was not found.")
        exit()
    except json.JSONDecodeError:
        send_notification("Error", "There was an issue decoding the schedule JSON file.")
        exit()

def get_current_task(schedule):
    current_day = datetime.datetime.now().strftime('%A')
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    
    # Return None if the current day isn't in the schedule
    if current_day not in schedule:
        return None

    # Iterate through today's tasks
    for time_range, task in schedule[current_day].items():
        start_time, end_time = time_range.split(' - ')
        
        # Convert time strings to datetime objects
        start_time_obj = datetime.datetime.strptime(start_time, '%I:%M %p').time()
        end_time_obj = datetime.datetime.strptime(end_time, '%I:%M %p').time()
        current_time_obj = datetime.datetime.strptime(current_time, '%I:%M %p').time()

        # Check if the current time falls within a task's time range
        if start_time_obj <= current_time_obj <= end_time_obj:
            return task

    return None

def find_end_time(schedule, task_name):
    for day, tasks in schedule.items():
        for time_range, task in tasks.items():
            if task == task_name:
                _, end_time = time_range.split(' - ')
                return end_time
    return None

def main():
    current_task = None
    while True:  # Keep running indefinitely
        try:
            schedule = read_schedule_from_json()
            new_task = get_current_task(schedule)

            if new_task is None:
                time.sleep(60)
                continue

            if new_task != current_task:
                current_task = new_task
                end_time = find_end_time(schedule, current_task)
                send_notification('Task:', f'{current_task} until {end_time}')

            time.sleep(60)

        except Exception as e:
            send_notification("Unexpected Error", str(e))
            time.sleep(60)

if __name__ == "__main__":
    main()