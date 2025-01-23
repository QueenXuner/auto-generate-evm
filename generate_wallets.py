import os
from eth_account import Account
from mnemonic import Mnemonic

# Enable HD wallet features
Account.enable_unaudited_hdwallet_features()

def generate_wallets(num_wallets, words_count):
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
        private_key = Account.from_mnemonic(seed_phrase).key.hex()  # Derive private key
        address = Account.from_mnemonic(seed_phrase).address  # Derive the Ethereum address

        wallets_info.append({
            'seed_phrase': seed_phrase,
            'private_key': private_key,
            'address': address
        })
    
    return wallets_info

# Input user
num_wallets = int(input("Enter the number of wallets to generate: "))
words_count = int(input("Choose the number of words in seed phrase (12, 15, 18, 21, 24): "))

# Generate wallets
wallets_info = generate_wallets(num_wallets, words_count)

# Define output file names
seed_file = f"seed{words_count}.txt"
address_file = f"address{words_count}.txt"
private_key_file = f"privatekey{words_count}.txt"
wallets_file = f"wallets{words_count}.txt"

# Write output to files
with open(seed_file, 'w') as sf, open(address_file, 'w') as af, open(private_key_file, 'w') as pkf, open(wallets_file, 'w') as wf:
    for info in wallets_info:
        sf.write(info['seed_phrase'] + '\n')
        af.write(info['address'] + '\n')
        pkf.write(info['private_key'] + '\n')
        wf.write(f"{info['seed_phrase']} | {info['address']} | {info['private_key']}\n")

print(f"Wallets generated and saved to {seed_file}, {address_file}, {private_key_file}, and {wallets_file}.")
