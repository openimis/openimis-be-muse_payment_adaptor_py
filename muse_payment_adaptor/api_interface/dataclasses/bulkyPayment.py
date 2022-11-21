from pydantic import BaseModel
from typing import List


class BulkyPaymentMessageHeader(BaseModel):
    sender: str
    receiver: str
    msgId: str
    messageType: str
    paymentType: str


class BulkyPaymentSummary(BaseModel):
    institutioncode: str  # "T1120000"
    totalAmount: str  # "72274.00"
    referenceNo: str  # "4020"
    paymentDesc: str  # "REFUND LOANEES WITH AMOUNT"
    applyDate: str  # "2022-09-11 18:59:49.104"
    noofTransaction: int  # 3  # Programmatically created based on payList
    isSTP: bool  # True


class BulkyPaymentPayListElement(BaseModel):
    paymentChannel: str  # Literal['Bank Account', 'Mobile']
    payeeCode: str  # "S09260061"  # HF / EO ?
    payeeName: str  # "IBRAHIM N KIMAMBO"  # HF / EO Name?
    payeeAccountNumber: str  # "9821231996"  # EO Bank account?
    payeeAccountName: str  # "IBRAHIM N KIMAMBO"
    payeeBankName: str  # "ACCESSBANK"
    payeeBankBic: str  # "ACTZTZTZ"
    amount: str  # "18244.0"  # Shouldn't be numeric?


class BulkyPaymentSubmissionRequestMessage(BaseModel):
    messageHeader: BulkyPaymentMessageHeader
    paymentSummary: BulkyPaymentSummary
    payList: List[BulkyPaymentPayListElement]


class BulkyPaymentSubmissionRequest(BaseModel):
    message: BulkyPaymentSubmissionRequestMessage
    digitalSignature: str
