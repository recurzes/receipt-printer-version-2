import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, client_secret: str) -> bool:
    expected_signature = hmac.new(
        client_secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)