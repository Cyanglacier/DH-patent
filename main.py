# 基于DH密钥交换，实现两个客户端之间的数据传输，并且第三方即使截获数据也无法解密
# 1 储存模块 = 储存公钥，私钥，对话密钥，数据
# 2 交换模块 = 达成沟通，实现密钥交换，并发送数据

'''
伪代码

# 储存模块：
# 基于speck256k1曲线，输入任意数值，hash后生成私钥，并储存公钥
# 生成的公私钥对保存在本地
# 从外部引入csv作为模拟数据

Class 储存模块

    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.session_key = None
        self.data = None

    def store_public_key(self, public_key):
        self.public_key = public_key

    def store_private_key(self, private_key):
        self.private_key = private_key

    def store_session_key(self, session_key):
        self.session_key = session_key

    def store_data(self, data):
        self.data = data

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_session_key(self):
        return self.session_key

    def get_data(self):
        return self.data

# 交换模块：
# 定位发送角色，此处采用P2P通讯
# 请求获得对方的公钥
# 根据对方的公钥，和自己的私钥，以及希望传输数据的“HEAD”，生成承诺A
# 将承诺发送给对方
# 对方接收承诺，根据发送方的公钥，和自己的私钥，以及希望接受数据的“HEAD”，生成承诺B
# 承诺A - 承诺B = 对话密钥
# 交换承诺
# 发送方根据对话密钥将数据加密，发送给接收方。
# 接收方根据本地计算的对话密钥，解密数据

'''


import hashlib
import ecdsa
import csv

class 储存模块:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.session_key = None
        self.data = None

    def generate_key_pair(self, input_value):
        # 使用输入值生成私钥
        hash_object = hashlib.sha256(input_value.encode())
        private_key_bytes = hash_object.digest()
        
        # 基于secp256k1曲线生成私钥和公钥
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        self.private_key = sk.to_string().hex()
        self.public_key = vk.to_string().hex()

    def store_public_key(self, public_key):
        self.public_key = public_key

    def store_private_key(self, private_key):
        self.private_key = private_key

    def store_session_key(self, session_key):
        self.session_key = session_key

    def store_data(self, data):
        self.data = data

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_session_key(self):
        return self.session_key

    def get_data(self):
        return self.data

    def load_data_from_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)

    def save_keys_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"Public Key: {self.public_key}\n")
            file.write(f"Private Key: {self.private_key}\n")

    def load_keys_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.public_key = lines[0].split(': ')[1].strip()
            self.private_key = lines[1].split(': ')[1].strip()
