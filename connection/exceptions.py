class ServerException(Exception):

    def __init__(self, status_code: int, msg: str, errors: dict = None):
        self.msg = msg
        self.errors = errors
        self.status_code = status_code


class InvalidInputs(ServerException):

    def __init__(self):
        super().__init__(400, 'Invalid inputs.')


class Unauthorized(ServerException):

    def __init__(self):
        super().__init__(403, 'Unauthorized access.')


class FlowAlreadyExists(ServerException):

    def __init__(self, flow_id: str):
        super().__init__(400, f'Flow: {flow_id}, already exists.')
        self.flow_id = flow_id


class FlowNotFound(ServerException):

    def __init__(self, flow_id: str):
        super().__init__(404, f'Flow: {flow_id} not found.')
        self.log_id = flow_id


class InvalidStatus(ServerException):

    def __init__(self, status: str):
        super().__init__(400, f'Invalid state: {status}.')
        self.status = status


class WhoisError(ServerException):

    def __init__(self):
        super().__init__(400, 'Name or Service not known.')