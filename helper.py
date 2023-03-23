import string

def make_friendly(customer):
    # Replace underscore with space
    # Make first letter of each word uppercase
    customerFriendly = string.capwords(customer.replace("_", " "))
    return customerFriendly