# Folder Synchronization Tool

This is a Python script that synchronizes two folders, ensuring that the contents of the replica folder exactly match those of the source folder. It performs one-way synchronization from source to replica, creating, updating, and deleting files and directories in the replica to match the source. The tool also logs all synchronization actions to a specified log file and outputs them to the console for easy monitoring.

## Features

- **One-way Synchronization**: Ensures that the replica folder is an exact copy of the source folder.
- **File Operations**: 
    - Creates new files and directories in the replica that are present in the source.
    - Updates files in the replica if they have been modified in the source.
    - Deletes files and directories from the replica if they no longer exist in the source.
- **Logging**: Logs all file creation, update, and deletion actions to both the console and a specified log file.
- **Periodic Synchronization**: Runs continuously, synchronizing at a user-defined interval until manually stopped.

## Prerequisites

- Python 3.x
- No external dependencies required; this script uses only standard Python libraries.

## Usage

### Command-line Arguments

The script takes the following command-line arguments:

| Argument      | Description                                          | Example                   |
|---------------|------------------------------------------------------|---------------------------|
| `--source`    | Path to the source folder to be synchronized         | `--source /path/to/source`|
| `--replica`   | Path to the replica folder that mirrors the source   | `--replica /path/to/replica` |
| `--log_file`  | Path to the directory where the log file is created  | `--log_file /path/to/log` |
| `--interval`  | Synchronization interval in seconds                  | `--interval 60`           |

### Running the Script

**Basic Execution**: Run the script with the specified arguments as follows:
    ```sh
    python main.py --source /path/to/source --replica /path/to/replica --log_file /path/to/log --interval 60
    ```

   This will synchronize `/path/to/source` to `/path/to/replica` every 60 seconds, logging all actions in the specified log file.
