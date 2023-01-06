# Preparation and tooling

## Participant
- Make sure you can access dev environment in your Azure with proper rights -> access portal.azure.com, login, check subscriptions
- Install Azure CLI on your machine using this [guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and make sure you can authenticate (use "az group create -n yournametest-rg -l northeurope" to check you can create resource group and then use "az group delete -n yournametest-rg" to delete it)
- Install [Visual Studio Code](https://code.visualstudio.com/Download) and install followign plugins:
  - ms-kubernetes-tools.vscode-kubernetes-tools
  - ms-vscode.vscode-node-azure-pack
  - ms-kubernetes-tools.vscode-aks-tools
- Install [kubectl](https://kubernetes.io/docs/tasks/tools/) and optionally [helm](https://helm.sh/docs/intro/install/)
- You may want to install 3rd party UI (but you can also use Azure portal or CLI during workshop)
  - ASCII based interactive UI for keyboard-focused people: [k9s](https://k9scli.io/topics/install/)
  - GUI based for mouse-focused people: [kubelens](https://k8slens.dev/)
- Clone this repo to your computer and learn [Git basics](https://docs.microsoft.com/en-us/azure/devops/repos/git/gitworkflow?view=azure-devops) like clone, pull, push, commit and work with Pull requests
- You may want to get familiar with Azure basics before workshop starts:
  - [Azure Portal intro](https://docs.microsoft.com/en-us/learn/modules/explore-azure-portal/)
  - [Azure CLI intro](https://docs.microsoft.com/en-us/learn/modules/control-azure-services-with-cli/)
  - [Azure Fundamentals intro](https://docs.microsoft.com/en-us/learn/modules/intro-to-azure-fundamentals/)

## Organizer
- Get subscription ready with enough VM core quotas (B-series) -> use EA, CSP or PAYG, but NOT trial subscriptions due to low quota
- Every participant to be Owner of this subscription for simplicity (you can delete subscription after training - it is good practice have short-lived subscription just for purpose of training and then people should use your dev/sandbox environment)
- Prefer subscription in customer tenant
- Give access on Owner level to instructor one day before start so shared coponents can be prepared
- Check every participant is prepared as per previous section (especially they can access environment) so time is not lost
- Trainer need to deploy environment.bicep template in resource/containerapp folder before start of lab 2