import argparse
import re


def validate_date_format(input_str: str) -> bool:
    pattern = r"(\d{4})\s\{.+?\}"
    return bool(re.fullmatch(pattern, input_str))


def parse_input(input_str: str) -> dict:
    time, task = re.findall(r"(\d{4})\s\{(.+?)\}", input_str)[0]
    hours = int(time[:2])


    minutes = int(time[2:])
    return {"hours": hours, "minutes": minutes, "task": task.strip()}


def add_task(args: argparse.Namespace) -> list:
    task_list = []

    if args.task:
        for task in args.task:
            if not validate_date_format(task):
                raise ValueError(f"Invalid format for task: {task}")

            task_dict = parse_input(task)
            task_list.append(task_dict)
        

    return task_list


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to manage tasks in the format: HHmm {task[s]}.")
    parser.add_argument("-t", "--task", nargs="+",
                        help="Add a task or tasks in the specified format: HHmm {task[s]}.")
    parser.add_argument("-d", "--display", action="store_true",
                        help="Display the tasks for the day.")
    args = parser.parse_args()
    tasks = add_task(args)

    # Print or process the tasks as reqired
    if args.display:
        for task in tasks:
            print(f"{task['hours']}:{task['minutes']} >>> {task['task']}")


if __name__ == "__main__":
    main()

