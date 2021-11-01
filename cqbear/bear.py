# -*- coding=utf-8 -*-
"""
TODO:
"""

import time
from typing import Callable, Dict, Optional
import requests
import threading

from flask import Flask, request as flask_request
from cqbear.remember import Job, Remember
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

        self.__sound_list = []
        self.__understander = SoundUnderstander()
        self.__think_thread = None

        # TODO:
        # replace the flask http server to
        # hand-write, socket-based http server
        self._ear = Flask(__name__)
        self._ear.add_url_rule(
            rule="/",
            endpoint=None,
            view_func=self.__listen,
            methods=['POST'])

    def __listen(self):
        if self.is_listening:
            request_json_data = flask_request.get_json()
            sound = self.__understander.understand(request_json_data)
            if sound and isinstance(sound, BaseSound):
                self.__sound_list.append(sound)
                # print(f"insert a sound into list \n {sound}")
        return 'OK'

    def start_listen(self):
        self.__think_thread = threading.Thread(
            target=self._ear.run,
            name="cqBear_ear_flask",
            kwargs={
                "host": self.addr,
                "port": self.port,
                "debug": False,
                "use_reloader": False
            }
        )

        if self.__think_thread:
            self.__think_thread.start()
        self.status = self.LISTEN
        print(f"bear ear listen at {self.addr}:{self.port}")

    def stop_listen(self):
        if self.__think_thread.is_alive():
            stop_thread(self)
        if not self.__think_thread.is_alive():
            self.status = self.IGNORE
            print("bear ear will ignore all sound")

    def clear_sound(self):
        self.__sound_list.clear()

    @property
    def is_listening(self):
        return self.status and self.__think_thread.is_alive()

    def get_sound(self) -> Optional[BaseSound]:
        if not len(self.__sound_list):
            return None
        sound = self.__sound_list[0]
        del self.__sound_list[0]
        return sound

    def ignore_sound(self):
        self.status = self.IGNORE

    def listen_sound(self):
        self.status = self.LISTEN


class BearMouth(object):

    FREE = True
    SHUTUP = False

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self._base_url = f"http://{self.addr}:{self.port}"

        self.__status = self.FREE

    @property
    def speakable(self):
        return self.__status and True

    def free(self):
        self.__status = self.FREE

    def shut_up(self):
        self.__status = self.SHUTUP

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

    __react_map = {}
    __remember: Optional[Remember] = None

    def __init__(self, bear, listen_cb: callable,
                 speak_cb: callable,
                 react_map: Dict[BaseSound, Callable],
                 remember_map: Dict[Job, Callable]):
        self.__bear = bear
        self.__listen = listen_cb
        self.__speak = speak_cb
        self.__react_map.update(react_map)
        self.__think_thread = None
        self.__remember_thread = None
        self.__status = self.THINKING
        self.__remember = Remember()

        for job, func in remember_map.items():
            self.add_remember(job, func)

    @property
    def status(self):
        return self.__status and self.__think_thread.is_alive()

    @status.setter
    def status(self, val: bool):
        if isinstance(val, bool):
            self.__status = val

    def _think(self):
        while True:
            time.sleep(0.1)
            sound = self.__listen()
            if sound and type(sound) != BaseSound:
                try:
                    print(f"[GOT] [{type(sound)}] <{sound.type_short}>: {sound.message}")
                except Exception:
                    pass
                react_cb_lst = self.__react_map.get(type(sound))
                if react_cb_lst:
                    for cb in react_cb_lst:
                        try:
                            cb(self.__bear, sound)
                        except Exception as e:
                            print(e)

    def start_think(self):
        self.__think_thread = threading.Thread(
            target=self._think,
            name="cqBear_brain_think"
        )
        if self.__think_thread:
            self.__think_thread.start()

        self.__remember_thread = threading.Thread(
            target=self.__remember.parallel_run,
            name="cqBear_brain_remember"
        )
        if self.__remember_thread:
            self.__remember_thread.start()

        if self.__think_thread.is_alive() and \
           self.__remember_thread.is_alive():
            self.__status = self.THINKING
        elif not self.__think_thread.is_alive():
            raise Exception("bear thinking thread running failed")
        elif not self.__remember_thread.is_alive():
            raise Exception("bear remember thread running failed")
        print("bear brain start think")

    def stop_think(self):
        if self.__think_thread.is_alive():
            stop_thread(self.__think_thread)
        if self.__remember_thread.is_alive():
            self.__remember.pause()
            self.__remember_thread.join()
            stop_thread(self.__remember_thread)
        if not self.__think_thread.is_alive() and \
           not self.__remember_thread.is_alive():
            self.status = self.REST
            print("bear brain stop think")

    def add_react(self, sound: BaseSound, react: callable):
        if sound not in self.__react_map.keys():
            self.__react_map[sound] = [react]
        else:
            self.__react_map[sound].append(react)

    def add_remember(self, job: Job, func: Callable):
        if not self.__remember:
            self.__remember = Remember()
        job.to_do(func, self.__bear).bind_remember(self.__remember)


class CqBear(object):
    """
    CqBear:
        Main, total entrence class of module cqbear.

    Using:
        bear = CqBear("127.0.0.1", 5701)
        bear.app().load("class.or.list.of.class")
        bear.start()
    """
    __react_map = {}
    __remember_list = {}

    def __init__(self, addr="localhost", port=5701, secret="",
                 cq_addr="localhost", cq_port=5700, qq=None):
        self.addr = addr
        self.port = port
        self.secret = secret

        self.cq_addr = cq_addr
        self.cq_port = cq_port

        self.qq = qq

        self.__ear = BearEar(self.addr, self.port, self.secret)
        self.mouth = BearMouth(self.cq_addr, self.cq_port)
        self.brain = BearBrain(self, self.__ear.get_sound,
                               self.mouth.speak,
                               self.__react_map, self.__remember_list)

    def start(self):
        self.mouth.free()
        self.__ear.start_listen()
        self.brain.start_think()

    def stop(self):
        self.mouth.shut_up()
        self.__ear.stop_listen()
        self.brain.stop_think()

    def reset(self):
        self.__ear.clear_sound()

    # decorator func
    @classmethod
    def add_react(cls, sound_type: type):
        def warpper(react):
            if sound_type not in cls.__react_map.keys():
                cls.__react_map[sound_type] = [react]
            else:
                cls.__react_map[sound_type].append(react)
            return react
        return warpper

    @classmethod
    def add_remember(cls, job: Job):
        def warpper(react):
            if job not in cls.__remember_list.keys():
                cls.__remember_list[job] = react
            return react
        return warpper

    # the ear encapsulat

    def ear_clear_sound(self):
        self.__ear.clear_sound()

    def ear_is_listening(self) -> bool:
        return self.__ear.is_listening

    def ear_get_sound(self):
        return self.__ear.get_sound()

    def ear_ignore_sound(self):
        self.__ear.ignore_sound()

    def ear_listen_sound(self):
        self.__ear.listen_sound()
