import json
# import azure form recognizer libraries
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

# create variable for azure form recognizer endpoint and key
endpoint = "<your endpoint>"
key = "<your key>"

# create the client and authenticates with the endpoint and key
form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))

myReceiptUrl = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png"

# user form recognizer client to recognize image from myReceiptUrl
poller = form_recognizer_client.begin_recognize_receipts_from_url(myReceiptUrl)
result = poller.result()

# loop through results and extract data from receipt
for receipt in result:
    for name, field in receipt.fields.items():
        if name == "Items":
            print("Receipt Items:")
            for idx, items in enumerate(field.value):
                print("...Item #{}".format(idx + 1))
                for item_name, item in items.value.items():
                    print("......{}: {} has confidence {}".format(item_name, item.value, item.confidence))
        else:
            print("{}: {} has confidence {}".format(name, field.value, field.confidence))

