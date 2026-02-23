from datetime import datetime


log_file_path = ""


# Open a file, write the current date and time, close the file
def initialize():
    global log_file_path

    # Set the log file path name to the current date and time
    log_file_path = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "_vote_count.txt"

    try:
        with open(log_file_path, 'w') as log_file:
            log_file.write("===ELECTION COUNTING MACHINE===\n")
            log_file.write(str(datetime.now()) + "\n\n\n")
    except Exception as e:
        print("Error initializing log file: " + str(e))


def log(message: str):
    if log_file_path == "":
        print("No log file path provided!")
        return

    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(message + "\n")
    # handle an exception if the file does not exist
    except FileNotFoundError:
        print("Log file " + log_file_path + " not found!")
    except Exception as e:
        print("Error writing to log file: " + str(e))


def log_and_print(message: str):
    print(message)
    log(message)