def input_integer(message: str):
    result = 0

    no_problem = False
    while not no_problem:
        no_problem = True

        try:
            result = int(input(message))
        except ValueError:
            print("Please enter a valid integer.")
            no_problem = False
    
    return result


def input_specific_string(message: str, valid_options: list[str], case_sensitive=False):
    result = ""

    no_problem = False
    while not no_problem:
        no_problem = True

        result = input(message)

        check_result = result if case_sensitive else result.lower()
        check_options = valid_options if case_sensitive else [option.lower() for option in valid_options]

        if check_result not in check_options:
            print("Please enter one of the following options: " + ", ".join(valid_options))
            no_problem = False
    
    return result


def yes_or_no(string: str):
    result = input_specific_string(string, ["y", "n"])
    return result.lower() == "y"