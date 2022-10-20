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


@dataclass
class PaymentVoucher:
    """Case preserved to keep consistent witch provided api definition"""
    ReferenceNo: str = 'T1120000V220000534'
    ApplyDate: str = '2022-05-13 00:00:00.000'
    subBudgetClass: str = '201'
    paymentCode: str = 'HKMU'
    paymentBIC: str = 'CORUTZTZ'
    paymentDesc: str = 'Malipo ya ruzuku'
    narration: str = 'Malipo ya ruzuku'
    controlNumber: str = 'N/A'
    payerBankAccount: str = "01J028467502",
    payeeAccountName: str = "test account",
    unappliedAccount: str = "01J028467502",
    payeeBankAccount: str = "0150240150100",
    payerBankName: str = "CRDB",
    payeeBankName: str = "CRDB",
    amount: str = 338937.5,
    Currency: str = "TZS"
    payStationiD: str = " 12659"


@dataclass
class PvRequestMessage:
    messageHeader: MessageHeader
    paymentVoucher: PaymentVoucher


@dataclass
class PaymentVoucherSubmissionRequest:
    message: PvRequestMessage
    digitalSignature: str


@dataclass
class PaymentVoucherSubmissionResponse:
    trxStsCode: str


@dataclass
class MessageSummary:
    statusDesc: str  # Depending on status
    status: str = Literal['ACCEPTED', 'Rejected', 'Cancelled']  # Depending on status
    orgMsgId: str = '20210722205348'
    createdAt: str = '2021-07-22T21:54:26.915'  # Timestamp?
    PVNo: str = 'ILMS0000PV00001'


@dataclass
class PvSubmissionResponse:
    messageHeader: MessageHeader
    messageSummary: MessageSummary

