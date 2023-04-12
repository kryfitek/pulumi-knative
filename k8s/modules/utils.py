class Util:
    def __init__(self, prefix, postfix) -> None:
        self.prefix = prefix
        self.postfix = postfix

    def generateResourceName(self, name):
        return f"{self.prefix}-{name}-{self.postfix}"