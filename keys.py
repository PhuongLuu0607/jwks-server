import uuid, time
from cryptography.hazmat.primitives.asymmetric import rsa  # RSA key generation
import base64  # base64url encoding (required by JWKS)

# Each key is valid for 60 seconds
expiry_time = 60


class KeyManagement:
    def __init__(self):
        # Create 2 lists to store keys
        self.keys = []         # active 
        self.expired_keys = [] # expired 

    def create_new_key(self, expired=False):
        # Implement RSA key pair generation (public and private keys)
        private_key = rsa.generate_private_key(
            public_exponent=65537, 
            key_size=2048
        )

        # Derive public key from private key
        public_key = private_key.public_key()

        # Assign a unique kid
        kid = str(uuid.uuid4()) 

        # Set time expiration
        current_time = int(time.time())  # convert time to seconds
        if expired:
            exp = current_time - 30   # already expired 30 seconds ago
        else:
            exp = current_time + expiry_time   # valid for expiry_time seconds

        # Store key data in dictionary
        keypair = {
            "kid": kid,
            "private": private_key,
            "public": public_key,
            "exp": exp,
        }

        # Save key to correct list
        if expired:
            self.expired_keys.append(keypair)
        else:
            self.keys.append(keypair)
        return keypair

    # This function returns active keys
    def get_active_keys(self):
        current_time = int(time.time()) 
        result = []  # a list for valid keys
        for key in self.keys:
            if key["exp"] > current_time:
                result.append(key)
        return result

    # This function returns expired keys
    def get_expired_keys(self):
        return self.expired_keys

    # This function converts a public key to JSON Web Key format
    def convert_to_jwk(self, key):
        numbers = key["public"].public_numbers()

        # This function converts integer to bytes
        def convert_to_bytes(num):
            bit_length = num.bit_length()
            byte_length = (bit_length + 7) // 8  # round bits up to nearest byte
            return num.to_bytes(byte_length, "big")

        # This function converts bytes to base64url string
        def encode_base64url(val):
            return base64.urlsafe_b64encode(val).rstrip(b"=").decode("utf-8")

        # Convert modulus n and exponent e
        e = convert_to_bytes(numbers.e)
        n = convert_to_bytes(numbers.n)

        return {
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": key["kid"],
            "n": encode_base64url(n),
            "e": encode_base64url(e),
        }
