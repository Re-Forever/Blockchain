# coding: utf-8
# author = reforever
# time = 2020/5/14 17:14

import time
import gmssl.sm3


def new_block(data, prev_block_hash):
    block = Block()
    block.version = 1
    block.prev_block_hash = prev_block_hash
    block.timestamp = int(time.time())
    block.data = data
    block.hash = block.set_hash()
    return block


def new_genesis_block():
    return new_block(data="Genesis Block", prev_block_hash="")


class Block:

    def __init__(self):
        self.version = 0
        self.hash = ""
        self.prev_block_hash = ""
        self.merkel_root = ""
        self.timestamp = 0
        # self.bits = 0
        # self.nonce = 0
        self.data = None

    def set_hash(self):
        tmp = [
            str(self.version),
            self.prev_block_hash,
            self.merkel_root,
            str(self.timestamp),
            self.data
        ]
        data = "".join(tmp).encode()
        return gmssl.sm3.sm3_hash(list(data))
