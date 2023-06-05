from solcx import compile_standard
import json
from web3 import Web3
#from solcx import install_solc
#install_solc("0.6.0")

#Read solidity file
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)
    
# Compile our solidty    
compiled_sol = compile_standard(
    {
    "language": "Solidity",
    "sources":{"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*"  : {
                "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
            }
        }
    },
    },
    solc_version="0.6.0",

)
#print(compiled_sol)
#Compile to json
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file) 
    
# get bytecode //convert in python
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
chain_id = 5777
my_address = "0x0f7D2779B436Fd5CB1489ed207944560E98882C7"
priave_key = "0xb76f6e987c1d64c858e694f72b2127a0f06055af4b7baf283c42a06fad3a928f"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)
 
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print(nonce) 

# 1. Build transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().build_transaction({"chainid":chain_id, "from":my_address, "nonce":nonce})
print(transaction)