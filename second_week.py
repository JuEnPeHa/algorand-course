import json

from algosdk import account, constants, encoding, mnemonic, transaction
from algosdk.error import AlgodHTTPError
# from algosdk.future import transaction
from algosdk.v2client import algod

# Connect to an algod node
algod_address = "http://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

initial_faucet_account = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"

algo_testnet_funding = "https://dispenser.testnet.aws.algodev.network?account="

def generate_account():
    # Generate an account
    private_key, address = account.generate_account()
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    return private_key, address, mnemonic_phrase

def opt_in_usdc(phrase, address, private_key):
    # Opt in to asset
    bool_need_to_opt_in = True
    account_info = algod_client.account_info(address)
    for a in account_info["assets"]:
        print("Asset ID: {}".format(a))
        if a['asset-id'] == 10458941:
            bool_need_to_opt_in = False
    if bool_need_to_opt_in:
        print("Need to opt in!")
        params = algod_client.suggested_params()
        note = "Opting in!".encode()
        unsigned_txn = transaction.AssetOptInTxn(
            address,params,10458941,note=note,
        )
        signed_txn = unsigned_txn.sign(private_key)
        txid = algod_client.send_transaction(signed_txn)
        print("Transaction ID: {}".format(txid))

        try:
            txinfo = algod_client.pending_transaction_info(txid)
            print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
        except AlgodHTTPError as e:
            print(e)
    else:
        print("No need to opt in!")

    print("Please go to the following URL to fund your account with USDC: {}".format(algo_testnet_funding + address))
    input("Press a key to continue...")
    print("Account funded!")

    account_info = algod_client.account_info(address)
    for a in account_info["assets"]:
        print("Asset ID: {}".format(a))
        
    # print("Account balance: {}".format(account_info["amount"]))
    # params = algod_client.suggested_params()
    # note = "Opting in!".encode()
    # unsigned_txn = transaction.AssetTransferTxn(
    #     sender=address,
    #     sp=params,
    #     receiver=address,
    #     amt=0,
    #     index=10458941,
    #     note=note,
    # )
    # # signed_txn = unsigned_txn.sign(mnemonic.to_private_key(mnemonic_phrase))
    # signed_txn = unsigned_txn.sign(private_key)
    # txid = algod_client.send_transaction(signed_txn)
    # print("Transaction ID: {}".format(txid))

    # try:
    #     txinfo = algod_client.pending_transaction_info(txid)
    #     print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
    # except AlgodHTTPError as e:
    #     print(e)

def funding_account(address):
    # Fund the account
    print("Please go to the following URL to fund your account: {}".format(algo_testnet_funding + address))
    input("Press a key to continue...")
    print("Account funded!")
    
def first_transaction(phrase, address, private_key):
    account_info = algod_client.account_info(address)
    print("Account balance: {}".format(account_info["amount"]))
    params = personalized_params()
    receiver = initial_faucet_account
    amount = 100000
    note = "Hola mundo!".encode()
    unsigned_txn = transaction.PaymentTxn(address, params, receiver, amount, note=note)
    # signed_txn = unsigned_txn.sign(mnemonic.to_private_key(mnemonic_phrase))
    signed_txn = unsigned_txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID: {}".format(txid))

    try:
        txinfo = algod_client.pending_transaction_info(txid)
        print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
    except AlgodHTTPError as e:
        print(e)

def mint_asset( phrase, address, private_key):
    # Mint asset
    account_info = algod_client.account_info(address)
    print("Account balance: {}".format(account_info["amount"]))
    params = algod_client.suggested_params()
    note = "Minteando!".encode()
    total = 1000
    decimals = 0
    default_frozen = False
    unit_name = "JEPH"
    asset_name = "JEPHCoin"
    url = "https://jeph.technology"
    manager = address
    reserve = address
    freeze = address
    clawback = address
    unsigned_txn = transaction.AssetConfigTxn(
        sender=address,
        sp=params,
        total=total,
        decimals=decimals,
        default_frozen=default_frozen,
        manager=manager,
        reserve=reserve,
        freeze=freeze,
        clawback=clawback,
        unit_name=unit_name,
        asset_name=asset_name,
        url=url,
        note=note,
    )
    # signed_txn = unsigned_txn.sign(mnemonic.to_private_key(mnemonic_phrase))
    signed_txn = unsigned_txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID: {}".format(txid))

    try:
        txinfo = algod_client.pending_transaction_info(txid)
        print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
        txinfo_confirmed = transaction.wait_for_confirmation(algod_client, txid, 4)
        print("Transaction information: {}".format(json.dumps(txinfo_confirmed, indent=4)))
    except AlgodHTTPError as e:
        print(e)

def return_algos_to_faucet( phrase, address, private_key):
    # Return algos to faucet
    account_info = algod_client.account_info(address)
    print("Account balance: {}".format(account_info["amount"]))
    params = personalized_params()
    receiver = initial_faucet_account
    amount = account_info["amount"] - (100000 * 3) * 2
    note = "Returning unused Algos, Thank You!".encode()
    unsigned_txn = transaction.PaymentTxn(address, params, receiver, amount, note=note)
    signed_txn = unsigned_txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID: {}".format(txid))

    try:
        txinfo = algod_client.pending_transaction_info(txid)
        print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
    except AlgodHTTPError as e:
        print(e)

def return_usdc_to_faucet_if_exists( phrase, address, private_key):
    bool_has_usdc = False
    amount_to_return = 0
    account_info = algod_client.account_info(address)
    for a in account_info["assets"]:
        print("Asset ID: {}".format(a))
        # {'amount': 100000000, 'asset-id': 10458941, 'is-frozen': False}
        if a['asset-id'] == 10458941:
            bool_has_usdc = True
            amount_to_return = a['amount']
    
    if bool_has_usdc:
        print("Returning USDC to faucet...")
        params = personalized_params()
        receiver = initial_faucet_account
        amount = amount_to_return
        note = "Returning unused USDC, Thank You!".encode()
        unsigned_txn = transaction.AssetTransferTxn(address, params, receiver, amount, 10458941, note=note)
        signed_txn = unsigned_txn.sign(private_key)
        txid = algod_client.send_transaction(signed_txn)
        print("Transaction ID: {}".format(txid))

        try:
            txinfo = algod_client.pending_transaction_info(txid)
            print("Transaction information: {}".format(json.dumps(txinfo, indent=4)))
        except AlgodHTTPError as e:
            print(e)





def personalized_params():
    # Personalized params
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = constants.MIN_TXN_FEE
    return params




print("Generating account...")
private_key, address, mnemonic_phrase = generate_account()
print("Account generated! Address: {}".format(address))
print("Key: {}".format(private_key))
print("Mnemonic phrase: {}".format(mnemonic_phrase))


print("Funding account...")
funding_account(address)

print("Opting in to USDC...")
opt_in_usdc(mnemonic_phrase, address, private_key)

print("Sending first transaction...")
first_transaction(mnemonic_phrase, address, private_key)

print("Minting asset...")
mint_asset(mnemonic_phrase, address, private_key)

print("Returning USDC to faucet if exists...")
return_usdc_to_faucet_if_exists(mnemonic_phrase, address, private_key)

print("Returning algos to faucet...")
return_algos_to_faucet(mnemonic_phrase, address, private_key)