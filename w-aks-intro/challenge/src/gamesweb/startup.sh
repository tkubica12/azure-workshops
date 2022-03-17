#!/bin/bash
cat <<EOL 
  _____                               
  /  _  \ __________ _________   ____  
 /  /_\  \\___   /  |  \_  __ \_/ __ \ 
/    |    \/    /|  |  /|  | \/\  ___/ 
\____|__  /_____ \____/ |__|    \___  
        \/      \/                  \/ 
EOL

echo "<H1>Games by $NAME </H1>" > /usr/share/nginx/html/index.html
echo "<BR><BR><a href=\"http://$DOOM_URL\">Play Doom</a>" >> /usr/share/nginx/html/index.html
echo "<BR><BR><a href=\"http://$WOLFENSTEIN_URL\">Play Wolfenstein 3D</a>" >> /usr/share/nginx/html/index.html

