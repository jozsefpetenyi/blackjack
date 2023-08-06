class DidNotFindCardException(BaseException):
    def __init__(self, *args, **kwargs):
        pass

class IRunOutOfChipsException(BaseException):
    def __init__(self, *args, **kwargs):
        pass

class LogicError(BaseException):
    def __init__(self, *args, **kwargs):
        pass

class ActionIsAgainstTheRulesError(BaseException):
    def __init__(self, *args, **kwargs):
        pass