# In python, special built-in attributes of a module are provided
import logging

# logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler() # handler is responsible of telling the logger where to send the logs to; logging.StreamHandler sets the location to sys.stdout/ sys.stderr
logger = logging.getLogger(__name__) # if called when script is executed, interpreter prints the output with the logger's __name__
logger.addHandler(handler)
logger.setLevel(logging.INFO) # info level needs to be set, as logs are only printed for warn msgs by default

__file__
__name__

def main():
    print("main is executing")

if __name__ == "__main__":
    # when running a python script, the interpreter assigns the value "__main__" to the __name__ variable
    # if script is imported as a module, module name is set to the __name__ variable
    
    from pathlib import Path
    import os
    # 2 ways to set absolute paths
    absolute_path = (Path(__file__).resolve()) # way 1; can be Path("any_path")
    abs_path = os.path.abspath(__file__) # way 2

    # *this code here runs only when the script is not imported
    logger.info(f"Module {__name__} is executed")
    logger.info(f"It has file path {__file__}")