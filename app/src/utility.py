import string
import random

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

def generateID():
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.digits
    value = ''.join(random.choice(characters) for i in range(18))
    return int(value)