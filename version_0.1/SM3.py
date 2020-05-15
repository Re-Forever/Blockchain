#!/usr/bin/env python
# coding=utf-8
# @author = reforever
# @mail = 1589626444@qq.com
# @time = 2019年12月31日 星期二 10时26分11秒

'''
Function List:
 1.SM3_256 入口函数
 2.SM3_init 缓冲区初始化
 3.SM3_process 压缩消息的第一个len/64块
 4.SM3_done 压缩剩余消息并产生Hash
 5.SM3_compress 压缩单个消息块
 6.BiToW 生成W
 7.WToW1 生成W1
 8.CF CF函数
 9.BigEndian 大小端系统转换
'''



import binascii
from math import ceil

SM3_T1 = 0x79cc4519
SM3_T2 = 0x7a879d8a
SM3_IVA = 0x7380166f
SM3_IVB = 0x4914b2b9
SM3_IVC = 0x172442d7
SM3_IVD = 0xda8a0600 
SM3_IVE = 0xa96f30bc
SM3_IVF = 0x163138aa 
SM3_IVG = 0xe38dee4d 
SM3_IVH = 0xb0fb0e4e



class SM3_STATE(object):
    def __init__(self):
        self.state = [0] * 8
        self.length = 0
        self.curlen = 0
        self.buf = [0] * 64        


def SM3_ff0(x, y, z):
    return (x ^ y ^ z)


def SM3_ff1(x, y, z):
    return ((x & y) | (x & z) | (y & z))  


def SM3_gg0(x, y, z):
    return (x ^ y ^ z)


def SM3_gg1(x, y, z):
    return ((x & y) | ((~x) & z))


def SM3_rotl32(x, n):
    _in = x << n
    a = _in & 0xffffffff
    b = (_in - a) >> 32
    return a + b 


def SM3_p0(x):
    return (x ^ SM3_rotl32(x, 9) ^ SM3_rotl32(x, 17))


def SM3_p1(x):
    return (x ^ SM3_rotl32(x, 15) ^ SM3_rotl32(x, 23))


'''
 Function: BiToW
 Description: 从Bi计算W
 Calls:
 Called By: SM3_compress
 Input: Bi[16]
 Output: W[64]
 Return: null
 Others:
'''
def BiToW(B, W):
    for i in range(16):
        W[i] = B[i]
    for i in range(16, 68):
        tmp = W[i-16] ^ W[i-9] ^ SM3_rotl32(W[i-3], 15)
        W[i] = SM3_p1(tmp) ^ SM3_rotl32(W[i-13], 7) ^ W[i-6]


'''
 Function: WToW1
 Description: 从W计算W1
 Calls:
 Called By: SM3_compress
 Input: W[64]
 Output: W1[64]
 Return: null
 Others:
'''
def WToW1(W, W1):
    for i in range(64):
        W1[i] = W[i] ^ W[i+4]



'''
 Function: CF
 Description: CF函数并更新V
 Calls:
 Called By: SM3_compress
 Input: W[64], W1[64], V[8]
 Output: V[8]
 Return: null
 Others:
'''
def CF(W, W1, V):
    T = SM3_T1
    A, B, C, D, E, F, G, H = V[0], V[1], V[2], V[3], V[4], V[5], V[6], V[7]
    # print(hex(A), hex(B), hex(C), hex(D), hex(E), hex(F), hex(G), hex(H))
    for j in range(64):
        # SS1
        if j == 0:
            T = SM3_T1
        elif j == 16:
            T = SM3_rotl32(SM3_T2, 16)
        else:
            T = SM3_rotl32(T, 1)

        SS1 = SM3_rotl32((SM3_rotl32(A, 12) + E + T) & 0xffffffff , 7)
        # print(SS1)
        # SS2
        SS2 = SS1 ^ SM3_rotl32(A, 12)
        
        # TT1
        if j <= 15:
            FF = SM3_ff0(A, B, C)
        else:
            FF = SM3_ff1(A, B, C)
        TT1 = FF + D + SS2 + W1[j]
        # print(hex(FF), hex(D), hex(SS2), hex(W1[j]), hex(TT1))
        
        # TT2
        if j <= 15:
            GG = SM3_gg0(E, F, G)
        else:
            GG = SM3_gg1(E, F, G)
        TT2 = (GG + H + SS1 + W[j]) & 0xffffffff

        # else
        D = C 
        C = SM3_rotl32(B, 9) & 0xffffffff
        B = A
        A = TT1 & 0xffffffff
        H = G
        G = SM3_rotl32(F, 19) & 0xffffffff
        F = E
        E = SM3_p0(TT2) & 0xffffffff
        #print(j, hex(A) ,hex(B) ,hex(C) ,hex(D) ,hex(E) ,hex(F) ,hex(G) ,hex(H))
        #update V
    V[0] = A ^ V[0]
    V[1] = B ^ V[1]
    V[2] = C ^ V[2]
    V[3] = D ^ V[3]
    V[4] = E ^ V[4]
    V[5] = F ^ V[5]
    V[6] = G ^ V[6]
    V[7] = H ^ V[7]


'''
 Function: BigEndian
 Description: GM/T 0004-2012要求使用大端模式，如果你的计算机是小端系统则需要使用该函数
 Calls:
 Called By: SM3_compress, SM3_done
 Input: src[bytelen], bytelen
 Output: des[bytelen]
 Return: null
 Others: src和des可以表示相同的地址 
'''
def BigEndian(src, bytelen, des):
    for i in range(bytelen//4):
        tmp = des[4*i]
        des[4*i] = src[4*i+3]
        src[4*i+3] = tmp

        tmp = des[4*i+1]
        des[4*i+1] = src[4*i+2]
        des[4*i+2] = tmp


'''
 Function: SM3_init
 Description: 初始化SM3缓冲区
 Calls:
 Called By: SM3_256
 Input: md 
 Output: md
 Return: null
 Others: md = SM3_STATE()
'''
def SM3_init(md):
    md.curlen = md.length = 0
    md.state[0] = SM3_IVA
    md.state[1] = SM3_IVB
    md.state[2] = SM3_IVC
    md.state[3] = SM3_IVD
    md.state[4] = SM3_IVE
    md.state[5] = SM3_IVF
    md.state[6] = SM3_IVG
    md.state[7] = SM3_IVH


'''
 Function: SM3_compress
 Description: 压缩单个消息块
 Calls: BigEndian, BiToW, WToW1, CF
 Called By: SM3_256
 Input: md
 Output: md
 Return: null
 Others: md = SM3_STATE()
'''
def SM3_compress(md):
    W = [0] * 68
    W1 = [0] * 64
    # 小端系统
    # BigEndian(md.buf, 64, md.buf)
    # print(md.buf)
    buf = [0] * 16
    for i in range(64):
        buf[i//4] += md.buf[i]
        if i%4 != 3:
            buf[i//4] <<= 8
    # print(buf)
    BiToW(buf, W)
    WToW1(W, W1)
    CF(W, W1, md.state)


'''
 Function: SM3_process
 Description: 压缩消息的第一个len/64块
 Calls: SM3_compress
 Called By: SM3_256
 Input: md, buf[len], len
 Output: SM3_STATE *md
 Return: null
 Others: md = SM3_STATE() 
'''
def SM3_process(md, buf, length):
    i = 0
    while length > 0:
        md.buf[md.curlen] = buf[i]
        i += 1
        md.curlen += 1
        if md.curlen == 64:
            SM3_compress(md)
            md.length += 512
            md.curlen = 0
        length -= 1


'''
 Function: SM3_done
 Description: 压缩剩余消息并产生Hash
 Calls: SM3_compress
 Called By: SM3_256
 Input: md
 Output: unsigned char *hash
 Return: null
 Others: md = SM3_STATE()
'''
def SM3_done(md):
    tmp = 0
    md.length += md.curlen << 3
    md.buf[md.curlen] = 0x80
    md.curlen += 1
    if md.curlen > 56:
        while md.curlen < 64:
            md.buf[md.curlen] = 0
            md.curlen += 1
        SM3_compress(md)
        md.curlen = 0

    while md.curlen < 56:
        md.buf[md.curlen] = 0
        md.curlen += 1

    for i in range(56, 60):
        md.buf[i] = 0

    md.buf[63] = md.length & 0xff
    md.buf[62] = (md.length >> 8) & 0xff
    md.buf[61] = (md.length >> 16) & 0xff
    md.buf[60] = (md.length >> 24) & 0xff

    SM3_compress(md)
    Hash = ""
    for i in md.state:
        length = len(hex(i)[2:])
        state = hex(i)[2:]
        # print(i, state)
        while length < 8:
            state = '0' + state
            length += 1
        Hash = Hash + state
    return Hash    


'''
 Function: SM3_256
 Description: 入口函数
 Calls: SM3_init, SM3_process, SM3_done
 Called By:
 Input: buf
 Output: null
 Return: Hash值
 Others:
'''
def SM3_256(buf):
    md = SM3_STATE()
    SM3_init(md)
    SM3_process(md, buf, len(buf))
    return SM3_done(md)


# SM2使用的kdf函数
def SM3_kdf(z, klen):
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen/32)
    # print(z)
    zin = [i for i in bytes.fromhex(z.decode('utf8'))]
    # print(zin)
    ha = ""
    for i in range(rcnt):
        msg = zin + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        print(msg)
        ha = ha + SM3_256(msg)
        ct += 1
        print(ha)
        print()
    return ha[0: klen * 2]



def test():
    # 输入格式为byte的十六进制
    a = b"abc".hex()
    Msgl = [i for i in bytes.fromhex('%s' % a)]
    print(Msgl, len(Msgl))
    MsgHash = SM3_256(Msgl)
    print(MsgHash, len(MsgHash))


# test()
