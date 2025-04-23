from string import ascii_letters


def check_password(value):
    numbers = []
    letters = []
    for elem in value:
        if elem.isdigit():
            numbers.append(elem)
        elif elem.isalpha():
            if elem not in ascii_letters:
                return False
            letters.append(elem)
    return numbers and lettrs