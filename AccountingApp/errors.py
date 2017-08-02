class AppErrors(Exception):
    def __init__(self, message):
        self.message = message


class AccountsAreNotBalanced(AppErrors):
    pass


