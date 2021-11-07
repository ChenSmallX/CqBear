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
- [x] 添加事件
- [x] 添加获取参数的property
- [x] 添加注释
"""

import sys
from typing import List, Optional

from cqbear.util import allSubclasses


class Sound(dict):
    """消息事件基类"""
    FIRST_TYPE = None
    SECOND_TYPE = None
    THIRD_TYPE = None

    def __init__(self, data: dict):
        super(Sound, self).__init__(data)

    @property
    def type_short(self):
        t = "sound"
        for tp in [self.FIRST_TYPE, self.SECOND_TYPE, self.THIRD_TYPE]:
            t = t + f".{str(tp)}" if tp is not None else ""
        return t

    @property
    def time(self) -> int:
        return self.get(sys._getframe().f_code.co_name)


class Message(Sound):
    FIRST_TYPE = "message"

    def __init__(self, data: dict):
        super(Message, self).__init__(data)

    @property
    def message_id(self) -> int:
        """消息 ID"""
        return self.get(sys._getframe().f_code.co_name)


class PrivateMessageSender(dict):
    """发送人信息"""
    def __init__(self, data: dict):
        super(PrivateMessageSender, self).__init__(data)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def nickname(self) -> str:
        """昵称"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sex(self) -> str:
        """
        性别, `male` 或 `female` 或 `unknown`
        """
        return self.get(sys._getframe().f_code.co_name)

    @property
    def age(self) -> int:
        """年龄"""
        return self.get(sys._getframe().f_code.co_name)


class PrivateMessage(Message):
    """私聊消息

    可使用更详细的
        FriendPrivateMessage,
        GroupPrivateMessage,
        GroupSelfPrivateMessage,
        OtherPrivateMessage
    """
    SECOND_TYPE = "private"

    def __init__(self, data: dict):
        super(PrivateMessage, self).__init__(data)
        self._sender = None

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
        """临时会话来源

        可从 `PrivateMessage.TEMP_SOURCE_TYPE` 中获取枚举"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def message(self) -> str:
        """消息内容"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def raw_message(self) -> str:
        """原始消息内容"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def font(self) -> int:
        """字体"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sender(self) -> PrivateMessageSender:
        """发送人信息

        `sender` 中的各字段是尽最大努力提供的,
        不保证每个字段都一定存在,
        也不保证存在的字段都是完全正确的 ( 缓存可能过期 )"""
        if self._sender is None:
            self._sender = PrivateMessageSender(
                self.get(sys._getframe().f_code.co_name, {}))
        return self._sender


class FriendPrivateMessage(PrivateMessage):
    """私聊消息：好友私聊消息"""
    THIRD_TYPE = "friend"

    def __init__(self, data: dict):
        super(FriendPrivateMessage, self).__init__(data)


class GroupPrivateMessage(PrivateMessage):
    """私聊消息：群临时会话 私聊消息"""
    THIRD_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupPrivateMessage, self).__init__(data)


class GroupSelfPrivateMessage(PrivateMessage):
    """私聊消息：群中自身发送私聊消息"""
    THIRD_TYPE = "group_self"

    def __init__(self, data: dict):
        super(GroupSelfPrivateMessage, self).__init__(data)


class OtherPrivateMessage(PrivateMessage):
    """私聊消息：好友私聊消息、群临时会话、群中自身发送之外的其他私聊消息"""
    THIRD_TYPE = "other"

    def __init__(self, data: dict):
        super(OtherPrivateMessage, self).__init__(data)


class GroupMessageAnonymous(dict):
    """GroupMessage 中的 anonymous

    注：还未实现针对匿名者的禁言 Roar"""
    def __init__(self, data: dict):
        super(GroupMessageAnonymous, self).__init__(data)

    @property
    def id(self) -> int:
        """匿名用户 ID"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def name(self) -> str:
        """匿名用户名称"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def flag(self) -> str:
        """匿名用户 flag, 在调用禁言 API 时需要传入"""
        return self.get(sys._getframe().f_code.co_name)


class GroupMessageSender(dict):
    """GroupMessage 中的 sender"""
    def __init__(self, data: dict):
        super(GroupMessageSender, self).__init__(data)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def nickname(self) -> str:
        """昵称"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def card(self) -> str:
        """群名片/备注"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sex(self) -> str:
        """
        性别, `male` 或 `female` 或 `unknown`
        """
        return self.get(sys._getframe().f_code.co_name)

    @property
    def age(self) -> int:
        """年龄"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def area(self) -> str:
        """地区"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def level(self) -> str:
        """成员等级"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def role(self) -> str:
        """角色, `owner` 或 `admin` 或 `member`"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def title(self) -> str:
        """专属头衔"""
        return self.get(sys._getframe().f_code.co_name)


class GroupMessage(Message):
    """群消息

    可以使用更为详细的
        NormalGroupMessage，
        AnonymousGroupMessage，
        NoticeGroupMessage
    """
    SECOND_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupMessage, self).__init__(data)
        self._sender = None
        self._is_anony = None
        self._anony = None

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def anonymous(self) -> Optional[GroupMessageAnonymous]:
        """匿名信息, 如果不是匿名消息则为 None"""
        if self._is_anony is None:
            anony = self.get(sys._getframe().f_code.co_name, {})
            if anony is not None:
                self._anony = GroupMessageAnonymous(anony)
                self._is_anony = True
            else:
                self._is_anony = False
        return self._anony

    @property
    def message(self) -> str:
        """消息内容"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def raw_message(self) -> str:
        """原始消息内容"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def font(self) -> int:
        """字体"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def sender(self) -> GroupMessageSender:
        """发送人信息

        `sender` 中的各字段是尽最大努力提供的,
        不保证每个字段都一定存在,
        也不保证存在的字段都是完全正确的 ( 缓存可能过期 ) 。
        尤其对于匿名消息, 此字段不具有参考价值。"""
        if self._sender is None:
            self._sender = GroupMessageSender(
                self.get(sys._getframe().f_code.co_name, {}))
        return self._sender


class NormalGroupMessage(GroupMessage):
    """群消息：正常群消息(非匿名群成员发布的)"""
    THIRD_TYPE = "normal"

    def __init__(self, data: dict):
        super(NormalGroupMessage, self).__init__(data)


class AnonymousGroupMessage(GroupMessage):
    """群消息：匿名群成员发布的群消息"""
    THIRD_TYPE = "anonymous"

    def __init__(self, data: dict):
        super(AnonymousGroupMessage, self).__init__(data)


class NoticeGroupMessage(GroupMessage):
    """群消息：系统提示群消息"""
    THIRD_TYPE = "notice"

    def __init__(self, data: dict):
        super(NoticeGroupMessage, self).__init__(data)


class Notice(Sound):
    FIRST_TYPE = "notice"

    def __init__(self, data: dict):
        super(Notice, self).__init__(data)


class GroupUploadNoticeFile(dict):
    """GroupUploadNotice 中的 file"""
    def __init__(self, data: dict):
        super(GroupUploadNoticeFile, self).__init__(data)

    @property
    def id(self) -> str:
        """文件 ID"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def name(self) -> str:
        """文件名"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def size(self) -> int:
        """文件大小 ( 字节数 )"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def busid(self) -> int:
        """busid
        cqbear.roar.GetGroupFileUrl 等关于群文件的 roar 会需要填入"""
        return self.get(sys._getframe().f_code.co_name)


class GroupUploadNotice(Notice):
    """群文件上传"""
    SECOND_TYPE = "group_upload"

    def __init__(self, data: dict):
        super(GroupUploadNotice, self).__init__(data)
        self._file = None

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def file(self) -> GroupUploadNoticeFile:
        """文件信息"""
        if self._file is None:
            self._file = GroupUploadNoticeFile(
                self.get(sys._getframe().f_code.co_name))
        return self._file


class GroupAdminNotice(Notice):
    """群管理员变动

    可使用更加精确的
        SetGroupAdminNotice,
        UnsetGroupAdminNotice
    """
    SECOND_TYPE = "group_admin"

    def __init__(self, data: dict):
        super(GroupAdminNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """管理员 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)


class SetGroupAdminNotice(GroupAdminNotice):
    """群管理员变动：用户被设置为群管理员"""
    THIRD_TYPE = "set"

    def __init__(self, data: dict):
        super(SetGroupAdminNotice, self).__init__(data)


class UnsetGroupAdminNotice(GroupAdminNotice):
    """群管理员变动：用户被取消群管理员"""
    THIRD_TYPE = "unset"

    def __init__(self, data: dict):
        super(UnsetGroupAdminNotice, self).__init__(data)


class GroupDecreaseNotice(Notice):
    """群成员减少

    可以使用更精确的
        LeaveGroupDecreaseNotice,
        KickGroupDecreaseNotice,
        KickMeGroupDecreaseNotice
    """
    SECOND_TYPE = "group_decrease"

    def __init__(self, data: dict):
        super(GroupDecreaseNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def operator_id(self) -> int:
        """操作者 QQ 号 ( 如果是主动退群, 则和 `user_id` 相同 )"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """离开者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)


class LeaveGroupDecreaseNotice(GroupDecreaseNotice):
    """退群：用户主动退群"""
    THIRD_TYPE = "leave"

    def __init__(self, data: dict):
        super(LeaveGroupDecreaseNotice, self).__init__(data)


class KickGroupDecreaseNotice(GroupDecreaseNotice):
    """退群：成员被踢出群"""
    THIRD_TYPE = "kick"

    def __init__(self, data: dict):
        super(KickGroupDecreaseNotice, self).__init__(data)


class KickMeGroupDecreaseNotice(GroupDecreaseNotice):
    """退群：登录号被踢出群"""
    THIRD_TYPE = "kick_me"

    def __init__(self, data: dict):
        super(KickMeGroupDecreaseNotice, self).__init__(data)


class GroupIncreaseNotice(Notice):
    """群成员增加

    可使用更精确的
        ApproveGroupIncreaseNotice，
        InviteGroupIncreaseNotice
    """
    SECOND_TYPE = "group_increase"

    def __init__(self, data: dict):
        super(GroupIncreaseNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def operator_id(self) -> int:
        """操作者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """加入者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)


class ApproveGroupIncreaseNotice(GroupIncreaseNotice):
    """加群：管理员同意后加入"""
    THIRD_TYPE = "approve"

    def __init__(self, data: dict):
        super(ApproveGroupIncreaseNotice, self).__init__(data)


class InviteGroupIncreaseNotice(GroupIncreaseNotice):
    """加群：被管理员邀请入群"""
    THIRD_TYPE = "invite"

    def __init__(self, data: dict):
        super(InviteGroupIncreaseNotice, self).__init__(data)


class GroupBanNotice(Notice):
    """群禁言事件

    可使用更精确的
        EnableGroupBanNotice，
        DisableGroupBanNotice
    """
    SECOND_TYPE = "group_ban"

    def __init__(self, data: dict):
        super(GroupBanNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def operator_id(self) -> int:
        """操作者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """被禁言 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def duration(self) -> int:
        """禁言时长, 单位秒"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def is_ban(self) -> bool:
        """True: 禁言 / False: 解除禁言"""
        if self.get('sub_type') == 'ban':
            return True
        return False


class EnableGroupBanNotice(GroupBanNotice):
    """群禁言: 设置禁言"""
    THIRD_TYPE = "ban"

    def __init__(self, data: dict):
        super(EnableGroupBanNotice, self).__init__(data)


class DisableGroupBanNotice(GroupBanNotice):
    """群禁言: 解除禁言"""
    THIRD_TYPE = "lift_ban"

    def __init__(self, data: dict):
        super(DisableGroupBanNotice, self).__init__(data)


class FriendAddNotice(Notice):
    """好友添加"""
    SECOND_TYPE = "friend_add"

    def __init__(self, data: dict):
        super(FriendAddNotice, self).__init__(data)

    @property
    def user_id(self) -> int:
        """新添加好友 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)


class GroupRecallNotice(Notice):
    """群消息撤回"""
    SECOND_TYPE = "group_recall"

    def __init__(self, data: dict):
        super(GroupRecallNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """消息发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def operator_id(self) -> int:
        """操作者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def message_id(self) -> int:
        """被撤回的消息 ID"""
        return self.get(sys._getframe().f_code.co_name)


class FriendRecallNotice(Notice):
    """好友消息撤回"""
    SECOND_TYPE = "friend_recall"

    def __init__(self, data: dict):
        super(FriendRecallNotice, self).__init__(data)

    @property
    def user_id(self) -> int:
        """user_id"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def message_id(self) -> int:
        """message_id"""
        return self.get(sys._getframe().f_code.co_name)


class Notify(Notice):
    SECOND_TYPE = "notify"

    def __init__(self, data: dict):
        super(Notify, self).__init__(data)


class PokeNotify(Notify):
    """戳一戳

    分为 好友戳一戳 以及 群内戳一戳"""
    THIRD_TYPE = "poke"

    def __init__(self, data: dict):
        super(PokeNotify, self).__init__(data)

    @property
    def sender_id(self) -> int:
        """发送者 QQ 号 群内戳一戳事件不存在此属性"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """发送者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def target_id(self) -> int:
        """被戳者 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def group_id(self) -> int:
        """群号 好友戳一戳事件不存在此属性"""
        return self.get(sys._getframe().f_code.co_name)


class GroupLuckyKingNotify(Notify):
    """群红包运气王"""
    THIRD_TYPE = "lucky_king"

    def __init__(self, data: dict):
        super(GroupLuckyKingNotify, self).__init__(data)

    @property
    def user_id(self) -> int:
        """红包发送者id"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def target_id(self) -> int:
        """运气王id"""
        return self.get(sys._getframe().f_code.co_name)


class GroupMemberHonorChangeNotify(Notify):
    """群成员荣誉变更提示"""
    THIRD_TYPE = "honor"

    def __init__(self, data: dict):
        super(GroupMemberHonorChangeNotify, self).__init__(data)

    @property
    def user_id(self) -> int:
        """成员id"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def honor_type(self) -> str:
        """荣誉类型

        `talkative`龙王
        `performer`群聊之火
        `emotion`快乐源泉"""
        return self.get(sys._getframe().f_code.co_name)


class GroupCardNotice(Notice):
    """群成员名片更新

    此事件不保证时效性, 仅在收到消息时校验卡片

    当名片为空时 `card_xx` 字段为空字符串, 并不是昵称"""
    SECOND_TYPE = "group_card"

    def __init__(self, data: dict):
        super(GroupCardNotice, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """成员id"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def card_new(self) -> str:
        """新名片"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def card_old(self) -> str:
        """旧名片"""
        return self.get(sys._getframe().f_code.co_name)


class OfflineFileNoticeFile(dict):
    """OfflineFileNotice 中的 file"""
    def __init__(self, data: dict):
        super(OfflineFileNoticeFile, self).__init__(data)

    @property
    def name(self) -> str:
        """文件名"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def size(self) -> int:
        """文件大小"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def url(self) -> str:
        """下载链接"""
        return self.get(sys._getframe().f_code.co_name)


class OfflineFileNotice(Notice):
    """接收到离线文件"""
    SECOND_TYPE = "offline_file"

    def __init__(self, data: dict):
        super(OfflineFileNotice, self).__init__(data)
        self._file = None

    @property
    def user_id(self) -> int:
        """发送者id"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def file(self) -> OfflineFileNoticeFile:
        """文件数据"""
        if self._file is None:
            self._file = OfflineFileNoticeFile(
                self.get(sys._getframe().f_code.co_name))
        return self._file


class ClientStatusNoticeDevice(dict):
    """ClientStatusNotice 中的 device"""
    def __init__(self, data: dict):
        super(ClientStatusNoticeDevice, self).__init__(data)

    @property
    def app_id(self) -> int:
        """客户端ID"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def device_name(self) -> str:
        """设备名称"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def device_kind(self) -> str:
        """设备类型"""
        return self.get(sys._getframe().f_code.co_name)


class ClientStatusNotice(Notice):
    SECOND_TYPE = "client_status"

    def __init__(self, data: dict):
        super(ClientStatusNotice, self).__init__(data)
        self._clients = None

    @property
    def online(self) -> bool:
        """online"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def client(self) -> List[ClientStatusNoticeDevice]:
        """客户端信息"""
        if self._clients is None:
            clients = list()
            for dev in self.get(sys._getframe().f_code.co_name):
                clients.append(ClientStatusNoticeDevice(dev))
            self._clients = clients
        return self._clients


class EssenceNotice(Notice):
    """精华消息

    可使用更精确的
        AddEssenceNotice,
        DeleteEssenceNotice
    """
    SECOND_TYPE = "essence"

    def __init__(self, data: dict):
        super(EssenceNotice, self).__init__(data)

    @property
    def sender_id(self) -> int:
        """消息发送者ID"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def operator_id(self) -> int:
        """操作者ID"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def message_id(self) -> int:
        """消息ID"""
        return self.get(sys._getframe().f_code.co_name)


class AddEssenceNotice(EssenceNotice):
    """添加精华消息"""
    THIRD_TYPE = "add"

    def __init__(self, data: dict):
        super(AddEssenceNotice, self).__init__(data)


class DeleteEssenceNotice(EssenceNotice):
    """删除精华消息"""
    THIRD_TYPE = "delete"

    def __init__(self, data: dict):
        super(DeleteEssenceNotice, self).__init__(data)


class Request(Sound):
    FIRST_TYPE = "request"

    def __init__(self, data: dict):
        super(Request, self).__init__(data)


class FriendRequest(Request):
    """加好友请求

    使用 `cqbear.roar.SetFriendAddRequest` 处理此事件
    (需要传入 `FriendRequest.flag` 参数)"""
    SECOND_TYPE = "friend"

    def __init__(self, data: dict):
        super(FriendRequest, self).__init__(data)

    @property
    def user_id(self) -> int:
        """发送请求的 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def comment(self) -> int:
        """验证信息"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def flag(self) -> str:
        """请求 flag, 在调用处理请求的 API 时需要传入"""
        return self.get(sys._getframe().f_code.co_name)


class GroupRequest(Request):
    """加群请求/邀请

    使用 `cqbear.roar.SetGroupAddRequest` 处理此事件
    (需要传入 `GroupRequest.flag` 参数)"""
    SECOND_TYPE = "group"

    def __init__(self, data: dict):
        super(GroupRequest, self).__init__(data)

    @property
    def group_id(self) -> int:
        """群号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def user_id(self) -> int:
        """发起请求的 QQ 号"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def comment(self) -> str:
        """验证信息"""
        return self.get(sys._getframe().f_code.co_name)

    @property
    def flag(self) -> str:
        """请求 flag, 在调用处理请求的 API 时需要传入"""
        return self.get(sys._getframe().f_code.co_name)


class AddGroupRequest(Request):
    """加群请求"""
    THIRD_TYPE = "add"

    def __init__(self, data: dict):
        super(AddGroupRequest, self).__init__(data)


class InviteGroupRequest(Request):
    """邀请加群请求"""
    THIRD_TYPE = "invite"

    def __init__(self, data: dict):
        super(InviteGroupRequest, self).__init__(data)


class SoundUnderstander:
    _understand_map = {
        "default": Sound
    }

    def __init__(self):
        cls_lst = allSubclasses(Sound)
        for cls in cls_lst:
            if cls == Sound:
                continue
            key = self._get_key(clas=cls)
            self._understand_map[key] = cls

    def understand(self, data: dict) -> Sound:
        key = self._get_key(data=data)
        cls = self._understand_map.get(key, Sound)
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


def doc():
    for c in allSubclasses(Sound):
        print(f"class: {c}")
        print(f"doc: {c.__doc__}\n")


if __name__ == "__main__":
    doc()
