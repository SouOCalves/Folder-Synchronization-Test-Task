"""
Folder Synchronization Script

This script synchronizes two folders, a `source` and a `replica`, so that the
replica is an exact mirror of the source. The synchronization is performed
at regular intervals specified by the user.

Features:
    - Creates new files and directories in the `replica` that are present in the `source`.
    - Updates files in `replica` that have been modified in `source`.
    - Deletes files and directories from `replica` if they no longer exist in `source`.
    - Logs all synchronization actions (creation, updating, and deletion of files/directories)
      to a specified log file and outputs them to the console.

Usage:
    Run the script with the following command-line arguments:
    
    ```
    python main.py --source /path/src --replica /path/replica --log_file /path/log --interval 60
    ```

    Command-line Arguments:
        --source (str): Path to the source folder to mirror.
        --replica (str): Path to the replica folder that will be synchronized with the source.
        --log_file (str): Path to the directory where the log file will be created.
        --interval (int): Interval in seconds at which synchronization occurs.

Notes:
    - The script continues synchronizing until manually stopped, with each iteration separated
      by the specified interval.
    - The synchronization process can be terminated gracefully with a KeyboardInterrupt (Ctrl+C).

Requirements:
    - Built-in libraries: argparse, logging, os, shutil, time, datetime, and pathlib.
"""

import argparse
import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

def replicate_source(source: str, replica: str, interval: int) -> None:
    """
    Traverses both the source folder and the replica folder and adds, updates and deletes files
    and folders so that the replica folder is synchronized with the source folder.

    Parameters:
        source (str): Path to the source folder.
        replica (str): Path to the replica folder.
        interval (int): Time interval between synchronizations in seconds.

    """
    # Traverse and copy/update files
    for root, dirs, files in os.walk(source):
        replica_path = root.replace(source, replica, 1)
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)
            logging.info("[%s] Created directory: %s", datetime.now(), replica_path)
            print(f"[{datetime.now()}]] Created directory: {replica_path}")
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_path, file)

            # Check if the file needs to be copied or updated
            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info("[%s] Created file: %s", datetime.now(), replica_file)
                print(f"[{datetime.now()}] Created file: {replica_file}")
            elif os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info("[%s] Updated file: %s", datetime.now(), replica_file)
                print(f"[{datetime.now()}] Updated file: {replica_file}")

    # Remove files and directories not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        source_path = root.replace(replica, source, 1)

        # Remove files in replica that are not in source
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_path, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info("[%s] Deleted file: %s", datetime.now(), replica_file)
                print(f"[{datetime.now()}] Deleted file: {replica_file}")

        # Remove directories in replica that are not in source
        for directory in dirs:
            replica_dir = os.path.join(root, directory)
            source_dir = os.path.join(source_path, directory)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logging.info("[%s] Deleted directory: %s", datetime.now(), replica_dir)
                print(f"[{datetime.now()}] Deleted directory: {replica_dir}")

    try:
        time.sleep(interval)
        replicate_source(source, replica, interval)
    except KeyboardInterrupt:
        print("Stopping synchronization...")

def main() -> None:
    """
    Parses command-line arguments and initiates the synchronization of two folders
    (`source` and `replica`). Ensures that `replica` maintains a mirrored copy of `source`
    and logs all synchronization actions.

    Command-line Arguments:
        source (str): Path to the source folder to mirror.
        replica (str): Path to the replica folder that will be synchronized with the source.
        log_file (str): Path to the directory where the log file will be created.
        interval (int): Interval in seconds at which synchronization occurs.

    Example Usage:
        python main.py --source /path/src --replica /path/replica --log_file /path/log --interval 60
    """
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("--source", type=str, help="Path to the source folder")
    parser.add_argument("--replica", type=str, help="Path to the replica folder")
    parser.add_argument("--log_file", type=str, help="Path to the log file")
    parser.add_argument("--interval", type=int, help="Synchronization interval in seconds")
    args = parser.parse_args()

    # Check if the paths exist
    if not Path(args.source).exists():
        print("The source directory path does not exist")
        return
    if not Path(args.replica).exists():
        print("The replica directory path does not exist")
        return
    if not Path(args.log_file).exists():
        print("The log file path does not exist")
        return

    logging.basicConfig(filename=os.path.join(args.log_file, "Log"), level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    replicate_source(args.source, args.replica, args.interval)

if __name__ == "__main__":
    main()
