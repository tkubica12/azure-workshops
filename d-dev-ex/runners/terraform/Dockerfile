FROM mcr.microsoft.com/deployment-environments/runners/core:latest

ARG TERRAFORM_VERSION=1.8.5

# Install Terraform
RUN wget -O terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform.zip && rm terraform.zip
RUN mv terraform /usr/bin/terraform

# Install Git
RUN apt-get update && apt-get install -y git

# Grab all .sh files from scripts, copy to
# root scripts, replace line-endings and make them all executable
COPY scripts/* /scripts/
RUN find /scripts/ -type f -iname "*.sh" -exec dos2unix '{}' '+'
RUN find /scripts/ -type f -iname "*.sh" -exec chmod +x {} \;