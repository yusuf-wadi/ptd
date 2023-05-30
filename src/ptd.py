import argparse
from datetime import datetime
import os

# Define the task class
class Task:
    def __init__(self, time, description: str, completed: bool):
        self.time = time
        self.description = description
        self.completed = completed 

# Parse the command line arguments
parser = argparse.ArgumentParser(description="A cli tool that helps you plan your day")
parser.add_argument("-a", "--add", help="add a task to your day", nargs="+")
parser.add_argument("-d", "--display", help="display your tasks for the day", action="store_true")
parser.add_argument("-c", "--complete", help="mark a task as complete")
parser.add_argument("-u", "--uncomplete", help="mark a task as incomplete")
parser.add_argument("-l", "--list_ic", help="list incomplete tasks")
parser.add_argument("-r", "--remove", help="remove a task from your day (specify time)")
args = parser.parse_args()

print(args)
# Initialize the dictionary of tasks
tasks = {}

# create tasks directory in user's programs folder
if os.name == "nt":
    tasks_dir = os.path.join(os.path.expanduser('~'),  "Documents", "tasks")
    #print(tasks_dir)
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
        
if os.name == "posix":
    tasks_dir = os.path.join(os.path.expanduser('~'),  "tasks")
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)

filename = datetime.now().strftime("%d%m%Y_tasks.txt")
file = os.path.join(tasks_dir, filename)
# If the user specified the "add" argument, parse the task and time and add it to the dictionary of tasks
#dont add duplicate tasks
def add_task(time, description, completed):
    if args.add:
        if time not in tasks.keys():
            tasks[time] = [description, completed]
        else:
            print("Task at this time already exists")
            update = input("Update task? (y/n): ")
            if update == "y":
                tasks[time] = [description, completed]
    else:
        tasks[time] = [description, completed]
        
        
def get_tasks(file):
    try:
        with open(file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                time, description, completed = line.split(",")
                print("in get_tasks: " + time, description, completed)
                time = datetime.strptime(time, "%H%M")
                description = description.strip()
                completed = completed.strip()
                add_task(time.strftime("%H%M"), description, completed)
                
    except FileNotFoundError:
        if not args.add:
            print("No tasks for today")
            
def write_to_file(file, tasks):
    with open(file, "w") as f:
        for time, task in tasks.items():
            print("in write_to_file: " + time, task[0], task[1])
            f.write(f"{time},{task[0]},{task[1]}\n")
            
def error(msg):
    print("-------- ERROR --------")
    print(msg)
    print("-------- ERROR --------")
            
if args.add:
    # get tasks from file
    get_tasks(file)
    # parse the task and time and add it to the dictionary of tasks
    try:
        for i in range(0, len(args.add), 2):
            time = datetime.strptime(args.add[i], "%H%M").strftime("%H%M")
            description = args.add[i+1]
            add_task(time, description, False)
    except IndexError:
        error("Please specify a time and description for each task")
    # write tasks to file
    tasks = dict(sorted(tasks.items()))
    #if not os.path.exists(file) or os.stat(file).st_size == 0:
    write_to_file(file, tasks)
    # else:
    #     append_to_file(file, tasks)

if args.complete:
    # get tasks from file
    get_tasks(file)
    # mark task as complete
    if args.complete in tasks.keys():
        tasks[args.complete][1] = True
    else:
        error("Task not found")
    # write tasks to file
    write_to_file(file, tasks)

if args.uncomplete:
    # get tasks from file
    get_tasks(file)
    # mark task as incomplete
    if args.uncomplete in tasks.keys():
        tasks[args.uncomplete][1] = False
    else:
        error("Task not found")
    # write tasks to file
    write_to_file(file, tasks)

# If the user specified the "display" argument, sort the dictionary of tasks by time and display them in a timeline format
if args.display:
    # print stream
    print("displaying tasks...")
    # get tasks from file
    get_tasks(file)
    for time, task in sorted(tasks.items()):
        print("in display: " + time, task[0], task[1])
        print(f"{time}: {task[0]}{'[X]' if task[1] else '[ ]'}")

# If the user specified the "remove" argument, remove the task from the dictionary of tasks
if args.remove:
    # get tasks from file
    get_tasks(file)
    # remove task
    if args.remove in tasks.keys():
        del tasks[args.remove]
    else:
        error("Task not found")
    # sort tasks by time
    tasks = dict(sorted(tasks.items()))
    # write tasks to file
    write_to_file(file, tasks)
    

# If the user didn't specify any arguments, display the help message
if not (args.add or args.display or args.remove):
    parser.print_help()