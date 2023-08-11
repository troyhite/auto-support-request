# auto-support-request

This Azure Function creates a support ticket in Azure Support based on an Azure Monitor alert.

## Prerequisites

- An Azure subscription
- An Azure Monitor alert
- A Professional Direct, Premier, or Unified technical support plan
- An Azure AD App Registration that has the 'Support Request Contributor' AND 'Reader' roles at the subscription scope.
    - This app registration will need the following API permissions:
        - Azure Service Management: user_impersonation
        - Microsoft Graph: Application.ReadWrite.All, Application,ReadWrite.OwnedBy, User.Read

## Deployment

- Azure Function will need the following app configs added to function:
    - AZURE_SUBSCRIPTION_ID
    - AZURE_TENANT_ID
    - AZURE_CLIENT_ID
    - AZURE_CLIENT_SECRET
- The 'test-payload.json' is an example to use while testing the Function post deployment.
- The 'problemClassifications_vpngateway.json' gives all the problemClassificationIds for the various support options. These can then be coorelated to the type of ticket being created. That functionality is still in the works.