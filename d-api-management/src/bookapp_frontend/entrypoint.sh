#!/bin/sh
envsubst '$REACT_APP_APPLICATION_INSIGHTS_CONNECTION_STRING' < /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.tmp.html
mv /usr/share/nginx/html/index.tmp.html /usr/share/nginx/html/index.html
exec nginx -g 'daemon off;'