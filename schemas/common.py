from faker import Faker

fake = Faker()


def generate_field(field):
    if field == 'full_name':
        return fake.name()
    elif field == 'email':
        return fake.ascii_free_email()
    elif field == 'domain_name':
        return fake.domain_name()
    elif field == 'phone_number':
        return fake.phone_number()
    elif field == 'company_name':
        return fake.company()
    elif field == 'address':
        return fake.address()
