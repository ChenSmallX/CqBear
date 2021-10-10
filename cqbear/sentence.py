# -*- coding=utf-8 -*-
"""
实现 CQ-Code
"""

import json

from cqbear.util import allSubclasses


class CqCode(dict):
    _type = ""

    def __init__(self, data=None):
        if not self._type:
            raise NotImplementedError("Should use subclass of CqCode")
        if data:
            assert type(data) == dict
            self.update(data)

    def __str__(self):
        data = ""
        for k, v in self.items():
            data += f",{k}={v}"
        return f"[CQ:{self._type}{data}]"

    def to_str(self):
        return str(self)


class Face(CqCode):
    _type = "face"

    def set_face_by_id(self, id: int):
        self['id'] = id
        return self


class At(CqCode):
    _type = "at"

    def set_user_id(self, user_id: int):
        self['qq'] = user_id
        return self

    def set_name(self, at_name: int):
        """当在群中找不到此QQ号的名称时才会生效"""
        self['name'] = at_name
        return self


class ShareLink(CqCode):
    _type = "share"

    def set_url(self, url: str):
        self['url'] = url
        return self

    def set_title(self, title: str):
        self['title'] = title
        return self

    def set_content(self, content: str):
        self['content'] = content
        return self

    def set_image(self, image_url: str):
        self['image'] = image_url
        return self


class SharePlatformMusic(CqCode):
    _type = "music"

    def set_source(self, source: str):
        """'qq', '163', 'xm'"""
        assert (source in ['qq', '163', 'xm'])
        self['type'] = source
        return self

    def set_music_id(self, music_id: int):
        self["id"] = music_id
        return self


class ShareCustomMusic(CqCode):
    _type = "music"

    def __init__(self):
        super().__init__()
        self['type'] = 'custom'

    def set_url(self, url: str):
        """击后跳转目标 URL"""
        self['url'] = url
        return self

    def set_music_url(self, music_url: str):
        """音乐 URL"""
        self['audio'] = music_url
        return self

    def set_title(self, title: str):
        self['title'] = title
        return self

    def set_content(self, content: str):
        self['content'] = content
        return self

    def set_image_url(self, image_url: str):
        self['image'] = image_url
        return self


class Image(CqCode):
    _type = "image"

    def set_file_path(self, file_path: str):
        self['file'] = file_path
        return self

    def set_type(self, image_type: str):
        """图片类型, `flash` 表示闪照, `show` 表示秀图, 默认普通图片"""
        assert (image_type in ['flash', 'show'])
        self['type'] = image_type
        return self

    def set_url(self, url: str):
        self['url'] = url
        return self

    def set_cache(self, is_cache: bool):
        """只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 True"""
        self['cache'] = int(is_cache)
        return self

    class AFFECT_ID():
        NORMAL = 40000
        """普通"""
        PHANTOM = 40001
        """幻影"""
        SHAKE = 40002
        """抖动"""
        BIRTHDAY = 40003
        """生日"""
        LOVE_YOU = 40004
        """爱你"""
        LOOKING_FOR_FRIEND = 40005
        """征友"""

    def set_affect_id(self, affect_id: int):
        """
        - 发送秀图时的特效id, 默认为40000（普通）
        - 特效列表为Image.AFFECT_ID.XXX
        """
        self['id'] = affect_id
        return self

    def set_download_thread_count(self, count: int):
        """通过网络下载图片时的线程数, 默认单线程. (在资源不支持并发时会自动处理)"""
        self['c'] = count
        return self


class Reply(CqCode):
    _type = "reply"

    def set_id(self, id: int):
        """
        - 回复时所引用的消息id, 必须为本群消息.
        - 优先级低于 set_text

        如果 `id` 和 `text` 同时存在, 将采用自定义reply并替换原有信息
        如果 `id` 获取失败, 将回退到自定义reply
        """
        self['id'] = id
        return self

    def set_text(self, text: str):
        """
        - 自定义回复的信息
        - 优先级高于 set_id

        如果 `id` 和 `text` 同时存在, 将采用自定义reply并替换原有信息
        如果 `id` 获取失败, 将回退到自定义reply
        """
        self['text'] = text
        return self

    def set_user_id(self, user_id: int):
        """自定义回复时的自定义QQ, 如果使用自定义信息必须指定."""
        self['qq'] = user_id
        return self

    def set_reply_time(self, time: int):
        """自定义回复时的时间, 格式为Unix时间"""
        self['time'] = time
        return self

    def set_seq(self, seq: int):
        """起始消息序号, 可通过 `get_msg` 获得"""
        self['seq'] = seq
        return self


class Poke(CqCode):
    _type = "poke"

    def set_user_id(self, user_id: int):
        self['qq'] = user_id
        return self


Chuo1Chuo = Poke


class ForwardRecive(CqCode):
    _type = "forward"


class ForwardSend(CqCode):
    """
    使用 `cqbear.roar.SendGroupForwardMessage` 类承接此类实例

    `sgfm = SendGroupForwardMessage().add_message(ForwardSend())`
    `bear.mouth.speak(sgfm)`
    """
    _type = "node"

    def set_node_id(self, id: int):
        """转发消息id

        直接引用他人的消息合并转发, 实际查看顺序为原消息发送顺序

        与其他的set_xxx自定义消息二选一"""
        self['id'] = id
        return self

    def set_node_user_name(self, name: str):
        self['name'] = name
        return self

    def set_user_id(self, user_id: int):
        self['uin'] = user_id
        return self

    def set_content(self, content: str):
        """**不支持转发套娃**"""
        self['content'] = content
        return self

    def set_seq(self, seq: int):
        self['seq'] = seq
        return self

    def __str__(self):
        return json.dumps(dict(self))


class Xml(CqCode):
    _type = "xml"

    def set_xml_data(self, data: str):
        """xml内容, xml中的value部分, 记得实体化处理"""
        self['data'] = data
        return self

    def set_resid(self, resid: int):
        self['resid'] = resid
        return self


class Json(CqCode):
    _type = "json"

    def set_xml_data(self, data: str):
        """xml内容, xml中的value部分, 记得实体化处理"""
        self['data'] = data
        return self

    def set_resid(self, resid: int):
        self['resid'] = resid
        return self


class Text2Voice(CqCode):
    _type = "tts"

    def set_text(self, text: str):
        self['text'] = text
        return self


class CqCodeUnderstander:
    _understand_map = {}

    def __init__(self) -> None:
        cq_code_list = allSubclasses(CqCode)
        for cq_code in cq_code_list:
            # 此处包含 "": CqCode
            self._understand_map[cq_code._type] = cq_code

    @staticmethod
    def parse_str_cqcode(str_cqcode: str):
        ret = {
            "CQ": "",
            "data": {}
        }
        if str_cqcode.startswith("[CQ:") and str_cqcode.endswith("]"):
            str_cqcode = str_cqcode[1:-1]  # 不用 strip 是为了防止末尾存在 ...]]] 的情况
            args = str_cqcode.split(',')

            cq = args.pop(0)
            cq = cq.split(":")
            ret["CQ"] = cq[1] if cq[1] is not None else ""

            for arg in args:
                t_arg = arg.split("=")
                ret['data'][t_arg[0]] = t_arg[1]
        return ret

    def understand(self, str_cqcode: str):
        cqcode_dict = self.parse_str_cqcode(str_cqcode)
        if cqcode_dict:
            cqcode = self._understand_map.get(cqcode_dict.get('CQ'))
            if cqcode and type(cqcode) != CqCode:
                return cqcode(cqcode_dict['data'])
