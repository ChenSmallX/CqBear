# -*- coding=utf-8 -*-
"""
"""


from cqbear.sentence import ForwardSend


class Roar(dict):
    """发送消息基类
    """
    _extend_url = None

    @property
    def extend_url(self) -> str:
        if not self._extend_url:
            raise NotImplementedError
        return self._extend_url

    @property
    def speak_data(self) -> dict:
        return dict(self)


class SendPrivateMessage(Roar):
    """发送私聊消息"""
    _extend_url = "send_private_msg"

    def __init__(self):
        self['auto_escape'] = False

    def set_auto_escape(self, auto_escape: bool):
        self['auto_escape'] = auto_escape
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = int(user_id)
        return self

    def set_group_id(self, group_id: int):
        self['group_id'] = int(group_id)
        return self

    def set_message(self, message: str):
        self['message'] = str(message)
        return self


class SendGroupMessage(Roar):
    _extend_url = "send_group_msg"

    def __init__(self):
        self['auto_escape'] = False

    def set_auto_escape(self, auto_escape: bool):
        self['auto_escape'] = auto_escape
        return self

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_message(self, message: str):
        self['message'] = str(message)
        return self


class SendGroupForwardMassage(Roar):
    """
    messages存放的message为cqbear.sentence.ForwardSend

    `sgfm = SendGroupForwardMessage().add_message(ForwardSend())`
    `bear.mouth.speak(sgfm)`
    """
    _extend_url = "send_group_forward_msg"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_messages(self, messages: list):
        self['messages'] = messages
        return self

    def add_message(self, message: ForwardSend):
        if self.get("messages"):
            self['messages'].append(message)
        else:
            self['messages'] = [message]
        return self


class DeleteMessage(Roar):
    _extend_url = "delete_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


class GroupKick(Roar):
    _extend_url = "set_group_kick"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_reject_add_request(self, reject: bool):
        self['reject_add_request'] = reject
        return self


class GroupBan(Roar):
    _extend_url = "set_group_ban"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_duration_second(self, second: int):
        self['duration'] = second
        return self


class GroupWholeBan(Roar):
    _extend_url = "set_group_whole_ban"

    def set_group_id(self, group_id):
        self['group_id'] = group_id
        return self

    def set_ban_status(self, ban_enable: bool):
        self['enable'] = ban_enable
        return self


class SetGroupAdmin(Roar):
    _extend_url = "set_group_admin"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_enable(self, enable: bool):
        """true 为设置, false 为取消"""
        self['enable'] = enable
        raise self


class SetGroupMemberCardName(Roar):
    _extend_url = "set_group_card"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_card_name(self, name: str):
        self['card'] = name
        return self


class SetGroupName(Roar):
    _extend_url = "set_group_name"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_group_name(self, group_name: str):
        self['group_name'] = group_name
        return self


class LeaveGroup(Roar):
    _extend_url = "set_group_leave"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_dismiss(self, dismiss: bool):
        """是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散"""
        self['dismiss'] = dismiss
        return self


class SetGroupSpecialTitle(Roar):
    _extend_url = "set_group_special_title"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_special_title(self, special_title: str):
        """专属头衔, 不填或空字符串表示删除专属头衔"""
        self['special_title'] = special_title
        return self

    def set_duration(self, duration_second: int):
        """专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果,
        可能是只有某些特殊的时间长度有效, 有待测试"""
        self['duration'] = duration_second
        return self


class SetFriendAddRequest(Roar):
    _extend_url = "set_friend_add_request"

    def set_flag(self, flag: str):
        """加好友请求的 flag（需从上报的cqbear.sound.FriendRequest中获得）"""
        self['flag'] = flag
        return self

    def set_approve(self, approve: bool):
        """是否同意请求"""
        self['approve'] = approve
        return self

    def set_remark(self, remark: str):
        """添加后的好友备注（仅在同意时有效）"""
        self['remark'] = remark
        return self


class SetGroupAddRequest(Roar):
    _extend_url = "set_group_add_request"

    def set_flag(self, flag: str):
        """加群请求的 flag（需从上报的cqbear.sound.GroupRequest中获得）"""
        self['flag'] = flag
        return self

    def set_sub_type(self, sub_type: str):
        """add` 或 `invite`, 请求类型
        （需要和上报cqbear.sound.GroupRequest中的 `sub_type` 字段相符）"""
        self['sub_type'] = sub_type
        return self

    def set_approve(self, approve: bool):
        """是否同意请求／邀请"""
        self['approve'] = approve
        return self

    def set_reason(self, reason: str):
        """拒绝理由（仅在拒绝时有效）"""
        self['reason'] = reason
        return self


class getLoginInfo(Roar):
    _extend_url = "get_login_info"


class getStrangerInfo(Roar):
    _extend_url = "get_stranger_info"

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_no_cache(self, no_cache: bool):
        """是否不使用缓存（使用缓存可能更新不及时, 但响应更快）"""
        self['no_cache'] = no_cache
        return self


class GetFriendList(Roar):
    _extend_url = "get_friend_list"


class DeleteFriend(Roar):
    _extend_url = "delete_friend"

    def set_user_id(self, user_id: int):
        """好友 QQ 号"""
        self['friend_id'] = user_id
        return self


class GetGroupInfo(Roar):
    _extend_url = "get_group_info"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_no_cache(self, no_cache: bool):
        """否不使用缓存（使用缓存可能更新不及时, 但响应更快）"""
        self['no_cache'] = no_cache
        return self


class GetGroupList(Roar):
    _extend_url = "get_group_list"


class GetGroupMemberInfo(Roar):
    _extend_url = "get_group_member_info"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_no_cache(self, no_cache: bool):
        """是否不使用缓存（使用缓存可能更新不及时, 但响应更快）"""
        self['no_cache'] = no_cache
        return self


class GetGroupMemberList(Roar):
    _extend_url = "get_group_member_list"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class GetGroupHonorInfo(Roar):
    _extend_url = "get_group_honor_info"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_type(self, honor_type: str):
        """要获取的群荣誉类型, 可传入
        `talkative` `performer` `legend`
        `strong_newbie` `emotion` 以分别获取单个类型的群荣誉数据,
        或传入 `all` 获取所有数据"""
        assert honor_type in [
            "talkative", "performer", "legend",
            "strong_newbie", "emotion"]
        self['type'] = honor_type
        return self


class CheckCanSendImage(Roar):
    _extend_url = "can_send_image"


class CheckCanSendVoiceRecord(Roar):
    _extend_url = "can_send_record"


class GetVersionInfo(Roar):
    _extend_url = "get_version_info"


class RestartCqhttpServer(Roar):
    _extend_url = "set_restart"

    def set_delay_ms(self, delay_ms: int):
        """要延迟的毫秒数, 如果默认情况下无法重启, 可以尝试设置延迟为 2000 左右"""
        self['delay'] = delay_ms
        return self


class SetGroupPortrait(Roar):
    """设置群头像"""
    _extend_url = "set_group_portrait"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_image_file(self, image_file: str):
        """
        - 绝对路径, 例如 `file:///C:\\\\Users\\Richard\\Pictures\\1.png`,
            格式使用 [`file` URI](https://tools.ietf.org/html/rfc8089)
        - 网络 URL, 例如 `http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg`
        - Base64 编码, 例如 `base64://iVBORw0KGgoAErkJggg==`
        """
        self['file'] = image_file
        raise self

    def set_use_cache(self, use_cache: int):
        """表示是否使用已缓存的文件

        `cache`: 通过网络 URL 发送时有效, `1`表示使用缓存, `0`关闭关闭缓存, 默认 为`1`"""
        self['cache'] = 1 if use_cache else 0
        return self

# TODO: 从 获取群系统消息 继续开始添加 Roar
