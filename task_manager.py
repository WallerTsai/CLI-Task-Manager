import argparse
from datetime import datetime
import json
from enum import Enum
import os

class TaskStatus(Enum):
    """ Enumeration of possible task statuses """
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_FILE = os.path.join(SCRIPT_DIR, "tasks.json")

valid_statuses = {status.value for status in TaskStatus}

def is_valid_status(value:str) -> bool:
    """Check if a status value is valid
    
    Args:
        value (str): Status value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return value in valid_statuses

def load_tasks() -> dict:
    """Load tasks from JSON file
    
    Returns:
        dict: Dictionary containing all tasks
    """
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
    """Save tasks to JSON file with ID reorganization
    
    Args:
        jsondata (dict): Task data to save
    """
    with open(TASK_FILE,'w') as f:
        jsondata = reorganize_ids(jsondata)
        json.dump(jsondata,f,indent=4)

def reorganize_ids(jsondata:dict) -> dict:
    """Reorganize task IDs into contiguous numerical sequence
    
    Args:
        jsondata (dict): Original task data with existing IDs
        
    Returns:
        dict: New task data with sequential IDs starting from 1
    """
    if not jsondata:
        return {}
    
    new_tasks = {}
    for new_id,task in enumerate(jsondata.values(),start=1):
        new_tasks[str(new_id)] = task
    
    return new_tasks

def add_task(jsondata:dict,description:str) -> None:
    """Add a new task to the task list
    
    Args:
        jsondata (dict): Task data to modify
        description (str): Description of the new task
    """
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
    """Remove a task from the task list
    
    Args:
        jsondata (dict): Task data to modify
        task_id (str): ID of the task to remove
    """
    if jsondata.pop(task_id,None):
        print(f"Task (ID: {task_id}) deleted successfully")
    else:
        print(f"Task (ID: {task_id}) does not exist")

def clean_tasks(jsondata:dict) -> None:
    """Clear all tasks from the task list
    
    Args:
        jsondata (dict): Task data to clear
    """
    jsondata.clear()
    print(f"Task list cleaned up")

def update_task_status(jsondata:dict,task_id:str,new_status:str) -> None:
    """Update the status of a specific task
    
    Args:
        jsondata (dict): Task data to modify
        task_id (str): ID of the task to update
        new_status (str): New status value for the task
    """
    if not is_valid_status(new_status): # 判断类型在不在枚举类中
        print(f"Invalid status. Allowed statuses are: {', '.join([s.value for s in TaskStatus])}")
        return
    try:
        jsondata[task_id]["status"] = new_status
        jsondata[task_id]["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Task (ID: {task_id}) updated successfully")
    except KeyError:
        print(f"Task (ID: {task_id}) does not exist")

def list_tasks(jsondata: dict, status_filter:str = "all") -> None:
    """Display tasks in a formatted table
    
    Args:
        jsondata (dict): Task data to display
        status_filter (str): Filter tasks by status (default: 'all')(other: 'todo','in-progress','done')
    """
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
    " Configuration for supported CLI commands"
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
        """Get configured command specifications
        
        Returns:
            dict: Command configuration dictionary
        """
        return self._supported_queries

    @classmethod
    def get_parser(cls) -> argparse.ArgumentParser:
        """Create CLI argument parser
        
        Returns:
            argparse.ArgumentParser: Configured command line parser
        """
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

    # Load tasks
    tasks = load_tasks()

    command_info = supported_queries[kwargs.pop("command")]
    command_info["target"](tasks,**kwargs)

    # Save tasks
    save_tasks(tasks)
    
if __name__ == "__main__":
    main()
