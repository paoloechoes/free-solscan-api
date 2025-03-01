import requests
from .solauth import generate_solauth_token
import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logger = logging.getLogger(__name__)
logging.basicConfig(level=LOG_LEVEL)


def send_api_request(url, headers=None, url_params=None) -> dict:
    """
    Send a request to the Solscan API and return the response.
    """
    base_url = "https://api-v2.solscan.io/v2"
    default_headers = {
        "Accept": "application/json, text/plain, */*",
        "sol-aut": generate_solauth_token(),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": "https://solscan.io/",
        "Origin": "https://solscan.io",
        "Connection": "keep-alive",
    }

    if headers:
        default_headers.update(headers)

    # log url-encoded full request
    logging.debug(f"Sending request to {base_url + url} with params: {url_params}")

    response = requests.get(base_url + url, headers=default_headers, params=url_params)
    result = response.json()

    # check if "data" key is in the response
    if result.get("data", None) == None:
        raise Exception(f"Failed to get data from {url}")

    return result["data"]


class EndpointRouter:
    def __init__(self, endpoints):
        self._endpoints = {
            func_name: handler for func_name, handler in endpoints.items()
        }

    def __getattr__(self, name):
        """
        Handle dot notation calling scheme -> dict.func_name(*args, **kwargs)
        """
        return self._endpoints[name]


endpoints = {
    "transaction": lambda tx: send_api_request(
        f"/transaction/detail/", url_params={"tx": tx}
    ),
    "transactions": lambda address, page=1, page_size=40: send_api_request(
        f"/account/transaction",
        url_params={"address": address, "page": page, "page_size": page_size},
    ),
    "defi_activities": lambda address, page=1, page_size=100: send_api_request(
        f"/account/activity/dextrading",
        url_params={"address": address, "page": page, "page_size": page_size},
    ),
    "token_holders": lambda address, page=1, page_size=100: send_api_request(
        f"/token/holders",
        url_params={"address": address, "page_size": page_size, "page": page},
    ),
    "transfers": lambda address,
    remove_spam=True,
    exclude_amount_zero=True,
    page=1,
    page_size=100: send_api_request(
        f"/account/transfer",
        url_params={
            "address": address,
            "page_size": page_size,
            "page": page,
            "remove_spam": str(remove_spam).lower(),
            "exclude_amount_zero": str(exclude_amount_zero).lower(),
        },
    ),
    "token_holders_total": lambda address: send_api_request(
        f"/token/holder/total", url_params={"address": address}
    ),
    "account_info": lambda address: send_api_request(
        f"/account", url_params={"address": address}
    ),
    "portofolio": lambda address,
    type="token",
    page=1,
    page_size=100,
    hide_zero=True: send_api_request(
        f"/account/tokenaccounts",
        url_params={
            "address": address,
            "type": type,
            "page": page,
            "page_size": page_size,
            "hide_zero": hide_zero,
        },
    ),
    "balance_history": lambda address: send_api_request(
        f"/analytics/account/balance-history", url_params={"address": address}
    ),
    "top_address_transfers": lambda address, range_days=7: send_api_request(
        f"/analytics/account/top-address-transfers",
        url_params={"address": address, "range": range_days},
    ),
    "token_data": lambda token_address="So11111111111111111111111111111111111111112": send_api_request(
        f"/common/sol-market", url_params={"tokenAddress": token_address}
    ),
}
