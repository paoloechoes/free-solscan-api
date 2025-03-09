# free-solscan-api

`free-solscan-api` is a Python package that allows you to access Solana on-chain data through the Solscan API.

No rate limits, no API key, no restrictions, all for **free**.

## Important Disclaimer
This project is not intended for production use as it utilizes the Solscan Website API, which powers the data on their website but is not officially supported for external use. Therefore, there is no guarantee that this code will continue to work in the future.

## Installation and Usage

To install the package run:
```bash
pip install https://github.com/paoloechoes/free-solscan-api/releases/download/0.0.2/free_solscan_api-0.0.2-py3-none-any.whl
# or
poetry add https://github.com/paoloechoes/free-solscan-api/releases/download/0.0.2/free_solscan_api-0.0.2-py3-none-any.whl
```
To use the package:
```python
import free_solscan_api

# create the router for requests
router = free_solscan_api.Router(free_solscan_api.solscan_endpoints)

# Example
tx_details = router.transaction('57YB5kSKyBqFqLtmnzJKn3ZJuGsaMKDuJaKoZKHZJqU3fTRyoL3b2uMq7K9BNjWvJgDMhrs1npG4PbNzWguNSV1b')

print(tx_details)
```

## How it Works
This package wraps around a specific version of the Solscan API:
`https://api-v2.solscan.io/v2`

This is different from the paid version:
`https://pro-api.solscan.io/v2.0`

(Starting at **$199/month**)

The version we use is the same one the web app uses to load data.

After verifying that the data on the website was not server-side rendered, I examined the network tab in the developer tools. Multiple `XMLHttpRequests` were loading all the data on the page.

For example:
`https://api-v2.solscan.io/v2/transaction/detail?tx=y2WyTkLdQHgJQW44YtKiQLGaYnVxt3X6YS22Qvo599c1RcGnRnuzayAVCaoxvXCahvHJp6Ne1YA24d5KoXYrCS2`

Looking at the headers:
`sol-aut: DciYBB0XNHH5HB9dls0fKMFNDbyPDv6WMh7Vy-Pl`

Using this same auth token for other requests resulted in an unauthorized access error. Each request used a different, seemingly random token.

I examined the function initiating the API request and searched for the string "sol-aut":
```js
this.randomString = this.generateRandomString(),
this.cluster = r.get(l.ov) || "",
n.Z.defaults.withCredentials = this.includedWithCredentialsBaseUrl.includes(e),
this.HttpInstance = n.Z.create({
    baseURL: e,
    withCredentials: this.includedWithCredentialsBaseUrl.includes(e),
    headers: {
        "sol-aut": this.randomString,
        ...!!i && {
            token: i
        }
    },
    ...t
})
```

The "sol-aut" token was generated as a random string for each new request. The `this.generateRandomString()` function:
```js
generateRandomString() {
    let e = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789==--",
        t = Array(16).join().split(",").map(function() {
            return e.charAt(Math.floor(Math.random() * e.length))
        }).join(""),
        r = Array(16).join().split(",").map(function() {
            return e.charAt(Math.floor(Math.random() * e.length))
        }).join(""),
        n = Math.floor(31 * Math.random()),
        i = "".concat(t).concat(r),
        o = [i.slice(0, n), "B9dls0fK", i.slice(n)].join("");
    return o;
}
```

This function generates a valid "sol-aut" key for each new `XMLHttpRequest`.

By using it in our code, we now have **unlimited** free access to the API.

## Contributions
Most endpoints in the pro API docs at [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0/reference/v2-account-transfer) are also available with this package's API version.

However, there are some differences for certain endpoints. If you want to test new ones from the official docs or add some directly from the website, feel free to contribute.

Here is a list of currently implemented endpoints:
- `transaction(tx)`
- `transactions(address, page=1, page_size=40)`
- `defi_activities(address, page=1, page_size=100)`
- `token_holders(address, page=1, page_size=100)`
- `transfers(address, remove_spam=True, exclude_amount_zero=True, page=1, page_size=100)`
- `token_holders_total(address)`
- `account_info(address)`
- `portfolio(address, type="token", page=1, page_size=100, hide_zero=True)`
- `balance_history(address)`
- `top_address_transfers(address, range_days=7)`
- `token_data(token_address="So11111111111111111111111111111111111111112")`

### How to Add New Endpoints
First, go to [Solscan](https://solscan.io) and open your browser's developer tools. Select the **Network** tab and keep it open.

Explore the website and observe the requests the browser makes and the data it queries from the server. Focus on requests to `https://api-v2.solscan.io/v2`. Check the URL-encoded parameters used.

If you find an endpoint not implemented in the code, go to `src/free_solscan_api/api.py` and add it to the `endpoints` dictionary, giving it a name. You will then be able to access it using the router.
