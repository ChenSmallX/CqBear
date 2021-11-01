# -*- coding=utf-8 -*-

import datetime

from cqbear.bear import CqBear
from cqbear.remember import every
from cqbear.roar import (
    SendPrivateMessage,
    SendGroupMessage
)
from cqbear.sound import (
    FriendPrivateMessage,
    NormalGroupMessage
)
from cqbear.sentence import At

FRIEND_ID = 6666
GROUP_ID = 8888
SELF_ID = 2222


def check_group_msg(msg: NormalGroupMessage, group_id: int) -> bool:
    return msg.group_id == group_id


def check_friend_msg(msg: FriendPrivateMessage, user_id: int) -> bool:
    return msg.user_id == user_id


@CqBear.add_react(NormalGroupMessage)
def reply_group(bear: CqBear, msg: NormalGroupMessage):
    """
    监听并回复群消息
    """
    if check_group_msg(msg, GROUP_ID) and \
       At().set_user_id(SELF_ID).has_me(msg.raw_message):
        roar = SendGroupMessage()
        roar.set_group_id(msg.group_id)
        roar.set_message("this is an example message")

        bear.mouth.speak(roar)


@CqBear.add_react(FriendPrivateMessage)
def reply_friend(bear: CqBear, msg: FriendPrivateMessage):
    """
    监听并回复好友信息
    """
    if check_friend_msg(msg, FRIEND_ID):
        roar = SendPrivateMessage()
        roar.set_user_id(msg.user_id)
        roar.set_message("this is an example message")

        bear.mouth.speak(roar)


@CqBear.add_remember(every(1).hour.at("0:0:0"))
def punctually_per_hour(bear: CqBear):
    now = datetime.datetime.now()
    roar = SendGroupMessage()
    roar.set_group_id(GROUP_ID)
    roar.set_message(f"now is {now.hour} o'clock!")

    bear.mouth.speak(roar)
