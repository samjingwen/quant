import os

from cryptography.fernet import Fernet, InvalidToken


def load_dotenv(dotenv_path: str = '.env') -> None:
    """Load environment variables from a .env file.
    Detect and decrypt values prefixed with FERNET: using Fernet."""
    try:
        with open(dotenv_path, encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('\'"')

                prefix = "FERNET:"
                if val.startswith(prefix):
                    token = val[len(prefix):]
                    try:
                        fernet_key = _get_fernet_key()
                        val = fernet_key.decrypt(token.encode()).decode()
                    except (InvalidToken, KeyError):
                        print(f"Warning: failed to decrypt {key}")
                        # Leave the original value if decryption fails
                        continue

                os.environ.setdefault(key, val)
    except FileNotFoundError:
        pass


def _get_fernet_key() -> Fernet:
    key = os.getenv("FERNET_KEY")
    if not key:
        raise RuntimeError("Environment variable FERNET_KEY is not set")
    return Fernet(key.encode())



# key = _get_fernet_key()
# message = key.encrypt("super-secret-password".encode()).decode()
# print(message)