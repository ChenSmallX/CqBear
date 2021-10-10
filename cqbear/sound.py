# -*- coding=utf-8 -*-
"""
go-cqhttp 将事件分成了三种类型：
- 消息
- 提醒
- 请求

CqBear 将这些事件（event）称作 Sound ，比做 bear 听到的声音。
每个 Sound 都可能包括三个 type 用于标记和存储 go-cqhttp 上报的事件类型。

FIRST_TYPE SECOND_TYPE THIRD_TYPE
其中，FIRST_TYPE 对应事件中的 post_type，
SECOND_TYPE 对应 xxx_type，其中 xxx 是 FIRST_TYPE 的内容，例如 FIRST_TYPE 是 message，
    那么 SECOND_TYPE 就是 message_type 对应的字段，
THIRD_TYPE 对应 sub_type，用于更加细致地细分消息类型。

TODO:
从 群文件上传 继续丰富方法
"""

import sys

from cqbear.util import allSubclasses


class BaseSound(dict):
    FIRST_TYPE = None
    SECOND_TYPE = None
    THIRD_TYPE = None

    def __init__(self, data: dict):
        super(BaseSound, self).__init__(data)

    @property
    def type_short(self):
        t = "sound"
        for tp in [self.FIRST_TYPE, self.SECOND_TYPE, self.THIRD_TYPE]:
            t = t + f".{str(tp)}" if tp is not None else ""
        return t

    @property
    def time(self) -> int:
        return self.get(sys._getframe().f_code.co_name)


class Message(BaseSound):
    FIRST_TYPE = "message"

    def __init__(self, data: dict):
        super(Message, self).__init__(data)

    @property
    def message_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)


class PrivateMessageSender(dict):
    def __init__(self, data: dict):
        super(PrivateMessageSender, self).__init__(data)

    @property
    def user_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def nickname(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sex(self) -> str:
        """
        male or female or unknown
        """
        return self.get(sys._getframe().f_code.co_name)

    @property
    def age(self) -> int:
        return self.get(sys._getframe().f_code.co_name)


class PrivateMessage(Message):
    SECOND_TYPE = "private"

    def __init__(self, data: dict):
        super(PrivateMessage, self).__init__(data)

    class TEMP_SOURCE_TYPE():
        GROUP = 0
        """群聊"""
        QQ_CONSULT = 1
        """QQ咨询"""
        FIND = 2
        """查找"""
        QQ_MOVIE = 3
        """QQ电影"""
        HOT_CHAT = 4
        """热聊"""
        VERIFIVATION = 6
        """验证消息"""
        MUTIL_PERSON_CHAT = 7
        """多人聊天"""
        DATE = 8
        """约会"""
        CONTECT_BOOK = 9
        """通讯录"""

    @property
    def temp_source(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def message(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def raw_message(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def font(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sender(self) -> PrivateMessageSender:
        return PrivateMessageSender(
            self.get(sys._getframe().f_code.co_name, {}))


class FriendPrivateMessage(PrivateMessage):
    THIRD_TYPE = "friend"

    def __init__(self, data: dict):
        super(FriendPrivateMessage, self).__init__(data)


class GroupPrivateMessage(PrivateMessage):
    THIRD_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupPrivateMessage, self).__init__(data)


class GroupSelfPrivateMessage(PrivateMessage):
    THIRD_TYPE = "group_self"

    def __init__(self, data: dict):
        super(GroupSelfPrivateMessage, self).__init__(data)


class OtherPrivateMessage(PrivateMessage):
    THIRD_TYPE = "other"

    def __init__(self, data: dict):
        super(OtherPrivateMessage, self).__init__(data)


class GroupMessageAnonymous(dict):
    def __init__(self, data: dict):
        super(GroupMessageAnonymous, self).__init__(data)

    @property
    def id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def name(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def flag(self) -> str:
        return self.get(sys._getframe().f_code.co_name)


class GroupMessageSender(dict):
    def __init__(self, data: dict):
        super(GroupMessageSender, self).__init__(data)

    @property
    def user_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def nickname(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def card(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sex(self) -> str:
        """
        male or female or unknown
        """
        return self.get(sys._getframe().f_code.co_name)

    @property
    def age(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def area(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def level(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def role(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def title(self) -> str:
        return self.get(sys._getframe().f_code.co_name)


class GroupMessage(Message):
    SECOND_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupMessage, self).__init__(data)

    @property
    def group_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def anonymous(self) -> GroupMessageAnonymous:
        return GroupMessageAnonymous(
            self.get(sys._getframe().f_code.co_name, {}))

    @property
    def message(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def raw_message(self) -> str:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def font(self) -> int:
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sender(self) -> GroupMessageSender:
        return GroupMessageSender(self.get(sys._getframe().f_code.co_name, {}))


class NormalGroupMessage(GroupMessage):
    THIRD_TYPE = "normal"

    def __init__(self, data: dict):
        super(NormalGroupMessage, self).__init__(data)


class AnonymousGroupMessage(GroupMessage):
    THIRD_TYPE = "anonymous"

    def __init__(self, data: dict):
        super(AnonymousGroupMessage, self).__init__(data)


class NoticeGroupMessage(GroupMessage):
    THIRD_TYPE = "notice"

    def __init__(self, data: dict):
        super(NoticeGroupMessage, self).__init__(data)


class Notice(BaseSound):
    FIRST_TYPE = "notice"

    def __init__(self, data: dict):
        super(Notice, self).__init__(data)


class GroupUploadNotice(Notice):
    SECOND_TYPE = "group_upload"

    def __init__(self, data: dict):
        super(GroupUploadNotice, self).__init__(data)


class GroupAdminNotice(Notice):
    SECOND_TYPE = "group_admin"

    def __init__(self, data: dict):
        super(GroupAdminNotice, self).__init__(data)


class SetGroupAdminNotice(GroupAdminNotice):
    THIRD_TYPE = "set"

    def __init__(self, data: dict):
        super(SetGroupAdminNotice, self).__init__(data)


class UnsetGroupAdminNotice(GroupAdminNotice):
    THIRD_TYPE = "unset"

    def __init__(self, data: dict):
        super(UnsetGroupAdminNotice, self).__init__(data)


class GroupDecreaseNotice(Notice):
    SECOND_TYPE = "group_decrease"

    def __init__(self, data: dict):
        super(GroupDecreaseNotice, self).__init__(data)


class LeaveGroupDecreaseNotice(GroupDecreaseNotice):
    THIRD_TYPE = "leave"

    def __init__(self, data: dict):
        super(LeaveGroupDecreaseNotice, self).__init__(data)


class KickGroupDecreaseNotice(GroupDecreaseNotice):
    THIRD_TYPE = "kick"

    def __init__(self, data: dict):
        super(KickGroupDecreaseNotice, self).__init__(data)


class KickMeGroupDecreaseNotice(GroupDecreaseNotice):
    THIRD_TYPE = "kick_me"

    def __init__(self, data: dict):
        super(KickMeGroupDecreaseNotice, self).__init__(data)


class GroupIncreaseNotice(Notice):
    SECOND_TYPE = "group_increase"

    def __init__(self, data: dict):
        super(GroupIncreaseNotice, self).__init__(data)


class ApproveGroupIncreaseNotice(GroupIncreaseNotice):
    THIRD_TYPE = "approve"

    def __init__(self, data: dict):
        super(ApproveGroupIncreaseNotice, self).__init__(data)


class InviteGroupIncreaseNotice(GroupIncreaseNotice):
    THIRD_TYPE = "invite"

    def __init__(self, data: dict):
        super(InviteGroupIncreaseNotice, self).__init__(data)


class GroupBanNotice(Notice):
    SECOND_TYPE = "group_ban"

    def __init__(self, data: dict):
        super(GroupBanNotice, self).__init__(data)


class FriendAddNotice(Notice):
    SECOND_TYPE = "friend_add"

    def __init__(self, data: dict):
        super(FriendAddNotice, self).__init__(data)


class GroupRecallNotice(Notice):
    SECOND_TYPE = "group_recall"

    def __init__(self, data: dict):
        super(GroupRecallNotice, self).__init__(data)


class FriendRecallNotice(Notice):
    SECOND_TYPE = "friend_recall"

    def __init__(self, data: dict):
        super(FriendRecallNotice, self).__init__(data)


class Notify(Notice):
    SECOND_TYPE = "notify"

    def __init__(self, data: dict):
        super(Notify, self).__init__(data)


class GroupCardNotice(Notice):
    SECOND_TYPE = "group_card"

    def __init__(self, data: dict):
        super(GroupCardNotice, self).__init__(data)


class OfflineFileNotice(Notice):
    SECOND_TYPE = "offline_file"

    def __init__(self, data: dict):
        super(OfflineFileNotice, self).__init__(data)


class ClientStatusNotice(Notice):
    SECOND_TYPE = "client_status"

    def __init__(self, data: dict):
        super(ClientStatusNotice, self).__init__(data)


class EssenceNotice(Notice):
    SECOND_TYPE = "essence"

    def __init__(self, data: dict):
        super(EssenceNotice, self).__init__(data)


class AddEssenceNotice(EssenceNotice):
    THIRD_TYPE = "add"

    def __init__(self, data: dict):
        super(AddEssenceNotice, self).__init__(data)


class DeleteEssenceNotice(EssenceNotice):
    THIRD_TYPE = "delete"

    def __init__(self, data: dict):
        super(DeleteEssenceNotice, self).__init__(data)


class Request(BaseSound):
    FIRST_TYPE = "request"

    def __init__(self, data: dict):
        super(Request, self).__init__(data)


class FriendRequest(Request):
    SECOND_TYPE = "friend"

    def __init__(self, data: dict):
        super(FriendRequest, self).__init__(data)


class GroupRequest(Request):
    SECOND_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupRequest, self).__init__(data)


class SoundUnderstander:
    _understand_map = {
        "default": BaseSound
    }

    def __init__(self):
        cls_lst = allSubclasses(BaseSound)
        for cls in cls_lst:
            if cls == BaseSound:
                continue
            key = self._get_key(clas=cls)
            self._understand_map[key] = cls

    def understand(self, data: dict) -> BaseSound:
        key = self._get_key(data=data)
        cls = self._understand_map.get(key, BaseSound)
        return cls(data)

    def _get_key(self, data=None, clas=None) -> str:
        if not data and not clas:
            return None
        if data and clas:
            return None

        key = ""
        first_type = None
        second_type = None
        third_type = None

        if data is not None:
            first_type = data.get("post_type")
            second_type = data.get(f"{first_type}_type")
            third_type = data.get("sub_type")

        if clas is not None:
            first_type = clas.FIRST_TYPE
            second_type = clas.SECOND_TYPE
            third_type = clas.THIRD_TYPE

        if first_type:
            key = key + first_type
        if second_type:
            key = key + f"-{second_type}"
        if third_type:
            key = key + f"-{third_type}"
        return key


def main():
    understander = SoundUnderstander()
    print(understander._understand_map)


if __name__ == "__main__":
    main()
