# Preparation and tooling

## Participant
- Make sure you can access dev environment in your Azure with proper rights -> access portal.azure.com, login, check subscriptions
- Install Azure CLI on your machine using this [guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and make sure you can authenticate (use "az group create -n yournametest-rg -l northeurope" to check you can create resource group and then use "az group delete -n yournametest-rg" to delete it)
- Recommended: Install [Visual Studio Code](https://code.visualstudio.com/Download)
- Clone this repo to your computer and learn [Git basics](https://docs.microsoft.com/en-us/azure/devops/repos/git/gitworkflow?view=azure-devops) like clone, pull, push, commit and work with Pull requests
- You may want to get familiar with Azure basics before workshop starts:
  - [Azure Portal intro](https://docs.microsoft.com/en-us/learn/modules/explore-azure-portal/)
  - [Azure CLI intro](https://docs.microsoft.com/en-us/learn/modules/control-azure-services-with-cli/)
  - [Azure Fundamentals intro](https://docs.microsoft.com/en-us/learn/modules/intro-to-azure-fundamentals/)
- With online delivery it is better to have one monitor to watch the call and second monitor to work on

## Organizer
- Get subscription ready with enough VM core quotas (B-series) -> use EA, CSP or PAYG, but NOT trial subscriptions due to low quota. This lab requires about 6 B-series core per participant in northeurope region (do no forget to also check your total region cores quota). [https://docs.microsoft.com/en-us/azure/networking/check-usage-against-limits](https://docs.microsoft.com/en-us/azure/networking/check-usage-against-limits)
- Every participant to be **Owner** of this subscription for siplicity (you can delete subscription after training - it is good practice to have short-lived subscription just for purpose of training and later people should use your dev/sandbox environment if they want to continue exploring)
- Prefer subscription in customer tenant
- Give access on Owner level to instructor one day before start
- Check every participant is prepared as per previous section (especialy they can access environment) so time is not lost