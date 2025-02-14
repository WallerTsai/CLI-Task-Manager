# CLI Task Manager  
**Version**: v1.0  
**Last Updated**: 2025-02-15  

---

## Description  

A simple command-line task management tool implemented in Python. It supports adding, deleting, updating, and listing tasks. Task data is stored locally in a JSON file. Task statuses include `todo`, `in-progress`, and `done`, and task IDs are automatically reorganized into a continuous sequence.  

---

## Features  

- **Add Task**: Add a new task with a description; a unique ID is automatically assigned.  
- **Delete Task**: Delete a task by its ID.  
- **Update Task Status**: Update a task's status (`todo`, `in-progress`, `done`).  
- **List Tasks**: List all tasks, optionally filtered by status.  
- **Clean Tasks**: Clear all tasks.  
- **Automatic ID Reorganization**: Task IDs are automatically reorganized into a continuous sequence after deletion.  
- **Persistent Storage**: Task data is saved in a `tasks.json` file.  

---

## Project Structure  

### Core Functions  

- **`load_tasks()`**: Load task data from `tasks.json`. Returns an empty dictionary if the file is missing, empty, or malformed.  
- **`save_tasks(jsondata)`**: Save task data to `tasks.json` and reorganize task IDs.  
- **`reorganize_ids(jsondata)`**: Reorganize task IDs into a continuous sequence (e.g., `1, 2, 3`).  
- **`add_task(jsondata, description)`**: Add a new task with an auto-assigned unique ID.  
- **`delete_task(jsondata, task_id)`**: Delete a task by its ID.  
- **`clean_tasks(jsondata)`**: Clear all tasks.  
- **`update_task_status(jsondata, task_id, new_status)`**: Update a task's status.  
- **`list_tasks(jsondata, status_filter)`**: List tasks, optionally filtered by status.  

### Command-Line Interface  

Uses `argparse` to parse commands. Supported commands:  

- **`add`**: Add a new task.  
- **`delete`**: Delete a task.  
- **`clean`**: Clear all tasks.  
- **`update`**: Update a task's status.  
- **`list`**: List tasks, optionally filtered by status.  

---

## Installation & Execution  

1. Ensure Python 3.x is installed.  
2. Run the script:  
   ```bash  
   python task_manager.py  
   ```  

---

## Usage  

### Add a Task  
```bash  
python task_manager.py add test1  
```  

### Delete a Task  
```bash  
python task_manager.py delete 1  
```  

### Update Task Status  
```bash  
python task_manager.py update 2 todo  
```  

### List All Tasks  
```bash  
python task_manager.py list  
```  

### List Tasks by Status  
```bash  
python task_manager.py list --status_filter done  
```  

### Clear All Tasks  
```bash  
python task_manager.py clean  
```  

---

## Data Storage  

Tasks are stored in `tasks.json` in the script's directory. Example format:  
```json  
{  
    "1": {  
        "description": "test1",  
        "status": "in-progress",  
        "createdAt": "2025-02-15 12:00:00",  
        "updatedAt": "2025-02-15 12:30:00"  
    },  
    "2": {  
        "description": "test2",  
        "status": "todo",  
        "createdAt": "2025-02-15 13:00:00",  
        "updatedAt": "2025-02-15 13:00:00"  
    }  
}  
```  

---

## Task Statuses  

- **`todo`**: Task is pending.  
- **`in-progress`**: Task is in progress.  
- **`done`**: Task is completed.  

---

## Example Workflow  

1. Add a task:  
   ```bash  
   python task_manager.py add dance  
   ```  

2. List all tasks:  
   ```bash  
   python task_manager.py list  
   ```  

3. Update task status:  
   ```bash  
   python task_manager.py update 1 in-progress  
   ```  

4. Delete a task:  
   ```bash  
   python task_manager.py delete 1  
   ```  

5. Clear all tasks:  
   ```bash  
   python task_manager.py clean  
   ```  

---

## Code Overview  

### Core Logic  

- **Task ID Management**: The `reorganize_ids` function ensures task IDs remain continuous.  
- **Status Validation**: The `is_valid_status` function validates task statuses.  
- **Timestamps**: Each task includes `createdAt` and `updatedAt` timestamps.  

### Command-Line Parsing  

- **`SupportedQueries` Class**: Defines supported commands and arguments.  
- **`get_parser` Method**: Dynamically generates the command-line parser.  

---

## Current Limitations  

1. **No Task Description Updates**:  
   - The current code cannot update task descriptions; users must delete and re-add tasks.  

2. **Performance Concerns**:  
   - Reorganizing IDs on every save may cause performance issues with large datasets.   

3. **Basic User Interaction**:  
   - Command-line output lacks formatting or color.  
   - Minimal input validation (e.g., empty task descriptions).  

4. **Limited Feature Set**:  
   - Missing common features like task priorities or due dates.  

---

## Future Optimizations(When I Feel Like It )

1. **Enhance Task Updates**:  
   - Add an `update-description` command.  
   ```bash  
   python task_manager.py update-description 1 "New description"  
   ```  

2. **Optimize Performance**:  
   - Reorganize IDs only when deleting tasks, not on every save.  

3. **Improve User Experience**:  
   - Use libraries like `rich` or `colorama` for formatted output.  
   ```bash  
   ✅ Task added successfully (ID: 1)  
   ```  

4. **Expand Features**:  
   - Add task priorities (high/medium/low) and due dates.  
   ```bash  
   python task_manager.py add "Finish report" --priority high --due-date 2025-10-24  
   ```  

5. **Add Backup Functionality**:  
   - Automatically backup task data.  
   ```bash  
   python task_manager.py backup --output tasks_backup.json  
   ```  

6. **Support Import/Export**:  
   - Import/export tasks from/to CSV or JSON.  
   ```bash  
   python task_manager.py import --file tasks.csv  
   python task_manager.py export --file tasks_export.json  
   ```  

7. **Command-Line Autocompletion**:  
   - Implement autocompletion using `argcomplete`.  
   ```bash  
   python task_manager.py upd<TAB>  # Autocompletes to 'update'  
   ```  

---

## Notes  

- Do not manually modify `tasks.json` to avoid data corruption.  
- Task IDs are automatically reorganized after deletions.  

---