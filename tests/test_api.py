import free_solscan_api
import pytest
import os
import json

def pretty_print_json(json_data):
    print(json.dumps(json_data, indent=4))

def print_if_verbose(msg):
    if os.environ.get("TEST_VERBOSE", False):
        pretty_print_json(msg)

router = free_solscan_api.Router(free_solscan_api.solscan_endpoints)


def test_generate_solauth_token():
    token = free_solscan_api.generate_solauth_token()
    assert len(token) == 40
    assert "B9dls0fK" in token


def test_transaction():
    tx = "57YB5kSKyBqFqLtmnzJKn3ZJuGsaMKDuJaKoZKHZJqU3fTRyoL3b2uMq7K9BNjWvJgDMhrs1npG4PbNzWguNSV1b"
    tx_response = router.transaction(tx)
    print_if_verbose(tx_response)
    assert tx_response["trans_id"] == tx


def test_transactions():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    transactions_response = router.transactions(address)
    print_if_verbose(transactions_response)
    assert transactions_response != ({} or [] or [{}])


def test_defi_activities():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    defi_activities_response = router.defi_activities(address)
    print_if_verbose(defi_activities_response)
    assert defi_activities_response != ({} or [] or [{}])


def test_token_holders():
    address = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
    token_holders_response = router.token_holders(address)
    print_if_verbose(token_holders_response)
    assert token_holders_response != ({} or [] or [{}])


def test_transfers():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    transfers_response = router.transfers(address)
    print_if_verbose(transfers_response)
    assert transfers_response != ({} or [] or [{}])


def test_token_holders_total():
    address = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
    token_holders_total_response = router.token_holders_total(address)
    print_if_verbose(token_holders_total_response)
    assert token_holders_total_response != ({} or [] or [{}])


def test_account_info():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    account_info_response = router.account_info(address)
    print_if_verbose(account_info_response)
    assert account_info_response != ({} or [] or [{}])


def test_portofolio():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    portofolio_response = router.portofolio(address)
    print_if_verbose(portofolio_response)
    assert portofolio_response != ({} or [] or [{}])


def test_balance_history():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    balance_history_response = router.balance_history(address)
    print_if_verbose(balance_history_response)
    assert balance_history_response != ({} or [] or [{}])


def test_top_address_transfers():
    address = "4g9dwu6iVKnX91zRF3QTE7avjQoxbj15GZ7rHeo1SyWS"
    top_address_transfers_response = router.top_address_transfers(address)
    print_if_verbose(top_address_transfers_response)
    assert top_address_transfers_response != ({} or [] or [{}])


def test_token_data():
    token_address = "So11111111111111111111111111111111111111112"
    token_data_response = router.token_data(token_address)
    print_if_verbose(token_data_response)
    assert token_data_response != ({} or [] or [{}])
