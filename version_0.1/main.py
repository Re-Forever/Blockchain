# coding: utf-8
# author = reforever
# time = 2020/5/15 11:14

import blockchain

if __name__ == "__main__":
    bc = blockchain.new_blockchain()
    bc.add_block("A send B 1BTC")
    bc.add_block("B send C 2BTC")
    for block in bc.blocks:
        print("block.version:", block.version)
        print("block.hash:", block.hash)
        print("block.prev_block_hash:", block.prev_block_hash)
        print("block.merkel_root:", block.merkel_root)
        print("block.timestamp:", block.timestamp)
        print("block.data:", block.data)
        print("----------------------------------")
