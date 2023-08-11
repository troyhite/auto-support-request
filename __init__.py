import logging
import os
import json
import requests
import azure.functions as func
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    # Get the alert details from the request body
    alert_payload = req.get_json()
    alert_name = alert_payload['data']['essentials']['alertRuleName']
    alert_severity = alert_payload['data']['essentials']['severity']
    alert_description = alert_payload['data']['essentials']['description']
    alert_resource_id = alert_payload['data']['essentials']['monitoringService']

    # Get the resource group name from the alert resource ID
    resource_group_name = ""
    resource_id_parts = alert_resource_id.split('/')
    if len(resource_id_parts) >= 5:
        resource_group_name = resource_id_parts[4]

    # Check if the support ticket name is available
    support_ticket_name = f"{alert_name} ({alert_severity})"
    support_ticket_name = ''.join(e for e in support_ticket_name if e.isalnum() or e in ['-', '_'])
    support_ticket_name = support_ticket_name[:64] # limit the length to 64 characters
    support_ticket_name_available = check_support_ticket_name_availability(subscription_id, support_ticket_name)

    # Create the support ticket if the name is available
    if support_ticket_name_available:
        support_ticket_payload = {
            "properties": {
                "serviceId": "/providers/Microsoft.Support/services/5a813df8-0060-7015-892d-9f17015a6706",
                "title": support_ticket_name,
                "description": alert_description,
                "problemClassificationId": "/providers/Microsoft.Support/services/5a813df8-0060-7015-892d-9f17015a6706/problemClassifications/59297240-0228-3915-8fae-553a01974f0b",
                "severity": "moderate",
                "contactDetails": {
                    "firstName": "First",
                    "lastName": "Last",
                    "primaryEmailAddress": "you@example.com",
                    "preferredSupportLanguage": "en-US",
                    "preferredTimeZone": "Central Standard Time",
                    "country": "US"
                },
                "technicalTicketDetails": {
                    "resourceId": alert_resource_id
                },
                "properties": {
                    "alertName": alert_name,
                    "resourceGroupName": resource_group_name
                }
            }
        }
        create_support_ticket(subscription_id, support_ticket_name, support_ticket_payload)
        return func.HttpResponse(f"Support ticket created with name: {support_ticket_name}")
    else:
        return func.HttpResponse(f"Support ticket name {support_ticket_name} is not available")

def check_support_ticket_name_availability(subscription_id, support_ticket_name):
    # Check if the support ticket name is available
    credential = DefaultAzureCredential()
    access_token = credential.get_token("https://management.azure.com/.default").token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Support/checkNameAvailability?api-version=2020-04-01"
    payload = {
        "name": support_ticket_name,
        "type": "Microsoft.Support/supportTickets"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        response_json = response.json()
        return response_json['nameAvailable']
    else:
        logging.error(f"Failed to check support ticket name availability. Error: {response.text}")
        return False

def create_support_ticket(subscription_id, support_ticket_name, support_ticket_payload):
    # Create the support ticket
    credential = DefaultAzureCredential()
    access_token = credential.get_token("https://management.azure.com/.default").token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Support/supportTickets/{support_ticket_name}?api-version=2020-04-01"
    response = requests.post(url, headers=headers, json=support_ticket_payload)
    if response.status_code == 202:
        logging.info(f"Support ticket created with name: {support_ticket_payload['properties']['title']}")
    else:
        logging.error(f"Failed to create support ticket. Error: {response.text}")