# coding: utf-8
# author = reforever
# time = 2020/5/15 11:43

"""
工作量证明 proof of work
target为目标值，小于该值则算找到
TargetBits 为target sm3 hash的前几位中有多少个0
"""

import Crypto.Util.number
import gmssl.sm3
import cmath
TargetBits = 12
MaxInt64 = 1 << 63 - 1


def new_proof_of_work(aim_block):
    target = 1 << (256 - TargetBits)
    return ProofOfWork(aim_block, target)


class ProofOfWork:
    def __init__(self, aim_block=None, target=0):
        self.aim_block = aim_block
        self.target = target

    def prepare_data(self, nonce):
        self.aim_block.bits = TargetBits
        self.aim_block.nonce = nonce
        tmp = [
            str(self.aim_block.version),
            self.aim_block.prev_block_hash,
            self.aim_block.merkel_root,
            str(self.aim_block.timestamp),
            str(self.aim_block.bits),
            str(self.aim_block.nonce),
            self.aim_block.data
        ]
        # print(tmp)
        data = "".join(tmp).encode()
        return data

    def run(self):
        print("Begin Mining...")
        print("target hash = %064x" % self.target)
        nonce = 1
        while nonce < MaxInt64:
            data = self.prepare_data(nonce)
            # print("data:", list(data))
            hash = gmssl.sm3.sm3_hash(list(data))
            hash_int = int(hash, 16)
            if hash_int < self.target:
                print("found nonce, nonce = %d, hash = %s\n" % (nonce, hash))
                return nonce, hash
            nonce += 1

    def is_valid(self):
        data = self.prepare_data(self.aim_block.nonce)
        hash_int = int(gmssl.sm3.sm3_hash(list(data)), 16)
        if hash_int < self.target:
            return True
        else:
            return False
