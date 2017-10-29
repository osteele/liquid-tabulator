import os
import json


def tabulate(event, context):
    gsheet_key = os.getenv('GOOGLE_SHEET_KEY')
    gsheet_range = os.getenv('GOOGLE_SHEET_RANGE')

    body = {
        "message": "Google sheet key={}; range={}".format(gsheet_key, gsheet_range),
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
