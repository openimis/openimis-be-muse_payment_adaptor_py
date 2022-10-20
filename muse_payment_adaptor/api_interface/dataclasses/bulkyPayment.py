from dataclasses import dataclass
from decimal import Decimal
from typing import Literal, List

from muse_payment_adaptor.api_client.dataclasses.generic import MessageHeader, MessageSummary


@dataclass
class PaymentSummary:
    institutioncode: str = "T1120000"
    totalAmount: str = "72274.00"
    referenceNo: str = "4020"
    paymentDesc: str = "REFUND LOANEES WITH AMOUNT"
    applyDate: str = "2022-09-11 18:59:49.104"
    noofTransaction: str = 3  # Programmatically created based on payList
    isSTP: str = True


@dataclass
class PayListElement:
    paymentChannel: str = Literal['Bank Account', 'Mobile']
    payeeCode: str = "S09260061"  # HF / EO ?
    payeeName: str = "IBRAHIM N KIMAMBO"  # HF / EO Name?
    payeeAccountNumber: str = "9821231996" # EO Bank account?
    payeeAccountName: str = "IBRAHIM N KIMAMBO"
    payeeBankName: str = "ACCESSBANK"
    payeeBankBic: str = "ACTZTZTZ"
    amount: str = "18244.0"  # Shouldn't be numeric?


@dataclass
class BulkyPaymentSubmissionMessage:
    messageHeader: MessageHeader
    paymentSummary: PaymentSummary
    payList: List[PayListElement]


@dataclass
class BulkyPaymentSubmissionRequest:
    message: BulkyPaymentSubmissionMessage
    digitalSignature: str


@dataclass
class BPPayElement:
    PayeeCode: str
    EndtoEndid: str
    Amount: float


@dataclass
class BulkyPaymentSubmissionResponseMessage:
    messageHeader: MessageHeader
    messageSummary: MessageSummary
    BPPaylist: List[BPPayElement]


@dataclass
class BulkyPaymentSubmissionResponse:
    message: BulkyPaymentSubmissionResponseMessage
    digitalSignature: str
