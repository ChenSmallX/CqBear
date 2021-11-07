# -*- coding=utf-8 -*-
"""
实现 CQ-Code
"""

import json
from typing import Union

from cqbear.util import allSubclasses


class Sentence(dict):
    """Sentence 基类"""
    _type = ""

    def __init__(self, data=None):
        if not self._type:
            raise NotImplementedError("Should use subclass of Sentence")
        if data:
            assert type(data) == dict
            self.update(data)

    def __str__(self):
        data = ""
        for k, v in self.items():
            data += f",{k}={v}"
        return f"[CQ:{self._type}{data}]"

    def __repr__(self) -> str:
        return f"<{self.__class__}: {self.__str__()}>"

    def to_str(self):
        return str(self)

    def has_me(self, msg: str):
        """返回列表，列表包含消息中和当前sentence相匹配的sentence

        - 匹配规则：

            类型相同，且当前Sentence中设置了的属性在传入Sentence中相同

            例如：[CQ:at,qq=123] 可以匹配 [CQ:at,qq=123,name=hello]，反之不匹配

        Return:
            list[Sentence]
        """
        ret = []
        _, sentence_list = SentenceUnderstander.extract_sentence(msg)
        for sentence in sentence_list:
            if self == sentence:
                ret.append(sentence)
        return ret

    def __eq__(self, o) -> bool:
        if self.__class__ != o.__class__:
            return False
        if self._type != o._type:
            return False
        for k in self.keys():
            if k not in o.keys():
                return False
            if str(self[k]) != str(o[k]):
                return False
        return True


class Face(Sentence):
    """QQ 表情"""
    _type = "face"

    def set_face_by_id(self, id: int):
        """QQ 表情 ID"""
        self['id'] = id
        return self


# TODO: 语音 type==record
# TODO: 短视频 type==video


class At(Sentence):
    """@某人"""
    _type = "at"

    def set_user_id(self, user_id: Union[int, str]):
        """@的 QQ 号, `all` 表示全体成员"""
        self['qq'] = user_id
        return self

    def set_name(self, at_name: int):
        """当在群中找不到此QQ号的名称时才会生效"""
        self['name'] = at_name
        return self


class ShareLink(Sentence):
    """链接分享"""
    _type = "share"

    def set_url(self, url: str):
        """URL"""
        self['url'] = url
        return self

    def set_title(self, title: str):
        """标题"""
        self['title'] = title
        return self

    def set_content(self, content: str):
        """发送时可选, 内容描述"""
        self['content'] = content
        return self

    def set_image(self, image_url: str):
        """发送时可选, 图片 URL"""
        self['image'] = image_url
        return self


class SharePlatformMusic(Sentence):
    """音乐分享：三大平台平台"""
    _type = "music"

    def set_source(self, source: str):
        """'qq', '163', 'xm'

        分别表示使用 QQ 音乐、网易云音乐、虾米音乐"""
        assert (source in ['qq', '163', 'xm'])
        self['type'] = source
        return self

    def set_music_id(self, music_id: int):
        """歌曲 ID"""
        self["id"] = music_id
        return self


class ShareCustomMusic(Sentence):
    """音乐分享：自定义链接"""
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
        """标题"""
        self['title'] = title
        return self

    def set_content(self, content: str):
        """发送时可选, 内容描述"""
        self['content'] = content
        return self

    def set_image_url(self, image_url: str):
        """发送时可选, 图片 URL"""
        self['image'] = image_url
        return self


class Image(Sentence):
    """图片"""
    _type = "image"

    def set_file_name(self, file_name: str):
        """图片文件名"""
        self['file'] = file_name
        return self

    def set_type(self, image_type: str):
        """图片类型, `flash` 表示闪照, `show` 表示秀图, 默认普通图片"""
        assert (image_type in ['flash', 'show'])
        self['type'] = image_type
        return self

    def set_url(self, url: str):
        """图片 URL"""
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


class Reply(Sentence):
    """回复"""
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
        """起始消息序号, 可通过 `cqbear.roar.GetMessage` 获得"""
        self['seq'] = seq
        return self


# TODO: 红包 redbag


class Poke(Sentence):
    """戳一戳"""
    _type = "poke"

    def set_user_id(self, user_id: int):
        """需要戳的成员"""
        self['qq'] = user_id
        return self


Chuo1Chuo = Poke


# TODO: 礼物 gift


class ForwardRecive(Sentence):
    """合并转发（收）

    需要通过 `cqbear.roar.GetForwardMessage` 获取转发的具体内容"""
    _type = "forward"

    def set_id(self, id: str):
        """合并转发ID
        """
        self['id'] = id
        return self


class ForwardSend(Sentence):
    """合并转发（发）

    使用 `cqbear.roar.SendGroupForwardMessage` 类承接此类实例

    `sgfm = SendGroupForwardMessage().add_message(ForwardSend())`
    `bear.speak(sgfm)`
    """
    _type = "node"

    def __init__(self, data=None):
        super().__init__(data=data)
        self['type'] = "node"
        self['data'] = {}

    def set_node_id(self, id: int):
        """转发消息id

        直接引用他人的消息合并转发, 实际查看顺序为原消息发送顺序

        与其他的set_xxx自定义消息二选一"""
        self['data']['id'] = id
        return self

    def set_node_user_name(self, name: str):
        self['data']['name'] = name
        return self

    def set_user_id(self, user_id: int):
        self['data']['uin'] = user_id
        return self

    def set_content(self, content: str):
        """**不支持转发套娃**"""
        self['data']['content'] = content
        return self

    def set_seq(self, seq: int):
        self['data']['seq'] = seq
        return self

    def __str__(self):
        return json.dumps(dict(self))


class Xml(Sentence):
    """XML 消息"""
    _type = "xml"

    def set_xml_data(self, data: str):
        """xml内容, xml中的value部分, 记得实体化处理"""
        self['data'] = data
        return self

    def set_resid(self, resid: int):
        """可以不填"""
        self['resid'] = resid
        return self


class Json(Sentence):
    """JSON 消息"""
    _type = "json"

    def set_json_data(self, data: Union[str, dict, list, int]):
        """json内容, json的所有字符串记得实体化处理

        json中的字符串需要进行转义，否则无法正确得到解析:

        `,` => `&#44;`

        `&` => `&amp;`

        `[` => `&#91;`

        `]` => `&#93;`
        """
        if not isinstance(data, str):
            data = json.dumps(data)
        data = data.replace(",", "&#44;").replace("&", "&amp;").replace("[", "&#91;").replace("]", "&#93;")
        self['data'] = data
        return self

    def set_resid(self, resid: int):
        """默认不填为0, 走小程序通道, 填了走富文本通道发送"""
        self['resid'] = resid
        return self


# TODO: cardimage


class Text2Voice(Sentence):
    """文本转语音

    通过TX的TTS接口, 采用的音源与登录账号的性别有关"""
    _type = "tts"

    def set_text(self, text: str):
        """内容"""
        self['text'] = text
        return self


class SentenceUnderstander:
    _understand_map = {}

    def __init__(self) -> None:
        cq_code_list = allSubclasses(Sentence)
        for cq_code in cq_code_list:
            # 此处包含 "": Sentence
            self._understand_map[cq_code._type] = cq_code

    @staticmethod
    def parse_str_sentence(str_sentence: str):
        ret = {
            "CQ": "",
            "data": {}
        }
        if str_sentence.startswith("[CQ:") and str_sentence.endswith("]"):
            str_sentence = str_sentence[1:-1]  # 不用 strip 是为了防止末尾存在 ...]]] 的情况
            args = str_sentence.split(',')

            cq = args.pop(0)
            cq = cq.split(":")
            ret["CQ"] = cq[1] if cq[1] is not None else ""

            for arg in args:
                t_arg = arg.split("=")
                ret['data'][t_arg[0]] = t_arg[1]
        return ret

    def understand(self, str_sentence: str):
        sentence_dict = self.parse_str_sentence(str_sentence)
        if sentence_dict:
            sentence = self._understand_map.get(sentence_dict.get('CQ'))
            if sentence and type(sentence) != Sentence:
                return sentence(sentence_dict['data'])

    @staticmethod
    def extract_sentence(raw_msg: str):
        str_list = []
        sentence_list = []

        left_point = 0
        right_point = -1
        index = 0

        seek_in_sentence = False
        bracket_level = 0

        while index < len(raw_msg):
            if left_point < right_point:
                tmp_s = raw_msg[left_point: right_point]
                str_list.append(tmp_s)
                if tmp_s.startswith("[CQ:") and tmp_s.endswith("]"):
                    sentence_list.append(tmp_s)
                left_point = right_point

            if not seek_in_sentence:
                if raw_msg[index:index+4] == "[CQ:":
                    right_point = index
                    seek_in_sentence = True
                    bracket_level += 1
            elif seek_in_sentence:
                if raw_msg[index] == "[":
                    bracket_level += 1
                elif raw_msg[index] == "]":
                    bracket_level -= 1
                if bracket_level == 0:
                    right_point = index + 1
                    seek_in_sentence = False
            index += 1

        if right_point != index - 1:
            tmp_s = raw_msg[left_point: index]
            str_list.append(tmp_s)
            if tmp_s.startswith("[CQ:") and tmp_s.endswith("]"):
                sentence_list.append(tmp_s)

        return str_list, [SentenceUnderstander().understand(sentence) for sentence in sentence_list]


def doc():
    for c in allSubclasses(Sentence):
        print("========================================")
        print(f"name: {c}")
        print(f"doc: {c.__doc__}")

        set_methods = [
            method for method in dir(c) if method.startswith("set_")
        ]
        print(f"set method: {set_methods}")
        print("========================================")

if __name__ == "__main__":
    s = "part1[CQ:at,qq=666][CQ:at,qq=667]part2 [CQ:face,id=12]"
    str_list, sentence_list = SentenceUnderstander.extract_sentence(s)
    print(f"str_list   : {str_list}")
    print(f"sentence_list: {sentence_list}")

    print(At().set_user_id(666) == At().set_user_id(666).set_name("haha"))
    print(At().set_user_id(666).set_name("haha") == At().set_user_id(666))
    print(At().has_me(s))
