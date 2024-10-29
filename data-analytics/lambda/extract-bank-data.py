def lambda_handler(event, context):
    # Assuming event contains the row data
    Date = event['Date']
    Description = event['Description']
    ChequeNumber = event['ChequeNumber']

    return {
        'date': Date,
        'description': Description,
        'chequenumber': ChequeNumber
    }