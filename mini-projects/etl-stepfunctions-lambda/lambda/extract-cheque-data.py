def lambda_handler(event, context):
    # Assuming event contains the row data
    ChequeNumber = event['ChequeNumber']
    IssuerName = event['IssuerName']
    IssuerBank = event['IssuerBank']
    FRAUD = event['FRAUD']

    return {
        'chequenumber': ChequeNumber,
        'issuername': IssuerName,
        'issuerbank': IssuerBank,
        'fraud': FRAUD
    }