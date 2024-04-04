import sys
from db.models import Transaction
from db.database import SessionLocal, add_account, get_all_accounts, transfer_funds, clear_database, get_account_by_address
from wallet.wallet import BitcoinWallet
from wallet.warranty import create_transaction_hash, pseudo_sign_transaction, verify_signature
import random



asci_bitcoin = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣶⣶⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⡿⠿⠛⠛⠛⠛⠛⠛⠻⢿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣼⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣷⣄⠀⠀⠀⠀
⠀⠀⠀⣰⣿⡿⠋⠀⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀⠀⠈⢿⣿⣦⡀⠀⠀
⠀⠀⣸⣿⡿⠀⠀⠀⠸⠿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣶⣄⠀⠀⠀⠀⢹⣿⣷⠀⠀
⠀⢠⣿⡿⠁⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⢹⣿⣧⠀
⠀⣾⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⢀⣠⣿⣿⠟⠀⠀⠀⠀⠀⠈⣿⣿⠀
⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⠿⠿⠿⣿⣿⣥⣄⠀⠀⠀⠀⠀⠀⣿⣿⠀
⠀⢿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣧⠀⠀⠀⠀⢀⣿⣿⠀
⠀⠘⣿⣷⡀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⣼⣿⣿⡿⠀⠀⠀⠀⣸⣿⡟⠀
⠀⠀⢹⣿⣷⡀⠀⠀⢰⣶⣿⣿⣿⣷⣶⣶⣾⣿⣿⠿⠛⠁⠀⠀⠀⣸⣿⡿⠀⠀
⠀⠀⠀⠹⣿⣷⣄⠀⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀⠀⢀⣾⣿⠟⠁⠀⠀
⠀⠀⠀⠀⠘⢻⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣷⣶⣤⣤⣤⣤⣤⣤⣴⣾⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n"""




def print_help():
    print(asci_bitcoin)
    print("""
Available commands:
    help - Show this help message
    database - Show all wallets in the database. Use -all flag to see more
    random - Populate the database with 5 random wallets
    send <from_address> <to_address> <amount> - Send amount from one wallet to another
    clear - clear test_database
    """)
    print("""
          Project schema
          ├── db
          │   ├── database.py
          │   ├── __init__.py
          │   └── models.py
          ├── wallet
          │   ├── __init__.py
          │   ├── wallet.py
          │   └── warranty.py
          └── main.py
          """)

def print_database(all_data=False):
    session = SessionLocal()
    if not all_data:
        # Выводим только информацию о кошельках
        accounts = get_all_accounts(session)
        print(f"{'Address':<42} {'Balance':>10}")
        print("-" * 53)
        for account in accounts:
            print(f"{account.address:<42} {account.balance:>10.8f} BTC")
    else:
        # Выводим информацию из всех таблиц
        print("Accounts:")
        accounts = get_all_accounts(session)
        for account in accounts:
            print(f"Address: {account.address}, Balance: {account.balance} BTC, Private Key: {account.private_key}, Public Key: {account.public_key}", end='\n'+'*'*10+'\n\n', sep='\n')
        print("\nTransactions:")
        transactions = session.query(Transaction).all()
        for transaction in transactions:
            print(f"Sender: {transaction.sender_address}, Recipient: {transaction.recipient_address}, Amount: {transaction.amount} BTC, Hash: {transaction.transaction_hash}, Signature: {transaction.signature}")
    session.close()


def add_random_wallets():
    session = SessionLocal()
    for _ in range(5):
        private_key, public_key = BitcoinWallet.generate_key_pair()
        address = BitcoinWallet.compute_bitcoin_address(public_key)
        balance = random.uniform(0, 2)  # Random balance between 0 and 2 BTC
        add_account(session, address, private_key.to_string().hex(), balance, public_key.to_string().hex())
    session.close()
    print("5 random wallets added to the database.")



def send_funds(from_address, to_address, amount, sender_private_key_hex):
    print(f"Creating transaction from {from_address} to {to_address} for {amount} BTC...")
    transaction_hash = create_transaction_hash(from_address, to_address, amount)
    print(f"Transaction hash: {transaction_hash}")

    print("Signing transaction...")
    signature = pseudo_sign_transaction(transaction_hash, sender_private_key_hex)
    print(f"Transaction signature: {signature}")

    session = SessionLocal()
    account = get_account_by_address(from_address)
    if account is None:
        print("Sender account not found.")
        return

    public_key_hex = account.public_key

    if verify_signature(public_key_hex=public_key_hex, signature_hex=signature, message=transaction_hash):
        print("Signature verified successfully.")
        if transfer_funds(from_address, to_address, amount):
            print(f"Successfully transferred {amount} BTC from {from_address} to {to_address}.")
        else:
            print("Transaction failed. Possibly due to insufficient funds.")
    else:
        print("Failed to verify signature. Transaction rejected.")

    session.close()






def clear_database_command():
    session = SessionLocal()
    clear_database(session)
    session.close()




def main():
    print(asci_bitcoin)
    print("""Welcome to the Bitcoin Wallet Simulator. Type 'help' for a list of commands.
Press Ctrl+C to exit.""")
    while True:
        try:
            command = input(">").strip().split()
            if not command:
                continue
            if command[0] == "database":
                all_data = len(command) > 1 and command[1] == "-all"
                print_database(all_data)
            elif command[0] == "help":
                print_help()
            elif command[0] == "random":
                add_random_wallets()
            elif command[0] == "send" and len(command) == 5:
                _, from_address, to_address, amount, sender_private_key_hex = command
                send_funds(from_address, to_address, float(amount), sender_private_key_hex)
            elif command[0] == "clear":
                clear_database_command()
            elif command[0] == "exit":
                print("Goodbye!")
                break
            else:
                print("Invalid command. Type 'help' for a list of commands.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

