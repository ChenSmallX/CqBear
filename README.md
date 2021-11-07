# CqBear: QQ 机器熊框架

A bear-like bot python module for go-cqhttp.

一款 go-cqhttp 服务端的“类熊” QQ 机器人 python 框架。

> 将机器人称作熊 `Bear`，
> 将接受到的消息事件称作声音 `Sound`，
> 将发出的控制消息称作吼叫 `Roar`，
> 将规范化的符号表达(例如 at、图片等)称为句子 `Sentence`，
> 将事件驱动回调称为反应 `react`，
> 将计划任务称为记忆 `remember` 和 `job` 等。

## 环境准备

CqBear 充当的是一个 go-cqhttp 行为的控制器的角色，所以真正的 QQ 是运行在 go-cqhttp 中的，CqBear 只是提供了一个 python 语言的 go-cqhttp API 层。
所以在使用 CqBear 之前，需要先准备好 go-cqhttp。

### 下载并运行 go-cqhttp

#### 下载

- Windows PC

    下载：[go-cqhttp_windows_386.exe(32位系统)](https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp_windows_386.exe) 或 [go-cqhttp_windows_amd64.exe(64位系统)](https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp_windows_amd64.exe) (链接均链接到最新的 go-cqhttp 构建件)

- 其他系统环境

    前往 go-cqhttp 的 github-release 下载 **对应环境** 的预编译程序即可。

    > <https://github.com/Mrs4s/go-cqhttp/releases>

    解压 `.tar.gz` 包命令：

    ```sh
    tar -xzvf archive.tar.gz
    ```

- 自编译运行

    自行准备 Golang 环境。

    ```sh
    git clone https://github.com/Mrs4s/go-cqhttp.git
    cd go-cqhttp
    go build -ldflags "-s -w -extldflags '-static'"
    ```

    构建前可以使用 goproxy 国内代理来加速 go 依赖安装速度。

    ```sh
    go env -w GOPROXY=https://goproxy.cn,direct
    ```

    具体 go-cqhttp 构建文档：<https://docs.go-cqhttp.org/guide/quick_start.html#%E5%A6%82%E4%BD%95%E8%87%AA%E5%B7%B1%E6%9E%84%E5%BB%BA>。

#### 运行 go-cqhttp

首次运行 go-cqhttp 在选择通信方式后(CqBear 使用的是 HTTP 通信)会自动生成 config.yml 配置文件，修改 config.yml 中必要的配置和与 cqbear 相关的配置后，重启 go-cqhttp 即可。

> windows 端 双击运行
>
> linux 端 `./go-cqhttp`(首次运行推荐不带参数运行) 或 `./go-cqhttp faststart`(跳过各项检查，快速启动)

其中必要的配置：

- `account.uin`： QQ 账号
- `account.password`：密码，若使用扫码登录则无需填写这项

其中与 cqbear 相关的配置如下：

- `servers.http.host`: go-cqhttp 服务监听的地址，若和 cqbear 运行在同一台机器中，则填写 "127.0.0.1"，若不同则填写 "0.0.0.0"【此项需要在 cqbear 中使用】
- `servers.http.port`: go-cqhttp 服务监听的端口，可以使用默认的 `5700`，也可以自定义【此项需要在 cqbear 中使用】
- `servers.http.post.url`: cqbear 或其他接收 go-cqhttp 上报消息的服务端，此处可填写 "127.0.0.1:5701" 或其他地址【此项需要在 cqbear 中使用】

### CqBear 快速开始 Quick Start

#### 安装

```sh
python -m pip install cqbear
```

#### 示例

```py
from cqbear.bear import CqBear
from cqbear.roar import (
    SendPrivateMessage,
    SendGroupMessage
)
from cqbear.sound import (
    FriendPrivateMessage,
    NormalGroupMessage
)
from cqbear.sentence import At

@CqBear.react(NormalGroupMessage)  # 对 NormalGroupMessage 消息进行反应操作
def reply_group(bear: CqBear, msg: NormalGroupMessage):
    """
    监听并回复群消息
    """
    # 检查群号是否为 66666 以及 是否 at 了自己
    if msg.group_id == 66666 and At().set_user_id(12345).has_me(msg.raw_message):
        roar = SendGroupMessage()  # 创建群消息
        roar.set_group_id(msg.group_id)     # 设置群号
        roar.set_message("why you at me?")  # 设置消息内容
        bear.speak(roar)  # 发送消息

@CqBear.react(FriendPrivateMessage)  # 对 FriendPrivateMessage 消息进行反应操作
def reply_friend(bear: CqBear, msg: FriendPrivateMessage):
    """
    监听并回复好友信息
    """
    # 检查私聊好友的 QQ 号是否为 987654321
    if msg.user_id == 987654321:
        roar = SendPrivateMessage()      # 创建私聊消息
        roar.set_user_id(msg.user_id)    # 设置对方 QQ 号
        roar.set_message("this is an example message")  # 设置消息内容
        bear.speak(roar)  # 发送消息

bear = CqBear(
    addr="127.0.0.1",       # cqbear 监听的地址
    port=5701,              # cqbear 监听的端口
    cq_addr="127.0.0.1",    # go-cqhttp 监听的地址
    cq_port=5700,           # go-cqhttp 监听的端口
    qq=12345                # 当前机器人的 qq 号
)
bear.start()                # 开始监听消息
```

### 初级使用指南

建议使用带有 **【自动补全】** 和 **【提示doc】** 的 IDE 或 编辑器进行编码！

建议使用带有 **【自动补全】** 和 **【提示doc】** 的 IDE 或 编辑器进行编码！

建议使用带有 **【自动补全】** 和 **【提示doc】** 的 IDE 或 编辑器进行编码！

> 重要的事情说三遍。

cqbear 的核心组件为 CqBear，定义在 cqbear.bear 中，可使用 `from cqbear.bear import CqBear` 引入。

#### 熊

- `cqbear.bear.CqBear`

    > 熊
    >
    > 完整的 QQ 机器熊类，包括了自动监听 go-cqhttp 上报消息、对不同的声音(消息)类型执行对应的反应回调、定时执行记忆(计划)任务等功能。

    最基础的创建熊实例和开始运行：

    ```py
    from cqbear.bear import CqBear
    bear = CqBear(
        addr="127.0.0.1",       # cqbear 监听的地址
        port=5701,              # cqbear 监听的端口
        cq_addr="127.0.0.1",    # go-cqhttp 监听的地址
        cq_port=5700,           # go-cqhttp 监听的端口
        qq=12345                # 当前机器人的 qq 号
    )
    bear.start()                # 开始监听声音和执行定时任务
    ```

    可以通过 **装饰器** 注册声音反应和记忆任务，但是所有 **使用装饰器注册的** 声音反应和记忆任务必须定义在 **创建 CqBear 实例之前** 。装饰器类型：

    1. 注册声音反应：`@CqBear.react(Sound_Type)`
    2. 注册记忆任务：`@CqBear.remember(remember.Job)`

    在 CqBear 实例开始运行后，需要使用 CqBear 实例的 `add_react` 和 `add_remember` 方法动态地添加声音反应和记忆任务。

  - 注册声音(消息)反应

    例：

    ```py
    from cqbear.bear import CqBear
    from cqbear.sound import NormalGroupMessage

    @CqBear.react(NormalGroupMessage)
    def foo(bear: CqBear, msg: NormalGroupMessage):
        ...
    ```

    声音类型定义在 `cqbear.sound` 中，定义的回调函数 **需要且只要** 2个参数：

    - bear： 监听到消息的 CqBear 实例
    - msg： 监听的消息类型实例

    动态添加声音事件反应回调的方法：

    ```py
    from cqbear.bear import CqBear
    from cqbear.sound import NormalGroupMessage
    bear = CqBear(...)
    # bear 已经被初始化和正在运行

    # 定义回调函数
    def bar(bear: CqBear, msg: NormalGroupMessage):
        ...

    # 添加对应声音类型的反应回调
    bear.add_react(NormalGroupMessage, bar)
    ```

  - 注册记忆(计划)任务

    例：

    ```py
    from cqbear.bear import CqBear
    from cqbear.remember import every

    @CqBear.remember(every().hour.at(":0:0"))  # 每 1 小时的 0 分 0 秒执行
    def foo(bear: CqBear):
        ...

    # 更多记忆任务装饰器使用例子
    @CqBear.remember(every(2).minute.at("::24"))  # 每 2 分钟的 24 秒执行
    @CqBear.remember(every(3).day.at("15:30:00"))  # 每 3 天的 15：30 执行
    @CqBear.remember(every().Tuesday.at("5:30:00"))  # 每 周二 的 5：30 执行
    @CqBear.remember(every().Friday)  # 每 周五 的 {当前 bear 程序运行时间} 执行
    @CqBear.remember(every().month_day(7).at("15"))  # 每个月的 7 日的 15：00 执行
    import calendar
    @CqBear.remember(every().week_day(calendar.SUNDAY).at("3:24"))  # 每周日的 3：24 执行
    ```

    记忆任务的控制主体为 `cqbear.remember.Remember` 和 `cqbear.remember.Job`，前者为任务轮询和执行组件，后者为任务定义和检测组建。其中，CqBear 中已经内置了一个 `Remember` 实例用于执行定义好的 `Job`。

    **通过装饰器注册** 的记忆任务的参数 **需要且只要** 1 个参数。`注意：是通过装饰器注册的记忆任务才有这项约束`

    - bear：用于执行任务的 CqBear 实体

    动态添加记忆任务的方法：

    ```py
    from cqbear.bear import CqBear
    from cqbear.remember import every, Job
    bear = CqBear(...)
    # bear 已经被初始化和正在运行

    def foo(bear: CqBear):  # 使用 bear 作为参数的回调函数
        ...

    def bar(func: Callable, *args, **kwargs):  # 传入一个回调以及任意参数的函数
        ...

    def foobar(bear: CqBear): # 同样使用 bear 作为参数的回调函数
        ...

    # 定义一个 Job 实体，并在 to_do 方法中传入其调用的任务函数和要使用的参数
    # Job 的 to_do 方法接受一个回调函数 以及若干个回调函数需要的参数，此处传入的 bear 为 foo 需要的参数
    job_a = every(2).hour.at("4:00:00").to_do(foo, bear)

    # 也可直接通过 cqbear.remember.Job 创建 Job 实体，并通过 Job 自身的 every 方法指定间隔单位个数
    # 此处传入的 bar 为回调函数，而后续的 foo 和 bear 为 bar 需要的参数
    job_b = Job().every(15).minute.at("::20").to_do(bar, foo, bear)

    # 定义一个没有配置 执行回调函数 的记忆任务
    job_c = every(30).second

    # 将 job_a 和 job_b 注册到 bear 中
    bear.add_remember(job_a)  # 当没有传入函数作为参数时，需要保证 job_a.runable 为真值
    bear.add_remember(job_b)
    # 当传入的 job_c 没有配置执行函数时，可以给 add_remember 方法加上一个接受 bear 为参数的函数作为入参，add_remember 方法会自动将对应的 bear 实体传入此函数。
    # 当传入的 job_c 也已经绑定了函数，则 add_remember 的函数入参不生效(不覆盖 job_c 的执行函数)。
    bear.add_remember(job_c, foobar)
    ```

#### 声音(消息) cqbear.sound

> 声音的基类 `Sound`

CqBear 中产生的声音是从 go-cqhttp 端主动上报到 CqBear 的监听端口中，并由 `SonudUnderstander` 解析并实例化的。可以直接通过 `.` 来访问声音中所带有的参数，例如：

```py
@CqBear.react(NormalGroupMessage)
def reply_group(bear: CqBear, msg: NormalGroupMessage):
    group_id = msg.group_id
    sender_id = msg.user_id
    sender_detail = msg.sender
    message = msg.message
    raw_message = msg.raw_message  # raw_message 为纯字符串，message 则会是未转换前的消息格式
    ...
```

在编码的过程中可以通过有自动补全和提示doc的编码工具进行编码以获得最佳的体验。

获得所有声音类型和说明的方法：

```sh
$ python
>>> from cqbear.sound import doc as sound_doc
>>> sound_doc()
```

每种声音的详细参数以及描述可以在 [go-cqhttp 的事件文档](https://docs.go-cqhttp.org/event/)中获取。

> 如果发现有未实现的声音，请提交相关 issue 或 pr。

#### 吼叫(API指令) cqbear.roar

> 吼叫的基类 `Roar`

CqBear 中使用的吼叫是对 go-cqhttp api 的一层封装起到更好用的作用，在创建吼叫实例后，可使用实例的 `.set_xxx` 方法对其参数进行设置，例如：

```py
@CqBear.react(FriendPrivateMessage)
def reply_friend(bear: CqBear, msg: FriendPrivateMessage):
    roar = SendPrivateMessage()    # 吼叫
    roar.set_user_id(msg.user_id)
    roar.set_message("你好呀~")
    bear.speak(roar)  # 在 speak 之后，可继续编辑 roar 用于再次发送
    ...
```

在编码的过程中可以通过有自动补全和提示doc的编码工具进行编码以获得最佳的体验。

获得所有吼叫类型和说明的方法：

```sh
$ python
>>> from cqbear.roar import doc as roar_doc
>>> roar_doc()
```

每种吼叫的详细参数以及描述可以在 [go-cqhttp 的 API 文档](https://docs.go-cqhttp.org/api/)中获取。

> 如果发现有未实现的吼叫，请提交相关 issue 或 pr。

#### 句子(CQ code) cqbear.sentence

> 句子的基类 `Sentence`

CqBear 中将 CoolQ 中的 CQCode 概念称作句子，用于表示消息中中的各种元素，例如 at(`At`)，回复(`Reply`)，图片(`Image`)，表情(`Face`) 等。句子可以被发出也可以被收到，所以关于句子的使用方法会稍微多一些。

- 创建句子实例并设置参数。句子中也是需要有参数来丰富的，例如 at 句子需要有被 at 对象的 qq 号码，必要时还需要设置 at 时展示的文字等。设置参数时，可以使用实例的 `.set_xxx` 方法对参数进行设置，以及可以将创建的句子实体转换成，例：

    ```py
    from cqbear.sentence import At, Reply, Image
    at = At().set_user_id(123456)
    reply = Reply().set_message_id(-1588745453)
    image = Image().set_file_name("a.jpg").set_utl("https://xxx.xxx/xxx/a.jpg")

    print(at.to_str())
    print(str(reply))
    ```

- 从消息的 raw_message 中提取句子列表。CqBear 中内置了对句子的解析和识别功能，提供方便的代码开发流程。例：

    ```py
    from cqbear.sentence import SentenceUnderstander, At

    @CqBear.react(FriendPrivateMessage)
    def reply_friend(bear: CqBear, msg: FriendPrivateMessage):
        str_list, sentence_list = SentenceUnderstander.extract_sentence(msg.raw_message)
        for sentence in sentence_list:
            if isinstance(sentence, At):
                ...
    ```

- 检查消息中是否包含了某特定句子，例：

    ```py
    from cqbear.sentence import SentenceUnderstander, At
    from cqbear.sound import NormalGroupMessage

    @CqBear.react(NormalGroupMessage)
    def reply_friend(bear: CqBear, msg: NormalGroupMessage):
        if At().set_user_id(bear.qq).has_me(msg.raw_message):
            ...
    ```

在编码的过程中可以通过有自动补全和提示doc的编码工具进行编码以获得最佳的体验。

获得所有句子类型和说明的方法：

```sh
$ python
>>> from cqbear.sentence import doc as sentence_doc
>>> sentence_doc()
```

每种吼叫的详细参数以及描述可以在 [go-cqhttp 的 CQcode 文档](https://docs.go-cqhttp.org/cqcode/)中获取。

> 如果发现有未实现的句子，请提交相关 issue 或 pr。

#### 熊身体的其他部分(不建议独立使用)

CqBear 中定义了多个组件分别用于执行不同的工作，但在 CqBear 种都进行了二次封装，无法直接通过 CqBear 控制，若需要单独使用其中某项功能，则可以独立定义使用：

- `cqbear.bear.BearEar`

    > 耳朵：
    >
    > 顾名思义，是用于听声音(消息)的的。
    >
    > cqbear 将消息定义为了 N 种声音(`Sound`)，可在 `cqbear.sound` 中获得所有声音的定义。

    `BearEar` 中使用多线程创建了基于 `Flask` 的 http 服务端。后续有计划将 `Flask` 更换为基于 socket 的 http 服务端。

    单独使用 `BearEar`，可以创建一个可以监听 go-cqhttp 上报消息的服务端，获取到的不同类型的消息会转为具体的声音类实体并存储在声音队列中，可通过 `BearEar.get_sound` 方法获取一个声音实体。

    独立使用 BearEar 的例子：

    ```py
    from cqbear.bear import BearEar
    ear = Bear(
        addr="127.0.0.1",
        port=5701,
        secret=""    # 为了兼容 go-cqhttp 对上报消息加密功能预留的接口，暂时还未实现
    )
    ear.start_listen()  # start_listen 中使用了多线程，是个非阻塞的方法

    while True:
        sound = ear.get_sound()  # 从声音队列中获取一个声音
        ...

        if ...:
            ear.clear_sound()               # 清空声音队列
        if ... and ear.is_listening:        # 可使用 is_listening 判断 ear 当前是否会将声音推入队列
            ear.ignore_sound()              # 可使用 ignore_sound 控制 ear 不将声音存入声音队列
        if ... and not ear.is_listening:
            ear.listen_sound()              # 可使用 listen_sound 控制 ear 开始将声音存入声音队列，默认情况为开启
        if ...:
            break

    ear.stop_listen()  # 停止监听进程
    ```

- `cqbear.bear.BearMouth`

    > 嘴巴：
    >
    > 熊通过嘴巴说话(向 go-cqhttp 发出消息)。
    >
    > cqbear 将发出消息定义为了 N 种熊吼(`Roar`)，可在 `cqbear.roar` 种获得所有熊吼的定义。

    `BearMouth` 是一个可以将熊吼 Roar 转为 http 请求(`request`)发送到 go-cqhttp，并返回请求的回应(`response`)。

    `BearMouth` 可单独定义实体并用于发送熊吼，例：

    ```py
    import datetime
    import time
    from cqbear.bear import BearMouth
    from cqbear.roar import SendGroupMessage

    mouth = BearMouth(
        addr="127.0.0.1",   # go-cqhttp 监听的地址
        port=5700           # go-cqhttp 监听的端口
    )

    while True:
        time.sleep(0.5)

        # 一个简单的整点报时功能
        if datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
            group_roar = SendGroupMessage()
            group_roar.set_group_id(123456789).set_message(f"现在是{datetime.datetime.now().hour}点")

            # 也可以这样，只不过代码会显得比较长
            group_roar = SendGroupMessage().set_group_id(123456789).set_message(f"现在是{datetime.datetime.now().hour}点")

            if not mouth.speakable:  # 可以使用 speakable 判断当前 mouth 是否关闭了发送消息的功能
                mouth.free()  # 只有在 free 的情况下，speak方法才生效
            ret_code, ret_json_data = mouth.speak(roar)
            ...

        if ...:
            mouth.free()
        elif ...:
            mouth.shutup()

        if ...:
            break
    ```

- `cqbear.bear.BearBrain`

    > 大脑：
    >
    > 脑是熊思考的核心，“对声音做出反应”以及“记忆任务”都是在大脑中进行的。其中“对声音做出反应”的声音是从耳朵中获取的。

    `BearBrain` 会将声音反应(声音类型和回调函数的关系)和记忆任务(计划任务实例和计划任务控制模块)保存起来，在启动 BearBrain 的“思考”机制后，会通过给定的接口去获取声音并执行对应的函数，或检查是否到了执行计划任务的时间要去执行设定好的任务。

    `BearBrain` 可以单独使用，但需要自己定义许多东西。例如：

    ```py
    from cqbear.bear import BearBrain
    from cqbear.sound import (
        Sound,
        NormalGroupMessage,
        FriendPrivateMessage,
        AnonymousGroupMessage
    )
    from cqbear.remember import Job
    from typing import Optional

    def get_sound() -> Optional[Sound]:  # 定义一个用于获取声音的函数 返回 None 的时候 brain 不做操作
        ...

    react_map = {
        NormalGroupMessage: [foo],
        FriendPrivateMessage: [foo, bar]
    }  # 声音类型和回调 *列表* 的对应关系
    remember_map = {
        Job().every().hour.at(":24:00"): foobar
    }  # 计划任务和回调函数的对应关系

    brain = BearBrain(
        bear=None,
        listen_cb=get_sound,    # 传入一个获取声音的函数，一般是 BearEar.get_sound 方法
        speak_cb=None,          # speak_cb 暂时还没有功能依赖，所以可以传入 None
        react_map=react_map,        # 将两个 map 传入
        remember_map=remember_map
    )

    if not brain.is_thinking:   # brain 不可重复 start_think
        brain.start_think()     # start_think 使用了多线程，所以是不阻塞的

    brain.add_react(AnonymousGroupMessage, foooobarar)  # 动态添加声音反应和记忆任务
    brain.add_remember(Job()..., barfoo)

    if brain.is_thinking:
        brain.stop_think()
    ```
