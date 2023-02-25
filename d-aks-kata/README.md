# AKS with Kata containers
In standard Kubernetes deployment containers share kernel which might not be considered enough isolation in dinance, healtcare or when running untrusted code in SaaS platform (eg. when SaaS customers can bring their own code to bring custom behavior - eg. custom data processing capabilities).

This demo deploy AKS with Mariner OS and enable Kata containers runtime - isolation using nested virtualization (hypervisor). Such solution enables hard multi-tenancy on shared AKS nodes. It also enables Flux and downloads demo application - trusted and untrusted example.

After demo is deployed check logs of trusted and untrusted Pods and observe how trusted is using the same kernel as host while untrusted runs on its own kernel.