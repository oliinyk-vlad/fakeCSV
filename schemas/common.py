import random
import string
import requests


class DataNotFound(Exception):
    pass


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def generate_row():
    r = requests.get('https://api.namefake.com/english-united-states/random/')
    if r.status_code == 200:
        return {
            "full_name": r.json()['name'],
            "email": f"{r.json()['email_u']}@{r.json()['email_d']}",
            "domain_name": r.json()['domain'],
            "phone_number": r.json()['phone_h'],
            "company_name": r.json()['company'],
            "address": r.json()['address']
        }
    else:
        raise DataNotFound


def generate_unreadable_row():
    return {
        "full_name": f"{random_string(random.randint(2, 16))} {random_string(random.randint(2, 16))}",
        "email": f"{random_string(random.randint(2, 16))}@"
                 f"{random_string(random.randint(2, 8))}."
                 f"{random_string(random.randint(2, 6))}",
        "domain_name": f"{random_string(random.randint(2, 8))}.{random_string(random.randint(2, 6))}",
        "phone_number": f"+{str(random.randint(0, 9)).zfill(12)}",
        "company_name": random_string(random.randint(5, 16)),
        "address": f"{random_string(random.randint(5, 16))}, {random.randint(1, 1000)}"
    }
