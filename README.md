# auto-support-request

This Azure Function creates a support ticket in Azure Support based on an Azure Monitor alert.

## Prerequisites

- An Azure subscription
- An Azure Monitor alert
- A Professional Direct, Premier, or Unified technical support plan
- An Azure AD App Registration that has the 'Support Request Contributor' role at the subscription scope.

## Deployment

You can deploy this Azure Function to Azure with one click using the button below:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com/troyhite/auto-support-request/main/azuredeploy.json)

   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "<your-storage-account-connection-string>",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AZURE_SUBSCRIPTION_ID": "<your-subscription-id>",
       "AZURE_TENANT_ID": "<your-tenant-id>",
       "AZURE_CLIENT_ID": "<your-client-id>",
       "AZURE_CLIENT_SECRET": "<your-client-secret>",
       "AZURE_SUPPORT_SUBSCRIPTION_ID": "<your-support-subscription-id>"
     }
   }

Replace the values in angle brackets with your own values.

4. Open the terminal in Visual Studio Code and run the following command to install the required Python packages:
    ```python
    pip install -r requirements.txt
    ```
5. Deploy the Azure Function to Azure by running the following command in the terminal:
    ```python
    func azure functionapp publish
    ```
Replace `<your-function-app-name>` with the name of your Azure Function App.

6. In the Azure portal, navigate to your Azure Monitor alert and add an action group that calls your Azure Function.

- Select "Add action group".
- Enter a name for the action group.
- Select "Webhook" as the action type.
- Enter the URL of your Azure Function in the "Service URI" field.
- Select "POST" as the HTTP method.
- Enter the following JSON payload in the "Body" field:

  ```json
  {
    "alertRuleName": "{AlertRuleName}",
    "alertRuleDescription": "{AlertRuleDescription}",
    "alertSeverity": "{AlertSeverity}",
    "alertContext": "{AlertContext}"
  }
  ```

  Replace `{AlertRuleName}`, `{AlertRuleDescription}`, `{AlertSeverity}`, and `{AlertContext}` with the appropriate values.

7. Save the action group.

Your Azure Function is now set up to create a support ticket in Azure Support when an Azure Monitor alert is triggered.