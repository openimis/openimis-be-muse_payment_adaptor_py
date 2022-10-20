from dataclasses import dataclass
from typing import Literal


@dataclass
class MessageHeader:
    sender: str
    receiver: str
    msgId: str
    messageType: str
    paymentType: str

    @staticmethod
    def build_request_header():
        return MessageHeader(
            sender='TPLMIS',
            receiver='MUSE',
            msgId='202108091658043453',
            messageType='Payment',
            paymentType='Payment Voucher',
        )

    @staticmethod
    def build_response_header():
        return MessageHeader(
            sender='MUSE',
            receiver='ILMS',
            msgId='FBUS20210722215426884',
            messageType='ACK',
            paymentType='PV',
        )

    @staticmethod
    def build_bulky_payment_submission_request_header():
        return MessageHeader(
            sender="ILMS",
            receiver="MUSE",
            msgId="4020",
            messageType="REFUND",
            paymentType="Refund Bulky"
        )


@dataclass
class MessageSummary:
    statusDesc: str  # Depending on status
    status: str = Literal['ACCEPTED', 'Rejected', 'Cancelled', 'Unapplied']  # Depending on status
    orgMsgId: str = '20210722205348'
    createdAt: str = '2021-07-22T21:54:26.915'  # Timestamp?
    PVNo: str = 'ILMS0000PV00001'

