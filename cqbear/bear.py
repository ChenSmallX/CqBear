# -*- coding=utf-8 -*-
"""
TODO:
"""

import time
import requests
import threading

from flask import Flask, request as flask_request
from cqbear.roar import Roar
from cqbear.sound import BaseSound, SoundUnderstander
from cqbear.util import stop_thread

import logging
werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel(logging.ERROR)


class BearEar(object):

    LISTEN = True
    IGNORE = False

    def __init__(self, addr, port, secret):
        self.addr = addr
        self.port = port
        self.secret = secret
        self.status = self.IGNORE

        self._sound_list = []
        self._understander = SoundUnderstander()
        self._thread = None

        self._ear = Flask(__name__)
        self._ear.add_url_rule(
            rule="/",
            endpoint=None,
            view_func=self._listen,
            methods=['POST'])

    def _listen(self):
        if self.is_listening:
            request_json_data = flask_request.get_json()
            sound = self._understander.understand(request_json_data)
            if sound and isinstance(sound, BaseSound):
                self._sound_list.append(sound)
                # print(f"insert a sound into list \n {sound}")
        return 'OK'

    def start_listen(self):
        self._thread = threading.Thread(
            target=self._ear.run,
            name="cqBear_ear_flask",
            kwargs={
                "host": self.addr,
                "port": self.port,
                "debug": False,
                "use_reloader": False
            }
        )

        if self._thread:
            self._thread.start()
        self.status = self.LISTEN
        print(f"bear ear listen at {self.addr}:{self.port}")

    def stop_listen(self):
        if self._thread.is_alive():
            stop_thread(self)
        if not self._thread.is_alive():
            self.status = self.IGNORE
            print("bear ear will ignore all sound")

    def clear_sound(self):
        self._sound_list.clear()

    @property
    def is_listening(self):
        return self.status and self._thread.is_alive()

    def get_sound(self):
        if not len(self._sound_list):
            return None
        sound = self._sound_list[0]
        del self._sound_list[0]
        return sound


class BearMouth(object):

    FREE = True
    SHUTUP = False

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self._base_url = f"http://{self.addr}:{self.port}"

        self._status = self.FREE

    @property
    def speakable(self):
        return self._status and True

    def free(self):
        self._status = self.FREE

    def shut_up(self):
        self._status = self.SHUTUP

    def speak(self, roar: Roar):
        if not self.speakable:
            return

        url = f'{self._base_url}/{roar.extend_url}'
        data = roar.speak_data

        rcv = requests.post(url=url, data=data)
        req_code = rcv.status_code
        req_content = rcv.content
        rcv.close()
        return req_code, req_content


class BearBrain(object):
    THINKING = True
    REST = False

    _react_map = {}

    def __init__(self, bear, listen_cb: callable,
                 speak_cb: callable, react_map: dict):
        self._bear = bear
        self._listen = listen_cb
        self._speak = speak_cb
        self._react_map.update(react_map)
        self._thread = None
        self._status = self.THINKING

    @property
    def status(self):
        return self._status and self._thread.is_alive()

    @status.setter
    def status(self, val: bool):
        if isinstance(val, bool):
            self._status = val

    def _think(self):
        while True:
            time.sleep(0.1)
            sound = self._listen()
            if sound and type(sound) != BaseSound:
                print(f"[GOT] [{type(sound)}] {sound.type_short}")
                react_cb_lst = self._react_map.get(type(sound))
                if react_cb_lst:
                    for cb in react_cb_lst:
                        cb(self._bear, sound)

    def start_think(self):
        self._thread = threading.Thread(
            target=self._think,
            name="cqBear_brain_think"
        )

        if self._thread:
            self._thread.start()
        self._status = self.THINKING
        print("bear brain start think")

    def stop_think(self):
        if self._thread.is_alive():
            stop_thread(self._thread)
        if not self._thread.is_alive():
            self.status = self.REST
            print("bear brain stop think")

    @classmethod
    def add_react(cls, sound: BaseSound, react: callable):
        if sound not in cls._react_map.keys():
            cls._react_map[sound] = [react]
        else:
            cls._react_map[sound].append(react)


class CqBear(object):
    """
    CqBear:
        Main, total entrence class of module cqbear.

    Using:
        bear = CqBear("127.0.0.1", 5701)
        bear.app().load("class.or.list.of.class")
        bear.start()
    """
    _react_map = {}

    def __init__(self, addr="localhost", port=5701, secret="",
                 cq_addr="localhost", cq_port=5700, qq=None):
        self.addr = addr
        self.port = port
        self.secret = secret

        self.cq_addr = cq_addr
        self.cq_port = cq_port

        self.qq = qq

        self.ear = BearEar(self.addr, self.port, self.secret)
        self.mouth = BearMouth(self.cq_addr, self.cq_port)
        self.brain = BearBrain(self, self.ear.get_sound,
                               self.mouth.speak, self._react_map)

    def start(self):
        self.mouth.free()
        self.ear.start_listen()
        self.brain.start_think()

    def stop(self):
        self.mouth.shut_up()
        self.ear.stop_listen()
        self.brain.stop_think()

    def reset(self):
        self.ear.clear_sound()

    # decorator func
    @classmethod
    def add_react(cls, sound_type: type):
        def warpper(react):
            if sound_type not in cls._react_map.keys():
                cls._react_map[sound_type] = [react]
            else:
                cls._react_map[sound_type].append(react)
            return react
        return warpper
