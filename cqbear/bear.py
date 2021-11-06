# -*- coding=utf-8 -*-
"""
TODO:
"""

import time
from typing import (
    Callable, Dict, List, Optional,
    Tuple, Union
)
import requests
import threading
import socket
import json

from flask import Flask, request as flask_request
from cqbear.remember import Job, Remember
from cqbear.roar import (
    CheckCanSendImage, CheckCanSendVoiceRecord,
    CheckUrlSafely, GetFriendList, GetGroupList,
    GetGroupMemberList, GetMessage, GetOnlineClient,
    GetStatus, GetVersionInfo, GetVipInfo,
    RestartCqhttpServer, Roar, getLoginInfo
)
from cqbear.sound import Sound, SoundUnderstander
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
            if sound and isinstance(sound, Sound):
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

    def get_sound(self) -> Optional[Sound]:
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

    def speak(self, roar: Roar) -> Tuple[
        int,
        Optional[Union[dict, list]]
    ]:
        if not self.speakable:
            return

        url = f'{self._base_url}/{roar.extend_url}'
        data = roar.speak_data

        rcv = requests.post(url=url, data=data)
        req_code = rcv.status_code
        req_content = rcv.content
        rcv.close()

        if req_code != 200:
            return req_code, req_content

        j_req = json.loads(req_content)
        j_req_code = int(j_req.get("retcode", -1))
        j_req_status = j_req.get("status", "fail")
        j_req_data = j_req.get("data")

        if not j_req_code == 0 or not j_req_status == "ok":
            return j_req_code, j_req

        return j_req_code, j_req_data


class BearBrain(object):
    THINKING = True
    REST = False

    __react_map = {}
    __remember: Optional[Remember] = None

    def __init__(self, bear, listen_cb: Callable,
                 speak_cb: Callable,
                 react_map: Dict[Sound, List[Callable]],
                 remember_map: Dict[Job, Callable]):
        self.__bear = bear
        self.__listen = listen_cb
        self.__speak = speak_cb
        self.__react_map.update(react_map)
        self.__think_thread = None
        self.__remember_thread = None
        self.__status = self.REST
        self.__remember = Remember()

        for job, func in remember_map.items():
            self.add_remember(job, func)

    @property
    def is_thinking(self):
        return self.__status and \
               self.__think_thread.is_alive() and \
               self.__remember_thread.is_alive()

    def _think(self):
        while True:
            time.sleep(0.1)
            sound = self.__listen()
            if sound and type(sound) != Sound:
                try:
                    print(f"[GOT] [{type(sound)}] <{sound.type_short}>: {sound.message}")
                except Exception:
                    pass
                react_cb_lst = []
                for key in self.__react_map.keys():
                    if isinstance(sound, key):
                        react_cb_lst.extend(self.__react_map[key])
                if react_cb_lst:
                    for cb in react_cb_lst:
                        try:
                            cb(self.__bear, sound)
                        except Exception as e:
                            print(e)

    def start_think(self):
        if self.is_thinking:
            return

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
            self.__status = self.REST
            print("bear brain stop think")

    def add_react(self, sound: Sound, react: Callable):
        if sound not in self.__react_map.keys():
            self.__react_map[sound] = [react]
        else:
            self.__react_map[sound].append(react)

    def add_remember(self, job: Job, func: Optional[Callable] = None):
        if not self.__remember:
            self.__remember = Remember()

        if not job.runable and func is None:
            raise Exception("added Job must with a callable function or use Job.to_do make it RUNABLE")

        if not job.runable and func is not None:
            job.to_do(func, self.__bear)
        if job.runable:
            job.bind_remember(self.__remember)


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

    def __init__(self, addr: str = "localhost", port: int = 5701, secret="",
                 cq_addr: str = "localhost", cq_port: int = 5700, qq: int = None):
        self.addr = addr
        self.port = port
        self.secret = secret

        self.cq_addr = cq_addr
        self.cq_port = cq_port

        self.qq = qq

        self.__ear = BearEar(self.addr, self.port, self.secret)
        self.__mouth = BearMouth(self.cq_addr, self.cq_port)
        self.__brain = BearBrain(self, self.__ear.get_sound,
                                 self.__mouth.speak,
                                 self.__react_map, self.__remember_list)

    def start(self):
        self.__mouth.free()
        self.__ear.start_listen()
        self.__brain.start_think()

    def stop(self):
        self.__mouth.shut_up()
        self.__ear.stop_listen()
        self.__brain.stop_think()

    # TODO: looking for the reason of reset method

    # decorator func
    @classmethod
    def react(cls, sound_type: type):
        def warpper(react):
            if sound_type not in cls.__react_map.keys():
                cls.__react_map[sound_type] = [react]
            else:
                cls.__react_map[sound_type].append(react)
            return react
        return warpper

    @classmethod
    def remember(cls, job: Job):
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

    # the brain envapsulat
    def brain_is_thinking(self):
        return self.__brain.is_thinking

    def add_react(self, sound: Sound, react: Callable):
        self.__brain.add_react(sound, react)

    def add_remember(self, job: Job, react: Optional[Callable] = None):
        self.__brain.add_remember(job, react)

    def brain_stop_think(self):
        self.__brain.stop_think()

    def brain_start_think(self):
        if not self.__brain.is_thinking:
            self.__brain.start_think()

    # the mouth encapsulat
    def speak(self, roar: Roar):
        """
        Return:
            int: response code
            data: json-loaded dict data
        """
        return self.__mouth.speak(roar)

    def mouth_shutup(self):
        self.__mouth.shut_up()

    def mouth_free(self):
        self.__mouth.free()

    def mouth_speakable(self):
        return self.__mouth.speakable

    # TODO: add the build-in roar call

    def gocqhttp_online(self):
        """check the cqhttp server online status

        Return:
            -> bool: `True` online `False` offline
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.cq_addr, int(self.cq_port)))
        sock.close()
        return result == 0

    def login_info(self):
        """get login bear basic info::

        {
            'user_id': str,
            'nickname': str
        }
        """
        if self.gocqhttp_online():
            roar = getLoginInfo()
            _, ret = self.speak(roar)
            if ret:
                self.qq = ret.get("user_id")
                self.nickname = ret.get("nickname")

            return ret

    def get_friend_list(self):
        if self.gocqhttp_online():
            roar = GetFriendList()
            _, ret = self.speak(roar)
            if ret:
                self.__friend_list = ret
            return ret

    @property
    def friend_list(self):
        return self.__friend_list if self.__friend_list else self.get_friend_list()

    def get_group_list(self):
        if self.gocqhttp_online():
            roar_group_list = GetGroupList()
            _, groups = self.speak(roar_group_list)
            if groups:
                for group in groups:
                    group_id = int(group.get("group_id", 0))
                    if group_id:
                        roar_group_members = GetGroupMemberList().set_group_id(group_id)
                        _, members = self.speak(roar_group_members)
                        group['member_list'] = members
                self.__group_list = groups
                return groups

    @property
    def group_list(self):
        return self.__group_list if self.__group_list else self.get_group_list()

    @property
    def can_send_image(self):
        if self.gocqhttp_online():
            roar = CheckCanSendImage()
            _, ret = self.speak(roar)
            if ret:
                return bool(ret.get("yes", False))
        return False

    @property
    def can_send_voice(self):
        if self.gocqhttp_online():
            roar = CheckCanSendVoiceRecord()
            _, ret = self.speak(roar)
            if ret:
                return bool(ret.get("yes", False))
        return False

    def get_version_info(self):
        if self.gocqhttp_online():
            roar = GetVersionInfo()
            _, ret = self.speak(roar)
            if ret:
                self.__version_info = ret
                return ret

    @property
    def version_info(self):
        return self.__version_info if self.__version_info else self.get_version_info()

    def restart_gocqhttp(self, delay_ms=1000):
        """"""
        if self.gocqhttp_online():
            roar = RestartCqhttpServer().set_delay_ms(delay_ms)
            self.speak(roar)

    def get_cqhttp_status(self):
        if self.gocqhttp_online():
            roar = GetStatus()
            _, ret = self.speak(roar)
            if ret:
                self.__cqhttp_status = ret
                return ret

    @property
    def cqhttp_status(self):
        return self.__cqhttp_status if self.__cqhttp_status else self.get_cqhttp_status()

    def get_vip_info(self, user_id: int = None):
        if self.gocqhttp_online():
            roar = GetVipInfo()
            roar.set_user_id(user_id if user_id else self.qq)
            _, ret = self.speak(roar)
            if ret:
                if not user_id:
                    self.__vip_info = ret
                return ret

    @property
    def vip_info(self):
        return self.__vip_info if self.__vip_info else self.get_vip_info()

    def get_online_client(self):
        if self.gocqhttp_online():
            roar = GetOnlineClient().set_no_cache(True)
            _, clients = self.speak(roar)
            if clients:
                return clients
        return []

    @property
    def online_client(self):
        return self.get_online_client()

    def is_url_safely(self, url: str) -> bool:
        if self.gocqhttp_online():
            roar = CheckUrlSafely().set_url(url)
            _, ret = self.speak(roar)
            return 1 == ret.get("level", 2)
        return False

    def get_message(self, msg_id: int):
        """get message by id
        """
        if self.gocqhttp_online():
            roar = GetMessage().set_message_id(msg_id)
            _, msg = self.speak(roar)
            if msg:
                return msg
