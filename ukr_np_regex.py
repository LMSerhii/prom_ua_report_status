import re


def regex_np(ttn):
    """ находит совпадения с 14-ти значным кодом ттн новой почты"""
    ttn_num_regex = re.compile(r'\d{14}')
    data = f"{ttn}"
    mo = ttn_num_regex.match(data)

    return mo


def regex_ukr(ttn):
    """ находит совпадения с 13-ти значным кодом ттн укр-почты """
    ttn_num_regex = re.compile(r'\d{13}')
    data = f"{ttn}"
    mo = ttn_num_regex.match(data)

    return mo


def main():

    search_number = input("Input number: ")

    if regex_np(ttn=search_number):
        print("You find match in Nova Poshta")
    elif regex_ukr(ttn=search_number):
        print("You find match in Ukrposhta")

    # print(regex_np(ttn=search_number))
    # print(regex_ukr(ttn=search_number))


if __name__ == '__main__':
    main()