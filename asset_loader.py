from web3 import Web3
import json
infura_url = "https://linea-sepolia.infura.io/v3/b9e8f0cbb0d74cf6b87a0c7642f3fb1e"

web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.is_connected())
abi = open("abi.json", "r")
abi_ = json.load(abi)
address = '0x155E31b21C0E0261dB0d7a5E27e95f945e784d72'
contract = web3.eth.contract(address=address, abi=abi_)
call2 = contract.all_functions


def auth(_address, _password):
    call = contract.functions.getCred(_address).call()
    passwrd_hash = web3.keccak(text=_password)
    password_hash = str(web3.to_hex(passwrd_hash))
    password_hash = password_hash[2:]
    if call == password_hash:
        return True
    else:
        return False


def load_weapons(user):
    call = contract.functions.getUserWeapons(user).call()
    return call



