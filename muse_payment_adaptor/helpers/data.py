from core import TimeUtils

test_hf_data = {
    'code': 'TEST1',
    'name': 'Test Hospital',
    'acc_code': 'DL0002',
    'legal_form_id': 'G',
    'level': 'H',
    'location_id': 55,
    'address': 'Lantern Road 21 P.O.Box 3425',
    'email': 'juhygtfrx@aaaa.pl',
    'care_type': 'B',
    'services_pricelist_id': 7,
    'items_pricelist_id': 8,
    'audit_user_id': 1,
    'validity_from': TimeUtils.now()
}

test_hf_bank_info_data = {
    'bank_name': 'test bank info',
    'account_name': 'test account name',
    'bank_account': 'test bank account',
    'bic': 'test bic',
}