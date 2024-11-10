import logging
from web3 import Web3
from config_kiloex import BASE, BASE12, kiloconfigs
import time
import usdt_kiloex
import api_kiloex

with open('./abi/PositionRouter.abi', 'r') as f:
    abi = f.read()

def open_market_increase_position(config, product_id, margin, leverage, is_long, acceptable_price, referral_code):
    """
    Open a market increase position.
    """
    try:
        # Automatically authorize USDT limit
        usdt_kiloex.approve_usdt_allowance(config, config.market_contract, margin)

        w3 = Web3(Web3.HTTPProvider(config.rpc))
        
        # Convert addresses to checksum format
        wallet_address = Web3.to_checksum_address(config.wallet)
        market_address = Web3.to_checksum_address(config.market_contract)
        
        nonce = w3.eth.get_transaction_count(wallet_address)
        gas_price = w3.eth.gas_price
        execution_fee = config.execution_fee

        tx = {
            'from': wallet_address,
            'nonce': nonce,
            'gas': config.gas,
            'gasPrice': gas_price,
            'value': execution_fee,
            'chainId': config.chain_id
        }

        trade_contract_w3 = w3.eth.contract(address=market_address, abi=abi)
        txn = trade_contract_w3.functions.createIncreasePosition(
            product_id, 
            int(margin * BASE), 
            int(leverage * BASE), 
            is_long, 
            int(acceptable_price * BASE),
            execution_fee, 
            referral_code
        ).build_transaction(tx)

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=config.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        logging.info(f"Market increase position tx_hash: {tx_hash.hex()}")
        return tx_hash

    except Exception as e:
        logging.error(f'Market increase position error: {str(e)}')
        raise

def open_market_decrease_position(config, product_id, margin, is_long, acceptable_price):
    """
    Open a market decrease position.
    """
    try:
        w3 = Web3(Web3.HTTPProvider(config.rpc))
        
        # Convert addresses to checksum format
        wallet_address = Web3.to_checksum_address(config.wallet)
        market_address = Web3.to_checksum_address(config.market_contract)
        
        nonce = w3.eth.get_transaction_count(wallet_address)
        gas_price = w3.eth.gas_price
        execution_fee = config.execution_fee

        tx = {
            'from': wallet_address,
            'nonce': nonce,
            'gas': config.gas,
            'gasPrice': gas_price,
            'value': execution_fee,
            'chainId': config.chain_id
        }

        trade_contract_w3 = w3.eth.contract(address=market_address, abi=abi)
        txn = trade_contract_w3.functions.createDecreasePosition(
            product_id,
            int(margin * BASE),
            is_long,
            int(acceptable_price * BASE),
            execution_fee
        ).build_transaction(tx)

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=config.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        logging.info(f"Market decrease position tx_hash: {tx_hash.hex()}")
        return tx_hash

    except Exception as e:
        logging.error(f'Market decrease position error: {str(e)}')
        raise