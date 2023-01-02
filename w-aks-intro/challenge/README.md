# Challenge
You will deploy application consisting of 3 components - web application (with headings and links), Doom in browser and Wolfenstein 3D in browser.

Build web application and push it to your registry. Use environmental variable "NAME" and set it to you name (eg. "Tomas Kubica") so this is presented on landing page. Also configure DOOM_URL and WOLFENSTEIN_URL so your links work. This web web should run on games.yourip.nip.io. Container runs on port 80.

Dockefile for Doom application is available in src folder and runs on port 8000. Deploy it to your Kubernetes cluster and let it run on doom.games.yourip.nip.io (on port 80).

Dockefile for Wolfenstein application is available in src folder and runs on port 8000. Deploy it to your Kubernetes cluster and let it run on wolfenstein.wolfenstein.games.yourip.nip.io (on port 80).

Make screenshots of your apps running in browser to proof you have completed and celebrate!
