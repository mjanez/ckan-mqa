# inbuilt libraries
import logging
import logging.handlers
import os
from datetime import datetime


# Logging
def log_file(log_folder):
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

    logging.basicConfig(
                        handlers=[logging.FileHandler(filename=log_folder + "/ckan2mqa-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log", encoding='utf-8', mode='a+')],
                        format="%(asctime)s %(levelname)s::%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", 
                        level=logging.INFO
                        )
    
    log_files = os.listdir(log_folder)
    log_files = [f for f in log_files if f.endswith('.log')]

    # sort the list of log files by modification date
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_folder, x)))

    # delete all old log files except for the 3 most recent ones
    for log_file in log_files[:-3]:
        os.remove(os.path.join(log_folder, log_file))

    return logger