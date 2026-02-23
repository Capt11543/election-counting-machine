import logger as Logger


def input_integer(message: str, log=True):
    result = 0

    no_problem = False
    while not no_problem:
        no_problem = True

        user_input = input(message)
        Logger.log(message + user_input)

        try:
            result = int(user_input)
        except ValueError:
            Logger.log_and_print("Please enter a valid integer.")
            no_problem = False
    
    return result


def input_string(message: str, log=True):
    result = input(message)
    Logger.log(message + result)
    return result


def input_specific_string(message: str, valid_options: list[str], case_sensitive=False, log=True):
    result = ""

    no_problem = False
    while not no_problem:
        no_problem = True

        result = input(message)

        Logger.log(message + result)

        check_result = result if case_sensitive else result.lower()
        check_options = valid_options if case_sensitive else [option.lower() for option in valid_options]

        if check_result not in check_options:
            Logger.log_and_print("Please enter one of the following options: " + ", ".join(valid_options) + "(case " + "sensitive" if case_sensitive else "insensitive" + ")")
            no_problem = False
    
    return result


def yes_or_no(string: str, log=True):
    result = input_specific_string(string, ["y", "n"], False, log)
    return result.lower() == "y"