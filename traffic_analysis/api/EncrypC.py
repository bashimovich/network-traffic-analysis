import hashlib
import shutil
import os
import sys
from pathlib import Path
from Cryptodome.Cipher import AES
from datetime import datetime

class EncryptionTool:
    def __init__(self, user_file, _dir, user_key):
        self.user_file = user_file
        self.input_file_size = os.path.getsize(self.user_file)
        self.chunk_size = 1024
        self.total_chunks = self.input_file_size // self.chunk_size + 1
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")
        self.file_extension = self.user_file.split(".")[-1]
        self.hash_type = "SHA256"
        self.enc_media_file = f'{_dir}/' + self.user_file.split('/')[2]+'.encr'
        self.dec_media_file = (f'{_dir}/' + self.user_file.split('/')[2])[:-5]
        self.encrypt_output_file = f'./static/'+ self.enc_media_file
        self.decrypt_output_file = self.user_file[:-5].split(".")
        self.decrypt_output_file = f'./static/' + self.dec_media_file
        self.hashed_key_salt = dict()
        self.hash_key_salt()

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def encrypt(self):
        cipher_object = AES.new(
            self.hashed_key_salt["key"], AES.MODE_CFB, self.hashed_key_salt["salt"]
        )
        self.abort()  # if the output file already exists, remove it first
        input_file = open(self.user_file, "rb")
        output_file = open(self.encrypt_output_file, "ab")
        # done_chunks = 0
        # os.remove(self.user_file)
        for piece in self.read_in_chunks(input_file, self.chunk_size):
            encrypted_content = cipher_object.encrypt(piece)
            output_file.write(encrypted_content)
            # done_chunks += 1
        #     yield done_chunks / self.total_chunks * 100
        input_file.close()
        output_file.close()
        del cipher_object
        return self.enc_media_file 

    def decrypt(self):
        cipher_object = AES.new(
            self.hashed_key_salt["key"], AES.MODE_CFB, self.hashed_key_salt["salt"]
        )
        self.abort()  # if the output file already exists, remove it first
        input_file = open(self.user_file, "rb")
        output_file = open(self.decrypt_output_file, "xb")
        # done_chunks = 0
        for piece in self.read_in_chunks(input_file):
            decrypted_content = cipher_object.decrypt(piece)
            output_file.write(decrypted_content)
            # done_chunks += 1
            # yield done_chunks / self.total_chunks * 100
        input_file.close()
        output_file.close()
        del cipher_object
        return self.dec_media_file 

    def abort(self):
        if os.path.isfile(self.encrypt_output_file):
            os.remove(self.encrypt_output_file)
        if os.path.isfile(self.decrypt_output_file):
            os.remove(self.decrypt_output_file)

    def hash_key_salt(self):
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)
        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")
        del hasher
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)
        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")
        del hasher

