from pydantic import BaseModel
from typing import List


class BulkyPaymentMessageHeader(BaseModel):
    sender: str
    receiver: str
    msgId: str
    messageType: str
    paymentType: str


class BulkyPaymentSummary(BaseModel):
    institutioncode: str
    totalAmount: str
    referenceNo: str
    paymentDesc: str
    applyDate: str
    noofTransaction: int
    isSTP: bool


class BulkyPaymentPayListElement(BaseModel):
    paymentChannel: str
    payeeCode: str
    payeeName: str
    payeeAccountNumber: str
    payeeAccountName: str
    payeeBankName: str
    payeeBankBic: str
    amount: str


class BulkyPaymentSubmissionRequestMessage(BaseModel):
    messageHeader: BulkyPaymentMessageHeader
    paymentSummary: BulkyPaymentSummary
    payList: List[BulkyPaymentPayListElement]


class BulkyPaymentSubmissionRequest(BaseModel):
    message: BulkyPaymentSubmissionRequestMessage
    digitalSignature: str
