import re


class Helpers(object):
    """This class contains methods which are routinely used to avoid repetition"""

    def __init__(self):
        self.regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def email_valid(self, email):
        """A helper for validating emails"""
        if re.match(self.regex, email):
            return True
        else:
            return False
