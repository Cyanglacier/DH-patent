import hashlib
import ecdsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class exchange_module:
    def __init__(self, storage_module):
        self.storage = storage_module

    def generate_commitment(self, other_public_key, data_head):
        # 使用自己的私钥和对方的公钥生成共享密钥
        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(self.storage.get_private_key()), curve=ecdsa.SECP256k1)
        other_public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(other_public_key), curve=ecdsa.SECP256k1)
        shared_key = private_key.privkey.secret_multiplier * other_public_key.pubkey.point

        # 使用共享密钥和数据头生成承诺
        commitment = hashlib.sha256(str(shared_key).encode() + data_head.encode()).hexdigest()
        return commitment

    def calculate_session_key(self, commitment_a, commitment_b):
        # 计算会话密钥
        session_key = hashlib.sha256((commitment_a + commitment_b).encode()).digest()
        self.storage.store_session_key(session_key.hex())
        return session_key

    def encrypt_data(self, data):
        session_key = bytes.fromhex(self.storage.get_session_key())
        cipher = AES.new(session_key, AES.MODE_ECB)
        encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
        return encrypted_data.hex()

    def decrypt_data(self, encrypted_data):
        session_key = bytes.fromhex(self.storage.get_session_key())
        cipher = AES.new(session_key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(bytes.fromhex(encrypted_data)), AES.block_size)
        return decrypted_data.decode()

    def send_data(self, receiver_public_key, data):
        # 生成承诺A
        commitment_a = self.generate_commitment(receiver_public_key, "SEND")
        
        # 这里应该有一个网络通信的过程，发送承诺A给接收方
        # 接收方生成承诺B并发送回来
        # 为了演示，我们假设已经收到了承诺B
        commitment_b = "假设这是从接收方收到的承诺B"

        # 计算会话密钥
        self.calculate_session_key(commitment_a, commitment_b)

        # 加密数据
        encrypted_data = self.encrypt_data(data)

        # 发送加密数据（这里应该是网络通信过程）
        return encrypted_data

    def receive_data(self, sender_public_key, encrypted_data):
        # 生成承诺B
        commitment_b = self.generate_commitment(sender_public_key, "RECEIVE")
        
        # 这里应该有一个网络通信的过程，发送承诺B给发送方
        # 发送方应该已经发送了承诺A
        # 为了演示，我们假设已经收到了承诺A
        commitment_a = "假设这是从发送方收到的承诺A"

        # 计算会话密钥
        self.calculate_session_key(commitment_a, commitment_b)

        # 解密数据
        decrypted_data = self.decrypt_data(encrypted_data)

        return decrypted_data
