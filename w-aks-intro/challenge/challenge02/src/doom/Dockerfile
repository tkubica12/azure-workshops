FROM node:16-alpine

# Set up JS-DOS, NPM packages
WORKDIR site
RUN wget https://js-dos.com/6.22/current/js-dos.js && \
    wget https://js-dos.com/6.22/current/wdosbox.js && \
    wget https://js-dos.com/6.22/current/wdosbox.wasm.js
RUN npm install -g serve

# Set up game hosting
COPY doom.zip .
COPY index.html .
ENTRYPOINT npx serve -l tcp://0.0.0.0:8000