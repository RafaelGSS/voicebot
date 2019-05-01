from app.interpreter.response_code import ResponseCode
from ast import literal_eval


class BuilderResponse(object):
    base_response = '{{ "action": \"{0}\", "value": \"{1}\" }}'
    base_response_ask_again = '{{ "action": \"{0}\" }}'

    def __init__(self):
        pass

    @staticmethod
    def get_response(status, value):
        if status == ResponseCode.NEXT:
            return literal_eval(BuilderResponse.base_response.format("NEXT", value))
        if status == ResponseCode.ASK_STATE:
            return literal_eval(BuilderResponse.base_response.format("ASK_STATE", ','.join(str(x) for x in value)))
        if status == ResponseCode.ASK_AGAIN:
            return literal_eval(BuilderResponse.base_response_ask_again.format("ASK_AGAIN"))
