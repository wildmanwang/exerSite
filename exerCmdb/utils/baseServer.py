class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None

class BaseService(object):
    def __init__(self):
        pass
