# version0.1版本思路

### 区块相关:

1.定义一个区块的结构BLock

​		a.区块头:6个字段

​		b.区块体:字符串表示data

2.提供一个创建区块的方法

​		NewBlock(参数)

区块链相关:

1.定义一个区块链结构BLockChain

​		Block数组

2.提供一个创建BlockChain的方法

​		NewBlockChain()

3.提供一个添加区块的方法

​		AddBlock(参数）