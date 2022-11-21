import base64
import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from muse_payment_adaptor.apps import MusePaymentAdaptorConfig

__padding = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
__algorithm = hashes.SHA1()

logger = logging.getLogger(__name__)


def create_signature_bytes(message: bytes) -> bytes:
    """
    For a given message, create a signature returned as byte array. To use the signature in text payload use
    create_signature_b64_string
    """
    certificate = MusePaymentAdaptorConfig.certificate
    signature = certificate.key.sign(message, padding=__padding, algorithm=__algorithm)
    return signature


def create_signature_b64_bytes(message: bytes) -> bytes:
    """
    For a given message, create a signature encoded as base64, returned as byte array. Intermediate format between
    byte array and b64 string. To use the signature in text payload use create_signature_b64_string
    """
    return base64.encodebytes(create_signature_bytes(message))


def create_signature_b64_string(message: bytes) -> str:
    """
    For a given message, create a signature encoded as base64, returned as string. To be used in string payloads.
    """
    return create_signature_b64_bytes(message).decode('ascii')


def verify_signature_bytes(message: bytes, signature: bytes) -> bool:
    """
    For a given message, check if a signature (provided as byte array) is valid. Should be true for a signature created
    with create_signature_bytes. To validate the signature from text payload (b64) use verify_signature_b64_string.
    """
    certificate = MusePaymentAdaptorConfig.certificate
    public_key = certificate.key.public_key()
    try:
        public_key.verify(
            signature,
            message,
            padding=__padding,
            algorithm=__algorithm
        )
        return True
    except InvalidSignature:
        logger.debug("Signature validation failed")
        return False


def verify_signature_b64_bytes(message: bytes, signature: bytes) -> bool:
    """
    For a given message, check if a signature (encoded in base64, provided as byte array) is valid. Should be true for
    a signature created with create_signature_b64_bytes. To validate the signature from text payload (b64) use
    verify_signature_b64_string.
    """
    return verify_signature_bytes(message, base64.decodebytes(signature))


def verify_signature_b64_string(message: bytes, signature: str) -> bool:
    """
    For a given message, check if a signature (encoded in base64, provided as string) is valid. Should be true for
    a signature created with create_signature_b64_string. To be used to validate the signature from text payload.
    """
    return verify_signature_b64_bytes(message, str.encode(signature, 'ascii'))
