# -*- coding=utf-8 -*-
import threading
import ctypes
import inspect


class DotDict(dict):
    """
    支持使用.操作来访问字典成员
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


def allSubclasses(c) -> list:
    subclassse = []
    process = [c]

    while len(process):
        curr = process.pop(0)
        subclassse.append(curr)
        process.extend(curr.__subclasses__())

    return subclassse


def stop_thread(thread: threading.Thread):
    tid = thread.ident
    exctype = SystemExit
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
