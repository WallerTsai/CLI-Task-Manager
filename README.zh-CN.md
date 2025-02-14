
---

# CLI Task Manager
**版本**: v1.0  
**最后更新**: 2025-02-15

## Description

这是一个基于命令行的简单任务管理工具，使用 Python 实现。它支持添加、删除、更新和列出任务，任务数据以 JSON 格式存储在本地文件中。任务状态包括 `todo`、`in-progress` 和 `done`，任务 ID 会自动整理为连续序列。

---

## 功能特性

- **添加任务**：通过描述添加新任务，自动分配唯一 ID。
- **删除任务**：通过任务 ID 删除任务。
- **更新任务状态**：更新任务的状态（`todo`、`in-progress`、`done`）。
- **列出任务**：列出所有任务，支持按状态过滤。
- **清理任务**：清空所有任务。
- **自动 ID 整理**：删除任务后，自动重新整理任务 ID 为连续序列。
- **持久化存储**：任务数据保存在 `tasks.json` 文件中。

---

## 项目结构

### 核心函数

- **`load_tasks()`**：从 `tasks.json` 文件加载任务数据。如果文件不存在,空文件或格式错误，返回空字典。
- **`save_tasks(jsondata)`**：将任务数据保存到 `tasks.json` 文件，并自动整理任务 ID。
- **`reorganize_ids(jsondata)`**：将任务 ID 重新整理为连续序列（如 `1, 2, 3`）。
- **`add_task(jsondata, description)`**：添加新任务，自动分配唯一 ID。
- **`delete_task(jsondata, task_id)`**：通过任务 ID 删除任务。
- **`clean_tasks(jsondata)`**：清空所有任务。
- **`update_task_status(jsondata, task_id, new_status)`**：更新任务的状态。
- **`list_tasks(jsondata, status_filter)`**：列出任务，支持按状态过滤。

### 命令行接口

使用 `argparse` 实现命令行解析，支持以下命令：

- **`add`**：添加新任务。
- **`delete`**：删除任务。
- **`clean`**：清空所有任务。
- **`update`**：更新任务状态。
- **`list`**：列出任务，支持按状态过滤。

---

## 安装与运行

1. 确保已安装 Python 3.x。
2. 下载代码并运行：
   ```bash
   python task_manager.py
   ```

---

## 使用方法

### 添加任务
```bash
python task_manager.py add test1
```

### 删除任务
```bash
python task_manager.py delete 1
```

### 更新任务状态
```bash
python task_manager.py update 2 todo
```

### 列出所有任务
```bash
python task_manager.py list
```

### 按状态列出任务
```bash
python task_manager.py list --status_filter done
```

### 清空所有任务
```bash
python task_manager.py clean
```

---

## 数据存储

任务数据存储在 `tasks.json` 文件中，文件位于脚本所在目录。文件格式如下：

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

## 任务状态

- **`todo`**：任务待办。
- **`in-progress`**：任务进行中。
- **`done`**：任务已完成。

---

## 示例工作流

1. 添加任务：
   ```bash
   python task_manager.py add dance
   ```

2. 列出所有任务：
   ```bash
   python task_manager.py list
   ```

3. 更新任务状态：
   ```bash
   python task_manager.py update 1 in-progress
   ```

4. 删除任务：
   ```bash
   python task_manager.py delete 1
   ```

5. 清空所有任务：
   ```bash
   python task_manager.py clean
   ```

---

## 代码说明

### 核心逻辑

- **任务 ID 管理**：通过 `reorganize_ids` 函数确保任务 ID 始终为连续序列。
- **状态验证**：使用 `is_valid_status` 函数验证任务状态是否合法。
- **时间记录**：每个任务包含 `createdAt` 和 `updatedAt` 时间戳，记录创建和更新时间。

### 命令行解析

- **`SupportedQueries` 类**：定义支持的命令及其参数。
- **`get_parser` 方法**：创建命令行解析器，动态添加子命令。

---

## 注意事项

- 任务数据存储在 `tasks.json` 文件中，请勿手动修改该文件。
- 删除任务后，任务 ID 会自动重新整理为连续序列。

---

## 当前代码不足

1. **任务描述更新功能缺失**：
   - 当前代码仅支持更新任务状态，无法更新任务描述。
   - 用户需要删除任务并重新添加才能修改描述。

2. **性能问题**：
   - 每次保存任务时都会重新整理 ID，可能导致性能问题，尤其是在任务数量较多时。

3. **用户交互体验不足**：
   - 命令行提示信息较为简单，未提供颜色或格式化输出。
   - 缺少对用户输入的验证（如任务描述为空时未处理）。

4. **功能扩展性有限**：
   - 当前功能较为基础，未支持任务优先级、截止日期等常见任务管理功能。

---

## 未来可优化方案(想做时才做)

1. **增强任务更新功能**：
   - 添加 `update-description` 命令，支持更新任务描述。
   - 示例：
     ```bash
     python task_manager.py update-description 1 "新的任务描述"
     ```

2. **优化性能**：
   - 仅在删除任务时整理 ID，而不是每次保存时都整理。
   - 使用更高效的数据结构（如列表）存储任务，减少字典操作的开销。

3. **提升用户交互体验**：
   - 使用 `rich` 或 `colorama` 库为命令行输出添加颜色和格式化。
   - 示例：
     ```bash
     ✅ Task added successfully (ID: 1)
     ```

4. **扩展任务管理功能**：
   - 添加任务优先级（高、中、低）。
   - 支持任务截止日期和提醒功能。
   - 示例：
     ```bash
     python task_manager.py add "完成报告" --priority high --due-date 2025-10-24
     ```

5. **添加数据备份功能**：
   - 自动备份任务数据，防止数据丢失。
   - 示例：
     ```bash
     python task_manager.py backup --output tasks_backup.json
     ```

6. **支持导入和导出**：
   - 支持从 CSV 或 JSON 文件导入任务。
   - 支持将任务导出为 CSV 或 JSON 文件。
   - 示例：
     ```bash
     python task_manager.py import --file tasks.csv
     python task_manager.py export --file tasks_export.json
     ```

7.  **添加命令行补全**：
    - 使用 `argcomplete` 实现命令行参数自动补全，提升用户体验。
    - 示例：
      ```bash
      python task_manager.py upd<TAB>  # 自动补全为 'update'
      ```

---
