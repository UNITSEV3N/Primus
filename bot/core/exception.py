
class MemberExists(Exception):
    """If a member already exists in the server registry"""

    def __init__(self, message: str, member_name: str):
        super().__init__(message)
        self.member_name = member_name
        self.message = message

    def __str__(self):
        return f"{self.member_name}: {self.args[0]}"

class AuthorizationError(Exception):
    """If a member doesn't have the correct clearance"""

    def __init__(self, message: str, roles: list[str] = None):
        super().__init__(message)
        self.message = message
        self.roles = roles

    def __str__(self):
        return f"{self.args[0]}"

