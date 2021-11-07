# -*- coding=utf-8 -*-
"""
TODO:
- [x] 添加API
- [x] 添加注释
- [ ] __init__ 时初始化默认参数
"""


from typing import List, Union
from cqbear.sentence import ForwardSend, Sentence
from cqbear.util import allSubclasses


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
    """发送私聊消息
    ---
    若通过群临时消息发起会话，需要设置`group_id`参数，
    此时机器人本身必须是管理员/群主
    ---
    参数：

    | 字段名         | 数据类型  | 默认值   | 说明                                                                   |
    | ------------- | ------- | ------- | ---------------------------------------------------------------------- |
    | `user_id`     | int64   | -       | 对方 QQ 号                                                              |
    | `group_id`    | int64   | -       | 主动发起临时会话群号(机器人本身必须是管理员/群主)                               |
    | `message`     | message | -       | 要发送的内容                                                             |
    | `auto_escape` | boolean | `false` | 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 `message` 字段是字符串时有效 |
    ---
    响应数据：

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `message_id` | int32 | 消息 ID |
    """
    _extend_url = "send_private_msg"

    def __init__(self):
        self['auto_escape'] = False

    def set_auto_escape(self, auto_escape: bool):
        """消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) ,
        只在 `message` 字段是字符串时有效"""
        self['auto_escape'] = auto_escape
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = int(user_id)
        return self

    def set_group_id(self, group_id: int):
        """主动发起临时会话群号(机器人本身必须是管理员/群主)"""
        self['group_id'] = int(group_id)
        return self

    def set_message(self, message: Union[str, Sentence, list]):
        if isinstance(message, list):
            list_msg = ""
            for msg in message:
                list_msg += str(msg)
            message = list_msg
        self['message'] = str(message)
        return self


class SendGroupMessage(Roar):
    """发送群消息
    ---
    参数：

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `message` | message | - | 要发送的内容 |
    | `auto_escape` | boolean | `false` | 消息内容是否作为纯文本发送 ( 即不解析 CQ 码) , 只在 `message` 字段是字符串时有效 |
    ---
    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `message_id` | int32 | 消息 ID |
    """
    _extend_url = "send_group_msg"

    def __init__(self):
        self['auto_escape'] = False

    def set_auto_escape(self, auto_escape: bool):
        """消息内容是否作为纯文本发送 ( 即不解析 CQ 码) ,
        只在 `message` 字段是字符串时有效"""
        self['auto_escape'] = auto_escape
        return self

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_message(self, message: Union[str, Sentence, list]):
        if isinstance(message, list):
            list_msg = ""
            for msg in message:
                list_msg += str(msg)
            message = list_msg
        self['message'] = str(message)
        return self


class SendGroupForwardMassage(Roar):
    """发送合并转发 ( 群 )
    ---
    messages 存放的 forward node 为 cqbear.sentence.ForwardSend

    `sgfm = SendGroupForwardMessage().add_message(ForwardSend())`
    `bear.speak(sgfm)`
    ---
    参数：

    | 字段       | 类型           | 说明    |
    | ---------- | -------------- | ----- |
    | `group_id` | int64          | 群号   |
    | `messages` | forward node[] | 自定义转发消息 |
    """
    _extend_url = "send_group_forward_msg"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_messages(self, messages: List[ForwardSend]):
        self['messages'] = [
            msg.to_str() if isinstance(msg, ForwardSend) else msg
            for msg in messages]
        return self

    def add_message(self, message: ForwardSend):
        if self.get("messages"):
            self['messages'].append(message.to_str())
        else:
            self['messages'] = [message.to_str()]
        return self


class DeleteMessage(Roar):
    """撤回消息
    ---
    通过消息id撤回消息

    支持撤回自己的消息，群管理员/群主撤回成员消息

    当机器人是管理员时，撤回操作对其他管理员和群主无效
    """
    _extend_url = "delete_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


RecallMessage = DeleteMessage


class GetMessage(Roar):
    """获取消息
    ---
    通过消息id获取消息

    ---
    参数

    | 字段         | 类型  | 说明   |
    | ------------ | ----- | ------ |
    | `message_id` | int32 | 消息id |

    ---

    响应数据

    | 字段          | 类型     | 说明       |
    | ------------ | -------- | ---------- |
    | `message_id` | int32    | 消息id      |
    | `real_id`    | int32    | 消息真实id   |
    | `sender`     | object   | 发送者      |
    | `time`       | int32    | 发送时间    |
    | `message`    | message  | 消息内容    |
    | `raw_message`| message  | 原始消息内容 |
    """
    _extend_url = "get_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


class GetForwardMessage(Roar):
    """获取合并转发内容
    ---

    参数

    | 字段         | 类型   | 说明   |
    | ------------ | ------ | ------ |
    | `message_id` | string | 消息id |

    响应数据

    | 字段       | 类型              | 说明     |
    | ---------- | ----------------- | -------- |
    | `messages` | forward message[] | 消息列表 |
    """
    _extend_url = "get_forward_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


class GetImageInfo(Roar):
    """获取图片信息
    ---

    参数

    | 字段   | 类型   | 说明           |
    | ------ | ------ | -------------- |
    | `file` | string | 图片缓存文件名 |

    响应数据

    | 字段       | 类型   | 说明           |
    | ---------- | ------ | -------------- |
    | `size`     | int32  | 图片源文件大小 |
    | `filename` | string | 图片文件原名   |
    | `url`      | string | 图片下载地址   |
    """
    _extend_url = "get_image"

    def set_file(self, file: str):
        """图片缓存文件名"""
        self['file'] = file
        return self


class GroupKick(Roar):
    """群组踢人
    ---

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id` | int64 | - | 要踢的 QQ 号  |
    | `reject_add_request` | boolean | `false` | 拒绝此人的加群请求 |
    """
    _extend_url = "set_group_kick"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_reject_add_request(self, reject: bool):
        """是否拒绝此人的加群请求"""
        self['reject_add_request'] = reject
        return self


class GroupSingleMute(Roar):
    """群组单人禁言
    ---
    设置 duration 参数为 0 则取消禁言

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id` | int64 | - | 要禁言的 QQ 号 |
    | `duration` | number | `30 * 60` | 禁言时长, 单位秒, 0 表示取消禁言 |
    """
    _extend_url = "set_group_ban"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_duration(self, second: int):
        """禁言时长, 单位秒, 0 表示取消禁言"""
        self['duration'] = second
        return self


# TODO: 群组匿名用户禁言 _extend_url = "set_group_anonymous_ban"

class GroupWholeMute(Roar):
    """群组全员禁言
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `enable` | boolean | `true` | 是否禁言 |
    """
    _extend_url = "set_group_whole_ban"

    def set_group_id(self, group_id):
        self['group_id'] = group_id
        return self

    def set_enable(self, enable: bool):
        """是否禁言"""
        self['enable'] = enable
        return self


class SetGroupAdmin(Roar):
    """群组设置管理员
    ---
    当机器人为群主时有效

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id` | int64 | - | 要设置管理员的 QQ 号 |
    | `enable` | boolean | `true` | true 为设置, false 为取消 |
    """
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
    """设置群名片 ( 群备注 )
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id` | int64 | - | 要设置的 QQ 号 |
    | `card` | string | 空 | 群名片内容, 不填或空字符串表示删除群名片 |
    """
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
    """设置群名
    ---
    参数

    | 字段名   | 数据类型 | 说明 |
    | -------- | ------ | ---- |
    | `group_id` | int64 | 群号 |
    | `group_name` | string | 新群名 |
    """
    _extend_url = "set_group_name"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_group_name(self, group_name: str):
        self['group_name'] = group_name
        return self


class LeaveGroup(Roar):
    """退出群组
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `is_dismiss` | boolean | `false` | 是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散 |
    """
    _extend_url = "set_group_leave"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_dismiss(self, dismiss: bool):
        """是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散"""
        self['dismiss'] = dismiss
        return self


class SetGroupSpecialTitle(Roar):
    """设置群组专属头衔
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id` | int64 | - | 要设置的 QQ 号 |
    | `special_title` | string | 空 | 专属头衔, 不填或空字符串表示删除专属头衔 |
    | `duration` | number | `-1` | 专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果, 可能是只有某些特殊的时间长度有效, 有待测试 |
    """
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
    """处理加好友请求
    ---
    用于处理 cqbear.sound.FriendRequest 事件

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `flag` | string | - | 加好友请求的 flag（需从上报的数据中获得） |
    | `approve` | boolean | `true` | 是否同意请求 |
    | `remark` | string | 空 | 添加后的好友备注（仅在同意时有效） |
    """
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
    """处理加群请求／邀请
    ---
    用于处理 cqbear.sound.GroupRequest 事件

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `flag` | string | - | 加群请求的 flag（需从上报的数据中获得） |
    | `sub_type` 或 `type` | string | - | `add` 或 `invite`, 请求类型（需要和上报消息中的 `sub_type` 字段相符） |
    | `approve` | boolean | `true` | 是否同意请求／邀请 |
    | `reason` | string | 空 | 拒绝理由（仅在拒绝时有效） |
    """
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
    """获取登录号信息
    ---
    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | QQ 昵称 |
    """
    _extend_url = "get_login_info"


# TODO: 获取企点账号信息 _extend_url = "qidian_get_account_info"
class getStrangerInfo(Roar):
    """获取陌生人信息
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `user_id` | int64 | - | QQ 号 |
    | `no_cache` | boolean | `false` | 是否不使用缓存（使用缓存可能更新不及时, 但响应更快） |

    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `sex` | string | 性别, `male` 或 `female` 或 `unknown` |
    | `age` | int32 | 年龄 |
    | `qid` | string | qid ID身份卡 |
    """
    _extend_url = "get_stranger_info"

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self

    def set_no_cache(self, no_cache: bool):
        """是否不使用缓存（使用缓存可能更新不及时, 但响应更快）"""
        self['no_cache'] = no_cache
        return self


class GetFriendList(Roar):
    """获取好友列表
    ---
    响应数据

    响应内容为 json 数组, 每个元素如下：

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `remark` | string | 备注名 |
    """
    _extend_url = "get_friend_list"


class DeleteFriend(Roar):
    """删除好友
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `friend_id` | int64 | - | 好友 QQ 号 |
    """
    _extend_url = "delete_friend"

    def set_user_id(self, user_id: int):
        """好友 QQ 号"""
        self['friend_id'] = user_id
        return self


class GetGroupInfo(Roar):
    """获取群信息
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `no_cache` | boolean | `false` | 是否不使用缓存（使用缓存可能更新不及时, 但响应更快） |

    响应数据

    如果机器人尚未加入群, `group_create_time`, `group_level`, `max_member_count` 和 `member_count` 将会为0

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `group_id` | int64 | 群号 |
    | `group_name` | string | 群名称 |
    | `group_memo` | string | 群备注 |
    | `group_create_time` | uint32 | 群创建时间 |
    | `group_level` | uint32 | 群等级 |
    | `member_count` | int32 | 成员数 |
    | `max_member_count` | int32 | 最大成员数（群容量） |

    ---
    这里提供了一个API用于获取群图片, `group_id` 为群号
    https://p.qlogo.cn/gh/{group_id}/{group_id}/100
    """
    _extend_url = "get_group_info"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_no_cache(self, no_cache: bool):
        """否不使用缓存（使用缓存可能更新不及时, 但响应更快）"""
        self['no_cache'] = no_cache
        return self


class GetGroupList(Roar):
    """获取群列表
    ---
    响应数据

    响应内容为 json 数组

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `group_id` | int64 | 群号 |
    | `group_name` | string | 群名称 |
    | `group_memo` | string | 群备注 |
    | `group_create_time` | uint32 | 群创建时间 |
    | `group_level` | uint32 | 群等级 |
    | `member_count` | int32 | 成员数 |
    | `max_member_count` | int32 | 最大成员数（群容量） |
    """
    _extend_url = "get_group_list"


class GetGroupMembersInfo(Roar):
    """获取群成员信息
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `user_id`  | int64 | - | QQ 号 |
    | `no_cache` | boolean | `false` | 是否不使用缓存（使用缓存可能更新不及时, 但响应更快） |

    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `group_id` | int64 | 群号 |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `card` | string | 群名片／备注 |
    | `sex` | string | 性别, `male` 或 `female` 或 `unknown` |
    | `age` | int32 | 年龄 |
    | `area` | string | 地区 |
    | `join_time` | int32 | 加群时间戳 |
    | `last_sent_time` | int32 | 最后发言时间戳 |
    | `level` | string | 成员等级 |
    | `role` | string | 角色, `owner` 或 `admin` 或 `member` |
    | `unfriendly` | boolean | 是否不良记录成员 |
    | `title` | string | 专属头衔 |
    | `title_expire_time` | int64 | 专属头衔过期时间戳 |
    | `card_changeable` | boolean | 是否允许修改群名片 |
    """
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
    """获取群成员列表
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |

    响应数据


    响应内容为 json 数组, 对于同一个群组的同一个成员, 获取列表时和获取单独的成员信息时, 某些字段可能有所不同, 例如 `area`、`title` 等字段在获取列表时无法获得, 具体应以单独的成员信息为准。

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `group_id` | int64 | 群号 |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `card` | string | 群名片／备注 |
    | `sex` | string | 性别, `male` 或 `female` 或 `unknown` |
    | `age` | int32 | 年龄 |
    | `area` | string | 地区 |
    | `join_time` | int32 | 加群时间戳 |
    | `last_sent_time` | int32 | 最后发言时间戳 |
    | `level` | string | 成员等级 |
    | `role` | string | 角色, `owner` 或 `admin` 或 `member` |
    | `unfriendly` | boolean | 是否不良记录成员 |
    | `title` | string | 专属头衔 |
    | `title_expire_time` | int64 | 专属头衔过期时间戳 |
    | `card_changeable` | boolean | 是否允许修改群名片 |
    """
    _extend_url = "get_group_member_list"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class GetGroupHonorInfo(Roar):
    """获取群荣誉信息
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `group_id` | int64 | - | 群号 |
    | `type` | string | - | 要获取的群荣誉类型, 可传入 `talkative` `performer` `legend` `strong_newbie` `emotion` 以分别获取单个类型的群荣誉数据, 或传入 `all` 获取所有数据 |

    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `group_id` | int64 | 群号 |
    | `current_talkative` | object | 当前龙王, 仅 `type` 为 `talkative` 或 `all` 时有数据 |
    | `talkative_list` | array | 历史龙王, 仅 `type` 为 `talkative` 或 `all` 时有数据 |
    | `performer_list` | array | 群聊之火, 仅 `type` 为 `performer` 或 `all` 时有数据 |
    | `legend_list` | array | 群聊炽焰, 仅 `type` 为 `legend` 或 `all` 时有数据 |
    | `strong_newbie_list` | array | 冒尖小春笋, 仅 `type` 为 `strong_newbie` 或 `all` 时有数据 |
    | `emotion_list` | array | 快乐之源, 仅 `type` 为 `emotion` 或 `all` 时有数据 |

    其中 `current_talkative` 字段的内容如下：

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `avatar` | string | 头像 URL |
    | `day_count` | int32 | 持续天数 |

    其它各 `*_list` 的每个元素是一个 json 对象, 内容如下：

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `user_id` | int64 | QQ 号 |
    | `nickname` | string | 昵称 |
    | `avatar` | string | 头像 URL |
    | `description` | string | 荣誉描述 |
    """
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
    """检查是否可以发送图片
    ---
    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `yes` | boolean | 是或否 |
    """
    _extend_url = "can_send_image"


class CheckCanSendVoiceRecord(Roar):
    """检查是否可以发送语音
    ---
    响应数据

    | 字段名 | 数据类型 | 说明 |
    | ----- | ------- | --- |
    | `yes` | boolean | 是或否 |
    """
    _extend_url = "can_send_record"


class GetVersionInfo(Roar):
    """获取版本信息
    ---
    响应数据

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | --- | ---- |
    | `app_name` | string | `go-cqhttp` | 应用标识, 如 `go-cqhttp` 固定值 |
    | `app_version` | string |  | 应用版本, 如 `v0.9.40-fix4` |
    | `app_full_name` | string | | 应用完整名称 |
    | `protocol_version` | string | `v11` | OneBot 标准版本 固定值 |
    | `coolq_edition` | string | `pro` | 原Coolq版本 固定值 |
    | `coolq_directory` | string |  |  |
    | `go-cqhttp` | bool | true| 是否为go-cqhttp 固定值 |
    | `plugin_version` | string | `4.15.0` | 固定值 |
    | `plugin_build_number` | int | 99 | 固定值 |
    | `plugin_build_configuration` | string | `release` | 固定值 |
    | `runtime_version` | string |  |  |
    | `runtime_os` | string |  |  |
    | `version` | string || 应用版本, 如 `v0.9.40-fix4` |
    | `protocol` | int | `0/1/2/3/-1` | 当前登陆使用协议类型 |
    """
    _extend_url = "get_version_info"


class RestartCqhttpServer(Roar):
    """重启 go-cqhttp
    ---
    由于重启 go-cqhttp 实现同时需要重启 API 服务, 这意味着当前的 API 请求会被中断, 因此需要异步地重启, 接口返回的 `status` 是 `async`。

    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `delay` | number | `0` | 要延迟的毫秒数, 如果默认情况下无法重启, 可以尝试设置延迟为 2000 左右 |
    """
    _extend_url = "set_restart"

    def set_delay_ms(self, delay_ms: int):
        """要延迟的毫秒数, 如果默认情况下无法重启, 可以尝试设置延迟为 2000 左右"""
        self['delay'] = delay_ms
        return self


class SetGroupPortrait(Roar):
    """设置群头像
    ---
    参数

    | 字段       | 类型   | 说明                     |
    | ---------- | ------ | ------------------------ |
    | `group_id` | int64  | 群号                     |
    | `file`     | string | 图片文件名               |
    | `cache`    | int    | 表示是否使用已缓存的文件 |

    [1] `file` 参数支持以下几种格式：

    - 绝对路径, 例如 `file:///C:\\Users\\Richard\\Pictures\\1.png`, 格式使用 [`file` URI](https://tools.ietf.org/html/rfc8089)
    - 网络 URL, 例如 `http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg`
    - Base64 编码, 例如 `base64://iVBORw0KGgoAAAANSUhEUgAAABQAAAAVCAIAAADJt1n/AAAAKElEQVQ4EWPk5+RmIBcwkasRpG9UM4mhNxpgowFGMARGEwnBIEJVAAAdBgBNAZf+QAAAAABJRU5ErkJggg==`

    [2] `cache`参数: 通过网络 URL 发送时有效, `1`表示使用缓存, `0`关闭关闭缓存, 默认 为`1`

    [3] 目前这个API在登录一段时间后因cookie失效而失效, 请考虑后使用
    """
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


class GetChineseWordSlices(Roar):
    """获取中文分词
    ---
    参数

    | 字段      | 类型   | 说明 |
    | --------- | ------ | ---- |
    | `content` | string | 内容 |

    响应数据

    | 字段     | 类型     | 说明 |
    | -------- | -------- | ---- |
    | `slices` | string[] | 词组 |

    """
    _extend_url = ".get_word_slices"

    def set_content(self, content: str):
        """内容"""
        self['content'] = content
        return self


class OcrImage(Roar):
    """图片 OCR
    ---
    参数

    | 字段    | 类型   | 说明   |
    | ------- | ------ | ------ |
    | `image` | string | 图片ID |

    响应数据

    | 字段       | 类型            | 说明    |
    | ---------- | --------------- | ------- |
    | `texts`    | TextDetection[] | OCR结果 |
    | `language` | string          | 语言    |

    TextDetection

    | 字段          | 类型    | 说明   |
    | ------------- | ------- | ------ |
    | `text`        | string  | 文本   |
    | `confidence`  | int32   | 置信度 |
    | `coordinates` | vector2 | 坐标   |
    """
    _extend_url = "ocr_image"

    def set_image_id(self, image_id: str):
        """图片ID"""
        self['image'] = image_id
        return self


class GetGroupSystemMessage(Roar):
    """获取群系统消息
    ---
    响应数据

    | 字段               | 类型             | 说明         |
    | ------------------ | ---------------- | ------------ |
    | `invited_requests` | InvitedRequest[] | 邀请消息列表 |
    | `join_requests`    | JoinRequest[]    | 进群消息列表 |

    ::: warning 注意
    如果列表不存在任何消息, 将返回 `null`
    :::

    InvitedRequest

    | 字段           | 类型   | 说明              |
    | -------------- | ------ | ----------------- |
    | `request_id`   | int64  | 请求ID            |
    | `invitor_uin`  | int64  | 邀请者            |
    | `invitor_nick` | string | 邀请者昵称        |
    | `group_id`     | int64  | 群号              |
    | `group_name`   | string | 群名              |
    | `checked`      | bool   | 是否已被处理      |
    | `actor`        | int64  | 处理者, 未处理为0 |

    JoinRequest

    | 字段             | 类型   | 说明              |
    | ---------------- | ------ | ----------------- |
    | `request_id`     | int64  | 请求ID            |
    | `requester_uin`  | int64  | 请求者ID          |
    | `requester_nick` | string | 请求者昵称        |
    | `message`        | string | 验证消息          |
    | `group_id`       | int64  | 群号              |
    | `group_name`     | string | 群名              |
    | `checked`        | bool   | 是否已被处理      |
    | `actor`          | int64  | 处理者, 未处理为0 |
    """
    _extend_url = "get_group_system_msg"


class UploadGroupFile(Roar):
    """上传群文件
    ---
    只能上传本地文件, 需要上传 `http` 文件的话请先调用 [`download_file` API](#下载文件到缓存目录)下载

    参数

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `group_id` | int64  | 群号                      |
    | `file`     | string |  本地文件路径       |
    | `name`     | string | 储存名称         |
    | `folder`   | string | 父目录ID           |
    """
    _extend_url = "upload_group_file"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_file(self, file_path: str):
        """本地文件路径

        只能上传本地文件, 需要上传 `http` 文件的话请
        先调用 [`download_file` API](#下载文件到缓存目录)下载"""
        self['file'] = file_path
        return self

    def set_name(self, name: str):
        self['name'] = name
        return self

    def set_folder(self, folder: str):
        """在不提供 `folder` 参数的情况下默认上传到根目录"""
        self['folder'] = folder
        return self


class GetGroupFileSystemInfo(Roar):
    """获取群文件系统信息
    ---
    参数

    | 字段       | 类型  | 说明 |
    | ---------- | ----- | ---- |
    | `group_id` | int64 | 群号 |

    响应数据

    | 字段          | 类型  | 说明       |
    | ------------- | ----- | ---------- |
    | `file_count`  | int32 | 文件总数   |
    | `limit_count` | int32 | 文件上限   |
    | `used_space`  | int64 | 已使用空间 |
    | `total_space` | int64 | 空间上限   |
    """
    _extend_url = "get_group_file_system_info"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class GetGroupRootFiles(Roar):
    """获取群根目录文件列表
    ---
    参数

    | 字段       | 类型  | 说明 |
    | ---------- | ----- | ---- |
    | `group_id` | int64 | 群号 |

    响应数据

    | 字段      | 类型     | 说明       |
    | --------- | -------- | ---------- |
    | `files`   | File[]   | 文件列表   |
    | `folders` | Folder[] | 文件夹列表 |

    File

    | 字段             | 类型   | 说明                   |
    | ---------------- | ------ | ---------------------- |
    | `file_id`        | string | 文件ID                 |
    | `file_name`      | string | 文件名                 |
    | `busid`          | int32  | 文件类型               |
    | `file_size`      | int64  | 文件大小               |
    | `upload_time`    | int64  | 上传时间               |
    | `dead_time`      | int64  | 过期时间,永久文件恒为0 |
    | `modify_time`    | int64  | 最后修改时间           |
    | `download_times` | int32  | 下载次数               |
    | `uploader`       | int64  | 上传者ID               |
    | `uploader_name`  | string | 上传者名字             |

    Folder

    | 字段               | 类型   | 说明       |
    | ------------------ | ------ | ---------- |
    | `folder_id`        | string | 文件夹ID   |
    | `folder_name`      | string | 文件名     |
    | `create_time`      | int64  | 创建时间   |
    | `creator`          | int64  | 创建者     |
    | `creator_name`     | string | 创建者名字 |
    | `total_file_count` | int32  | 子文件数量 |
    """
    _extend_url = "get_group_root_files"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class GetGroupFilesByFolder(Roar):
    """获取群子目录文件列表
    ---
    参数

    | 字段        | 类型   | 说明                        |
    | ----------- | ------ | --------------------------- |
    | `group_id`  | int64  | 群号                        |
    | `folder_id` | string | 文件夹ID 参考 `Folder` 对象 |

    响应数据

    | 字段      | 类型     | 说明       |
    | --------- | -------- | ---------- |
    | `files`   | File[]   | 文件列表   |
    | `folders` | Folder[] | 文件夹列表 |

    File

    | 字段             | 类型   | 说明                   |
    | ---------------- | ------ | ---------------------- |
    | `file_id`        | string | 文件ID                 |
    | `file_name`      | string | 文件名                 |
    | `busid`          | int32  | 文件类型               |
    | `file_size`      | int64  | 文件大小               |
    | `upload_time`    | int64  | 上传时间               |
    | `dead_time`      | int64  | 过期时间,永久文件恒为0 |
    | `modify_time`    | int64  | 最后修改时间           |
    | `download_times` | int32  | 下载次数               |
    | `uploader`       | int64  | 上传者ID               |
    | `uploader_name`  | string | 上传者名字             |

    Folder

    | 字段               | 类型   | 说明       |
    | ------------------ | ------ | ---------- |
    | `folder_id`        | string | 文件夹ID   |
    | `folder_name`      | string | 文件名     |
    | `create_time`      | int64  | 创建时间   |
    | `creator`          | int64  | 创建者     |
    | `creator_name`     | string | 创建者名字 |
    | `total_file_count` | int32  | 子文件数量 |
    """
    _extend_url = "get_group_files_by_folder"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_folder_id(self, folder_id: str):
        """TODO: 添加关于 folder id 的注释"""
        self['folder_id'] = folder_id
        return self


class GetGroupFileUrl(Roar):
    """获取群文件资源链接
    ---
    参数

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `group_id` | int64  | 群号                      |
    | `file_id`  | string | 文件ID 参考 `File` 对象   |
    | `busid`    | int32  | 文件类型 参考 `File` 对象 |

    响应数据

    | 字段  | 类型   | 说明         |
    | ----- | ------ | ------------ |
    | `url` | string | 文件下载链接 |

    File

    | 字段             | 类型   | 说明                   |
    | ---------------- | ------ | ---------------------- |
    | `file_id`        | string | 文件ID                 |
    | `file_name`      | string | 文件名                 |
    | `busid`          | int32  | 文件类型               |
    | `file_size`      | int64  | 文件大小               |
    | `upload_time`    | int64  | 上传时间               |
    | `dead_time`      | int64  | 过期时间,永久文件恒为0 |
    | `modify_time`    | int64  | 最后修改时间           |
    | `download_times` | int32  | 下载次数               |
    | `uploader`       | int64  | 上传者ID               |
    | `uploader_name`  | string | 上传者名字             |

    Folder

    | 字段               | 类型   | 说明       |
    | ------------------ | ------ | ---------- |
    | `folder_id`        | string | 文件夹ID   |
    | `folder_name`      | string | 文件名     |
    | `create_time`      | int64  | 创建时间   |
    | `creator`          | int64  | 创建者     |
    | `creator_name`     | string | 创建者名字 |
    | `total_file_count` | int32  | 子文件数量 |
    """
    _extend_url = "get_group_file_url"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_file_id(self, file_id: str):
        """TODO: 添加注释"""
        self['file_id'] = file_id
        return self

    def set_busid(self, busid: int):
        """TODO: 添加注释"""
        self['busid'] = busid
        return self


class GetStatus(Roar):
    """获取状态
    ---
    响应数据

    | 字段              | 类型       | 说明                            |
    | ----------------- | ---------- | ------------------------------- |
    | `app_initialized` | bool       | 原 `CQHTTP` 字段, 恒定为 `true` |
    | `app_enabled`     | bool       | 原 `CQHTTP` 字段, 恒定为 `true` |
    | `plugins_good`    | bool       | 原 `CQHTTP` 字段, 恒定为 `true` |
    | `app_good`        | bool       | 原 `CQHTTP` 字段, 恒定为 `true` |
    | `online`          | bool       | 表示BOT是否在线                 |
    | `good`            | bool       | 同 `online`                    |
    | `stat`            | Statistics | 运行统计                        |

    Statistics

    | 字段               | 类型   | 说明             |
    | ------------------ | ------ | ---------------- |
    | `packet_received`  | uint64 | 收到的数据包总数 |
    | `packet_sent`      | uint64 | 发送的数据包总数 |
    | `packet_lost`      | uint32 | 数据包丢失总数   |
    | `message_received` | uint64 | 接受信息总数     |
    | `message_sent`     | uint64 | 发送信息总数     |
    | `disconnect_times` | uint32 | TCP 链接断开次数 |
    | `lost_times`       | uint32 | 账号掉线次数     |
    """
    _extend_url = "get_status"


class GetGroupAtallRemain(Roar):
    """获取群 @全体成员 剩余次数
    ---
    参数

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `group_id` | int64  | 群号                      |

    响应数据

    | 字段                             | 类型       | 说明                            |
    | ------------------------------- | ---------- | ------------------------------- |
    | `can_at_all`                    | bool       | 是否可以 @全体成员               |
    | `remain_at_all_count_for_group` | int16      | 群内所有管理当天剩余 @全体成员 次数 |
    | `remain_at_all_count_for_uin`   | int16      | Bot 当天剩余 @全体成员 次数      |
    """
    _extend_url = "get_group_at_all_remain"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class GetVipInfo(Roar):
    """获取VIP信息
    ---
    参数

    | 字段名 | 数据类型 | 默认值 | 说明 |
    | ----- | ------- | ----- | --- |
    | `user_id` | int64 | | QQ 号 |

    响应数据

    | 字段                | 类型    | 说明        |
    | ------------------ | ------- | ---------- |
    | `user_id`          | int64   | QQ 号       |
    | `nickname`         | string  | 用户昵称    |
    | `level`            | int64   | QQ 等级     |
    | `level_speed`      | float64 | 等级加速度  |
    | `vip_level`        | string  | 会员等级    |
    | `vip_growth_speed` | int64   | 会员成长速度 |
    | `vip_growth_total` | int64   | 会员成长总值 |
    """
    _extend_url = "_get_vip_info"

    def set_user_id(self, user_id: int):
        self['user_id'] = user_id
        return self


class SendGroupNotice(Roar):
    """发送群公告
    ---
    参数

    | 字段名      | 数据类型  | 默认值 | 说明    |
    | ---------- | ------- | ----- | ------ |
    | `group_id` | int64   |       | 群号    |
    | `content`  | string  |       | 公告内容 |
    """
    _extend_url = "_send_group_notice"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self

    def set_content(self, content: str):
        self['content'] = content
        return self


class ReloadEventFilter(Roar):
    """重载事件过滤器
    ---
    参数

    | 字段名  | 数据类型 | 默认值 | 说明 |
    | -----  | -------- | ----- | ---- |
    | `file` | string | - | 事件过滤器文件 |
    """
    _extend_url = "reload_event_filter"

    def set_file(self, file: str):
        """事件过滤器文件"""
        self['file'] = file
        return self


class DownloadFile(Roar):
    """下载文件到缓存目录
    ---
    参数

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `url` | string  | 链接地址                      |
    | `thread_count` | int32  | 下载线程数            |
    | `headers` | string or array  | 自定义请求头    |

    `headers`格式:

    字符串:

    ```
    User-Agent=YOUR_UA\\r\\nReferer=https://www.baidu.com
    ```

    JSON数组:

    ```json
    [
        "User-Agent=YOUR_UA",
        "Referer=https://www.baidu.com"
    ]
    ```

    响应数据

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `file`    | string       |  下载文件的*绝对路径*        |
    """
    _extend_url = "download_file"

    def set_url(self, url: str):
        self['url'] = url
        return self

    def set_thread_count(self, count: int):
        """下载线程数"""
        self['count'] = count
        return self

    def set_headers(self, headers):
        """自定义请求头

        str: "User-Agent=YOUR_UA\\r\\nReferer=https://www.baidu.com"

        或者

        list: [
            "User-Agent=YOUR_UA",
            "Referer=https://www.baidu.com"
        ]

        """
        self['headers'] = headers
        return self


class GetOnlineClient(Roar):
    """获取当前账号在线客户端列表

    ---

    相应数据：

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `clients`    | []Device       |  在线客户端列表  |

    Device:

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `app_id`    | int64       |  客户端ID |
    | `device_name`    | string       |  设备名称 |
    | `device_kind`    | string       |  设备类型 |
    """
    _extend_url = "get_online_clients"

    def set_no_cache(self, no_cache: bool):
        """是否无视缓存"""

        self['no_cache'] = no_cache
        return self


class GetGroupMsgHistory(Roar):
    """获取群消息历史记录
    ---
    参数

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `message_seq` | int64  | 起始消息序号, 可通过 `get_msg` 获得  |
    | `group_id` | int64  | 群号            |

    响应数据

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `messages`    | []Message       |  从起始序号开始的前19条消息  |
    """
    _extend_url = "get_group_msg_history"

    def set_message_seq(self, message_seq: int):
        """ 起始消息序号, 可通过 `get_msg` 获得"""
        self['message_seq'] = message_seq
        return self

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class SetEssenceMessage(Roar):
    """设置精华消息
    ---
    **参数**

    | 字段         | 类型  | 说明   |
    | ------------ | ----- | ------ |
    | `message_id` | int32 | 消息ID |
    """
    _extend_url = "set_essence_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


class DeleteEssenceMessage(Roar):
    """移出精华消息
    ---
    **参数**

    | 字段         | 类型  | 说明   |
    | ------------ | ----- | ------ |
    | `message_id` | int32 | 消息ID |
    """
    _extend_url = "delete_essence_msg"

    def set_message_id(self, message_id: int):
        self['message_id'] = message_id
        return self


class GetEssenceMessageList(Roar):
    """获取精华消息列表
    ---
    **参数**

    | 字段       | 类型  | 说明 |
    | ---------- | ----- | ---- |
    | `group_id` | int64 | 群号 |

    **响应数据**

    响应内容为 JSON 数组，每个元素如下：

    | 字段名          | 数据类型 | 说明         |
    | --------------- | -------- | ------------ |
    | `sender_id`     | int64    | 发送者QQ 号  |
    | `sender_nick`   | string   | 发送者昵称   |
    | `sender_time`   | int64    | 消息发送时间 |
    | `operator_id`   | int64    | 操作者QQ 号  |
    | `operator_nick` | string   | 操作者昵称   |
    | `operator_time` | int64    | 精华设置时间 |
    | `message_id`    | int32    | 消息ID       |
    """
    _extend_url = "get_essence_msg_list"

    def set_group_id(self, group_id: int):
        self['group_id'] = group_id
        return self


class CheckUrlSafely(Roar):
    """检查链接安全性
    ---
    **参数**

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `url` | string  | 需要检查的链接  |

    **响应数据**

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `level`    | int       |  安全等级： 1安全 2未知 3危险  |
    """
    _extend_url = "check_url_safely"

    def set_url(self, url: str):
        self['url'] = url
        return self


class GetModelShow(Roar):
    """获取在线机型
    ---
    **参数**

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `model` | string  | 机型名称  |

    **响应数据**

    | 字段        | 类型       | 说明            |
    | ---------- | ---------- | ------------ |
    | `variants`    | array       |  可用的在线机型列表  |

    响应内容为 JSON 数组，每个元素如下：

    | 字段名          | 数据类型 | 说明         |
    | --------------- | -------- | ------------ |
    | `model_show` | string | 具体在线机型内容 |
    | `need_pay` | boolean | 是否需要付费使用 |
    """
    _extend_url = "_get_model_show"

    def set_model(self, model: str):
        self['model'] = model
        return self


class SetModelShow(Roar):
    """设置在线机型
    ---
    **参数**

    | 字段       | 类型   | 说明                      |
    | ---------- | ------ | ------------------------- |
    | `model` | string  | 机型名称  |
    | `model_show` | string  | -  |
    """
    _extend_url = "_set_model_show"

    def set_model(self, model: str):
        self['model'] = model
        return self

    def set_model_show(self, model_show: str):
        self['model_show'] = model_show
        return self


def doc():
    for c in allSubclasses(Roar):
        print("========================================")
        print(f"name: {c}")
        print(f"doc: {c.__doc__}")

        set_methods = [
            method for method in dir(c) if method.startswith("set_")
        ]
        print(f"set method: {set_methods}")
        print("========================================")


if __name__ == "__main__":
    doc()
