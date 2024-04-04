# wallet.py
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import RIPEMD160
import hashlib
import base58

from db.database import add_account, update_balance, get_account_by_address,transfer_funds, add_transaction, pseudo_sign_transaction
from .warranty import create_transaction_hash

class BitcoinWallet:
    @staticmethod
    def generate_key_pair():
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.verifying_key
        return private_key, public_key

    @staticmethod
    def compute_bitcoin_address(public_key):
        pub_key_bytes = public_key.to_string("compressed")
        sha256_bpk = hashlib.sha256(pub_key_bytes).digest()
        
        # Использование RIPEMD-160 из pycryptodome
        ripemd160 = RIPEMD160.new()
        ripemd160.update(sha256_bpk)
        ripemd160_bpk = ripemd160.digest()
        
        version = b'\x00' + ripemd160_bpk
        checksum = hashlib.sha256(hashlib.sha256(version).digest()).digest()[:4]
        binary_address = version + checksum
        bitcoin_address = base58.b58encode(binary_address)
        return bitcoin_address.decode()
    
    

class Utils:
    @staticmethod
    def process_transaction(sender_address, recipient_address, amount):
        transaction_hash = create_transaction_hash(sender_address, recipient_address, amount)
        signature = pseudo_sign_transaction(transaction_hash, sender_address)
        if signature and transfer_funds(sender_address, recipient_address, amount):
            # Транзакция успешна, добавляем информацию о ней в базу данных
            add_transaction(sender_address, recipient_address, amount, transaction_hash, signature)
            print(f"Transaction processed and added to database: {transaction_hash}")
        else:
            print("Transaction failed: insufficient funds, invalid account, or signature failure.")



    @staticmethod
    def blockchain():
        """
        Возвращает текущее состояние блокчейна.
        """

        pass


if __name__ == "__main__":
    test_private_key, test_public_key = BitcoinWallet.generate_key_pair()
    address = BitcoinWallet.compute_bitcoin_address(test_public_key)
    print(address)