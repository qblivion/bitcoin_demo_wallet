import hashlib
from hashlib import sha256
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError, SigningKey
from ecdsa import VerifyingKey, BadSignatureError

def verify_signature(public_key_hex, signature_hex, message):
    public_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
    signature = bytes.fromhex(signature_hex)
    try:
        public_key.verify(signature, message.encode())
        return True
    except BadSignatureError:
        return False



def process_transaction(sender_address, recipient_address, amount, sender_private_key_hex, sender_public_key_hex):
    # Сгенерировать хеш транзакции
    transaction_hash = hashlib.sha256(f"{sender_address}{recipient_address}{amount}".encode()).hexdigest()
    
    # Симулируем подписание транзакции закрытым ключом
    signature = pseudo_sign_transaction(transaction_hash, sender_private_key_hex)
    
    # Проверяем подпись транзакции
    if verify_signature(sender_public_key_hex, signature, transaction_hash):
        print("Подпись верна. Транзакция успешно проверена.")
    else:
        print("Неверная подпись. Транзакция отклонена.")

def create_transaction_hash(sender_address, recipient_address, amount):
    transaction_string = f"{sender_address}{recipient_address}{amount}"
    return sha256(transaction_string.encode()).hexdigest()


def pseudo_sign_transaction(transaction_hash, private_key_hex):
    """Подпись транзакции с использованием приватного ключа и ECDSA."""
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    signature = private_key.sign(transaction_hash.encode())
    return signature.hex()

