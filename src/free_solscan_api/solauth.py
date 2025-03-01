import random


def generate_solauth_token() -> str:
    """
    Generate a valid sol-aut token used to authenticate requests to the Solscan API.
    """
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789==--"
    t = "".join(random.choice(chars) for _ in range(16))
    r = "".join(random.choice(chars) for _ in range(16))
    n = random.randint(0, 31)
    i = t + r
    return i[:n] + "B9dls0fK" + i[n:]
