import logging
from web3 import Web3
from config_kiloex import BASE

with open('./abi/Usdt.abi', 'r') as f:
    usdt_abi = f.read()

def approve_usdt_allowance(config, to_address, amount):
    """Approve USDT allowance for trading"""
    try:
        w3 = Web3(Web3.HTTPProvider(config.rpc))
        account = w3.eth.account.from_key(config.private_key)
        
        # Convert addresses to checksum format
        wallet_address = Web3.to_checksum_address(config.wallet)
        to_address = Web3.to_checksum_address(to_address)
        usdt_address = Web3.to_checksum_address(config.usdt_contract)
        
        contract = w3.eth.contract(address=usdt_address, abi=usdt_abi)
        
        allowance = contract.functions.allowance(wallet_address, to_address).call()
        base_decimals = 10 ** contract.functions.decimals().call()
        allowance = allowance / base_decimals
        
        amount = amount + 50000  # Add buffer
        if allowance < amount:
            logging.info(f'Approving USDT allowance: {amount}')
            
            gas_price = w3.eth.gas_price
            data = contract.functions.approve(
                to_address,
                int(amount * base_decimals)
            ).build_transaction({
                'from': wallet_address,
                'nonce': w3.eth.get_transaction_count(wallet_address),
                'gas': config.gas,
                'gasPrice': gas_price
            })

            signed_txn = account.sign_transaction(data)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return tx_receipt['status'] == 1
            
        logging.info(f'USDT allowance sufficient: {allowance}')
        return True
        
    except Exception as e:
        logging.error(f'USDT approval error: {str(e)}')
        raise

def get_balance(config):
    """Get USDT balance"""
    w3 = Web3(Web3.HTTPProvider(config.rpc))
    
    # Convert addresses to checksum format
    wallet_address = Web3.to_checksum_address(config.wallet)
    usdt_address = Web3.to_checksum_address(config.usdt_contract)
    
    contract = w3.eth.contract(address=usdt_address, abi=usdt_abi)
    balance = contract.functions.balanceOf(wallet_address).call()
    base_decimals = 10 ** contract.functions.decimals().call()
    return balance / base_decimals