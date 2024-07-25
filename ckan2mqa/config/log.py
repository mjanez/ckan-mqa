# inbuilt libraries
import logging
import logging.handlers
import os
from datetime import datetime


def log_file(log_folder, debug_mode=False):
    '''
    Starts the logger --log_folder parameter entered
    
    Parameters
    ----------
    - log_folder: Folder where log is stored 

    Return
    ----------
    Logger object
    '''
    logger = logging.getLogger()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_level = logging.DEBUG if debug_mode else logging.INFO

    logging.basicConfig(
                        handlers=[logging.FileHandler(filename=log_folder + "/ckan2mqa-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log", encoding='utf-8', mode='a+')],
                        format="%(asctime)s %(levelname)s::%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", 
                        level=log_level
                        )
    
    log_files = os.listdir(log_folder)
    log_files = [f for f in log_files if f.endswith('.log')]

    # sort the list of log files by modification date
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_folder, x)))

    # delete all old log files except for the 3 most recent ones
    for log_file in log_files[:-3]:
        os.remove(os.path.join(log_folder, log_file))

    return logger

def get_log_module():
    # Get the directory and file name of the current file
    dir_path, file_name_ext = os.path.split(os.path.abspath(__file__))
    
    # Split the file name and extension
    file_name, file_ext = os.path.splitext(file_name_ext)

    # Create the log module string
    log_module = f"[{os.path.basename(dir_path)}.{file_name}]"
    
    return log_module