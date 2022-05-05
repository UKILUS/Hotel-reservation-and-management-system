# -*- coding:utf-8 -*-
import json
class HttpCode(object):
    success = 0
    error = 1


def result(code=HttpCode.success, message='', data=None, kwargs=None, count=None):
    json_dict = {'data': data, 'code': code, 'message': message, 'count':count}
    print(json_dict)
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return json.dumps(json_dict)


def success(data=None):
    return result(code=HttpCode.success, message='OK', data=data)


def success_by_count(data=None, count=""):
    return result(code=HttpCode.success, message='OK', data=data, count=count)


def error(message='', data=None):
    return result(code=HttpCode.error, message=message, data=data)