# Azure Container Apps demo

Demonstrations:
- Connect to ext container and see access to Internet does not go via FW by calling curl http://ifconfig.io. Then connect to int container, do the same and see error message from firewall - UDRs work.
- Showcase /27 subnet
- Init container - show in web-ext
- Files mounted as volume - show on ext-env and then jump to web-ext container an list /myfiles
- Use UI to add managed certificate and custom FQDN to web on ext environment
- Use UI to showcase deployment of Azure Function in Docker to environment - there is also Function already deployed
- Show deployed Job