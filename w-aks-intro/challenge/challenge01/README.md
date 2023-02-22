# Challenge 01

In src folder you will find two applications - app01 is static web page (you can run it on nginx or apache) and app02 is simple Python web application.

- Create Dockerfile for both apps
- Build apps and push to your container registry
- Prepare Deployment, Service and Ingress for both apps
- Use Kustomize or Helm to package all components and deploy prod into prod namespace and test into test namespace
- Configure ingress to:
  - prod.ip.nip.io -> app01 in production
  - prod.ip.nip.io-app02 -> app02 in production
  - test.ip.nip.io -> app01 in test
  - test.ip.nip.io-app02 -> app02 in test
- Prod should run app02 v1 while test should run app02 v2