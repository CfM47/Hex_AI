def get_input(message: str, valid_inputs: dict) -> str or None:
    while True:
        print(message)
        for key in valid_inputs.keys():
            print(f"{valid_inputs[key]} [{key}]")
        user_input = input()

        if user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please try again.")
            print("Valid inputs are: ", valid_inputs)


def get_int_input(message: str, min_val: int, max_val: int) -> int or None:
    while True:
        print(message)
        user_input = input()

        try:
            user_input = int(user_input)
            if user_input < min_val or user_input > max_val:
                print(f"Input must be between {min_val} and {max_val}. Please try again.")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please try again.")
