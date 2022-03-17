#!/bin/bash
echo '
  _____                               
  /  _  \ __________ _________   ____  
 /  /_\  \\___   /  |  \_  __ \_/ __ \ 
/    |    \/    /|  |  /|  | \/\  ___/ 
\____|__  /_____ \____/ |__|    \___  
        \/      \/                  \/ 
'

sed -i -e "s/#TODOAPIURL#/${TODOAPIURL/'//'/'\/\/'}/" /usr/share/nginx/html/js/app.js 
sed -i -e "s/#INSTANCENAME#/$(cat /etc/hostname)/" /usr/share/nginx/html/js/app.js 
sed -i -e "s/#INSTANCEVERSION#/$(cat /version | tr -d '\r' | tr -d '\n')/" /usr/share/nginx/html/js/app.js 

echo "$(cat /etc/hostname) - $(cat /version)" > /usr/share/nginx/html/info
