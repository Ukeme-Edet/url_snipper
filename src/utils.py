import random
import string


def generate_url_key():
    """
    Generate a Fernet key and return it as a base64 encoded string.
    """
    alpha = string.ascii_letters + string.digits
    key = "".join(random.choice(alpha) for _ in range(11))
    return key
