import hashlib
import ecdsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

from .exchange_module import exchange_module
from .storage_module import storage_module

# 定义一些可能在整个包中使用的全局变量或配置
DEFAULT_CURVE = ecdsa.SECP256k1
DEFAULT_ENCODING = 'utf-8'

# 初始化全局的存储模块和交换模块实例
global_storage = storage_module()
global_exchange = exchange_module(global_storage)

# 如果有其他需要在包被导入时执行的初始化代码，可以放在这里
