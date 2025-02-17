import argparse
from datetime import datetime
import json
from enum import Enum
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_FILE = os.path.join(SCRIPT_DIR, "tasks.json")

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

valid_statuses = {status.value for status in TaskStatus}

def is_valid_status(value:str) -> bool:
    
    return value in valid_statuses

def load_tasks() -> dict:
    
    try:
        with open(TASK_FILE,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"The file is empty or contains formatting errors;\
               it will be replaced with a new data format.")
        return {}
    
def save_tasks(jsondata:dict) -> None:
    
    with open(TASK_FILE,'w') as f:
        jsondata = reorganize_ids(jsondata)
        json.dump(jsondata,f,indent=4)

def reorganize_ids(jsondata:dict) -> dict:
    
    if not jsondata:
        return {}
    
    new_tasks = {}
    for new_id,task in enumerate(jsondata.values(),start=1):
        new_tasks[str(new_id)] = task
    
    return new_tasks

def add_task(jsondata:dict,description:str) -> None:
    
    max_id = max((int(k) for k in jsondata.keys()), default=0)
    new_id = str(max_id + 1)
    jsondata[new_id] = {
        "description": description,
        "status": TaskStatus.TODO.value,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updatedAt":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(f"Task added successfully (ID: {new_id})")

def delete_task(jsondata:dict,task_id) -> None:
    
    if jsondata.pop(task_id,None):
        print(f"Task (ID: {task_id}) deleted successfully")
    else:
        print(f"Task (ID: {task_id}) does not exist")

def clean_tasks(jsondata:dict) -> None:
    
    jsondata.clear()
    print(f"Task list cleaned up")

def update_task_status(jsondata:dict,task_id:str,new_status:str) -> None:
    
    if not is_valid_status(new_status): 
        print(f"Invalid status. Allowed statuses are: {', '.join([s.value for s in TaskStatus])}")
        return
    try:
        jsondata[task_id]["status"] = new_status
        jsondata[task_id]["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Task (ID: {task_id}) updated successfully")
    except KeyError:
        print(f"Task (ID: {task_id}) does not exist")

def list_tasks(jsondata: dict, status_filter:str = "all") -> None:
    
    if not jsondata:
        print("No tasks found")

    print(f"{'ID':<5} {'Status':<12} {'Description':<30} {'Created At':<20} {'Updated At':<20}")
    print("-" * 90)

    flag = False
    for task_id,task in jsondata.items():
        if status_filter == "all" or task["status"] == status_filter:
            flag = True
            print(
                f"{task_id:<5} {task['status']:<12} {task['description']:<30} "
                f"{task['createdAt']:<20} {task['updatedAt']:<20}"
            )
    
    if not flag:
        print(f"No tasks found with status: {status_filter}")
    print("-" * 90)

class SupportedQueries:
    _supported_queries = {
        "add": {
            "target": add_task,
            "help": "Add a new task",
            "args": [
                {"params": ["description"], "type": str, "help": "Description of the task"}
            ]
        },
        "delete": {
            "target": delete_task,
            "help": "Delete a task",
            "args": [
                {"params": ["task_id"], "type": str, "help": "ID of the task to delete"}
            ]
        },
        "clean": {
            "target": clean_tasks,
            "help": "Clean all tasks",
            "args": []
        },
        "update": {
            "target": update_task_status,
            "help": "Update task status",
            "args": [
                {"params": ["task_id"], "type": str, "help": "ID of the task to update"},
                {"params": ["new_status"], "type": str.lower, "choices": [status.value for status in TaskStatus],
                "help": "New status (todo, in-progress, done)"}
            ]
        },
        "list": {
            "target": list_tasks,
            "help": "List tasks",
            "args": [
                {"params": ["--status_filter"], "type": str, "choices": ["all", "todo", "in-progress", "done"], 
                "default": "all", "help": "Filter tasks by status (default: all)"}
            ]
        }
    }

    @property
    def get_supported_queries(self) -> dict:
        
        return self._supported_queries

    @classmethod
    def get_parser(cls) -> argparse.ArgumentParser:
        
        parser = argparse.ArgumentParser(description="A simple CLI task manager.")
        subparsers = parser.add_subparsers(dest="command", required=True)

        for name,config in cls._supported_queries.items():
            subparser = subparsers.add_parser(name,help=config["help"])
            for arg in config["args"]:
                params = arg.pop("params")
                subparser.add_argument(*params,**arg)

        return parser

def main():
    supported_queries = SupportedQueries().get_supported_queries
    parser = SupportedQueries.get_parser()

    args = parser.parse_args()
    kwargs = vars(args)

    tasks = load_tasks()

    command_info = supported_queries[kwargs.pop("command")]
    command_info["target"](tasks,**kwargs)

    save_tasks(tasks)
    
if __name__ == "__main__":
    main()
