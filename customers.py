"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self,
                 firstname,
                 lastname,
                 email,
                 password):

        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __repr__(self):
        """ Convenience method to show information about customer in console"""

        return "<Customer name: {} {}, email: {}, password: {}".format(
                                self.firstname,
                                self.lastname,
                                self.email,
                                self.password)


def read_customer_from_file(filepath):
    """Read customer data and popular dictionary of customer info.

    Dictionary will be {email: Customer object}
    """

    customer_info = {}

    file_obj = open(filepath)

    for line in file_obj:
        (firstname,
         lastname,
         email,
         password) = line.strip().split("|")

        customer_info[email] = Customer(firstname,
                                        lastname,
                                        email,
                                        password)

    return customer_info

# globally defined customer_info dictionary

customer_info = read_customer_from_file("customers.txt")


def get_by_email(email):
    """Return the customer object, given the email"""

    # access globally defined dictionary customer_info

    customer = customer_info[email]

    return customer












