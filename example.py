# -*- coding=utf-8 -*-

from cqbear import CqBear

bear = CqBear(
    addr="127.0.0.1",
    port="5701",
    cq_addr="127.0.0.1",
    cq_port="5700",
    qq="2085861497"
)

bear.start()
