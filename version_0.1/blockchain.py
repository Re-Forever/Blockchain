# coding: utf-8
# author = reforever
# time = 2020/5/15 10:02

import block


def new_blockchain():
    head_block = block.new_genesis_block()
    blockchain = Blockchain()
    blockchain.blocks.append(head_block)
    return blockchain


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, data):
        prev_block_hash = self.blocks[-1].hash
        new_block = block.new_block(data, prev_block_hash)
        self.blocks.append(new_block)


# bc = new_blockchain()
# bc.add_block("1")
# print(bc.blocks[1].prev_block_hash)
