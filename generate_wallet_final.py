# Gabungan dari generate_wallets.py, generate_wallets_with_passphrase.py, dan slip39

import os
from eth_account import Account
from mnemonic import Mnemonic

# Enable HD wallet features
Account.enable_unaudited_hdwallet_features()

def generate_wallets(num_wallets, words_count, passphrase=None):
    mnemo = Mnemonic("english")
    strength_mapping = {
        12: 128,
        15: 160,
        18: 192,
        21: 224,
        24: 256
    }

    if words_count not in strength_mapping:
        raise ValueError("Allowed values for words_count are [12, 15, 18, 21, 24]")

    wallets_info = []

    for _ in range(num_wallets):
        # Generate seed phrase
        seed_phrase = mnemo.generate(strength=strength_mapping[words_count])
        
        # Derive private key and Ethereum address based on the mode (with/without passphrase)
        if passphrase:
            private_key = Account.from_mnemonic(seed_phrase, passphrase).key.hex()
            address = Account.from_mnemonic(seed_phrase, passphrase).address
        else:
            private_key = Account.from_mnemonic(seed_phrase).key.hex()
            address = Account.from_mnemonic(seed_phrase).address

        wallets_info.append({
            'seed_phrase': seed_phrase,
            'private_key': private_key,
            'address': address
        })

    return wallets_info

# Main menu for user input
print("Select wallet generation mode:")
print("1. Standard (no passphrase)")
print("2. With Passphrase")
mode = int(input("Enter mode (1 or 2): "))

num_wallets = int(input("Enter the number of wallets to generate: "))
words_count = int(input("Choose the number of words in seed phrase (12, 15, 18, 21, 24): "))
output_file = input("Enter the desired output filename (e.g., sixgpt.txt): ")

if mode == 1:
    wallets_info = generate_wallets(num_wallets, words_count)
elif mode == 2:
    passphrase = input("Enter a passphrase for added security: ")
    wallets_info = generate_wallets(num_wallets, words_count, passphrase)
else:
    raise ValueError("Invalid mode selected.")

# Write to the user-defined output file
with open(output_file, 'w') as of:
    for info in wallets_info:
        of.write(f"Seed Phrase: {info['seed_phrase']}\n")
        of.write(f"Address: {info['address']}\n")
        of.write(f"Private Key: {info['private_key']}\n")
        of.write("\n")

print(f"Wallets generated and saved to {output_file}.")
