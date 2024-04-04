# database.py
from sqlalchemy.orm import Session
from .__init__ import init_db
from .models import Account, Transaction

SessionLocal = init_db()

def add_account(session, address, private_key, balance, public_key):
    new_account = Account(address=address, private_key=private_key, balance=balance, public_key=public_key)
    session.add(new_account)
    session.commit()


def get_account_by_address(address):
    with SessionLocal() as session:
        account = session.query(Account).filter(Account.address == address).first()
        return account

def update_balance(address, new_balance):
    with SessionLocal() as session:
        account = session.query(Account).filter(Account.address == address).first()
        if account:
            account.balance = new_balance
            session.commit()
            return account
        else:
            return None

def delete_account(address):
    with SessionLocal() as session:
        account = session.query(Account).filter(Account.address == address).first()
        if account:
            session.delete(account)
            session.commit()
            return True


def add_transaction(sender_address, recipient_address, amount, transaction_hash, signature):
    with SessionLocal() as session:
        new_transaction = Transaction(sender_address=sender_address, recipient_address=recipient_address,
                                      amount=amount, transaction_hash=transaction_hash, signature=signature)
        session.add(new_transaction)
        session.commit()
        return new_transaction

def get_transaction_by_hash(transaction_hash):
    with SessionLocal() as session:
        transaction = session.query(Transaction).filter(Transaction.transaction_hash == transaction_hash).first()
        return transaction
    

def transfer_funds(sender_address, recipient_address, amount):
    with SessionLocal() as session:
        sender_account = session.query(Account).filter(Account.address == sender_address).first()
        recipient_account = session.query(Account).filter(Account.address == recipient_address).first()
        if sender_account and recipient_account and sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            session.commit()
            return True
        else:
            return False


def pseudo_sign_transaction(transaction_hash, sender_address):
    with SessionLocal() as session:
        # Получаем аккаунт отправителя из базы данных по его адресу
        sender_account = session.query(Account).filter(Account.address == sender_address).first()
        if sender_account:
            # Используем приватный ключ отправителя для имитации подписи
            signature = f"signed_{transaction_hash}_with_{sender_account.private_key}"
            return signature
        else:
            return None


def get_all_accounts(session):
    """Получение списка всех аккаунтов из базы данных."""
    return session.query(Account).all()


def clear_database(session):
    """Очистка всех таблиц базы данных."""
    try:
        session.query(Account).delete()
        session.query(Transaction).delete()
        session.commit()
        print("Database cleared successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error clearing database: {e}")
