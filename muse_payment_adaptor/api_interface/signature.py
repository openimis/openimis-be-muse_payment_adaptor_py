import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from muse_payment_adaptor.apps import MusePaymentAdaptorConfig

__padding = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
__algorithm = hashes.SHA1()

logger = logging.getLogger(__name__)


def create_signature(message: bytes) -> bytes:
    certificate = MusePaymentAdaptorConfig.certificate
    signature = certificate.key.sign(message, padding=__padding, algorithm=__algorithm)
    return signature


def verify_signature(message: bytes, signature: bytes) -> bool:
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
