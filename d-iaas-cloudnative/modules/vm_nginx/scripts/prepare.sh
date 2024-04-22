echo ### Configuring NGINX
cat <<EOF > /etc/nginx/sites-available/default
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /mnt/myshare;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                try_files \$uri \$uri/ =404;
        }
}

server {
        listen 80;
        listen [::]:80;

        root /default_site;

        index index.html;

        server_name node.demo.local;

        location / {
                try_files \$uri \$uri/ =404;
        }
}
EOF

if [ ! -d "/etc/default_site" ]; then
mkdir /default_site
fi

echo Hello from $HOSTNAME >> /default_site/index.html

systemctl restart nginx

echo ### Get secrets from Key Vault
az login --identity --allow-no-subscriptions
password=$(az keyvault secret show --vault-name $keyvaultname --name storage-key --query value -o tsv)

echo ### Mounting Azure File Share
mkdir /mnt/myshare
if [ ! -d "/etc/smbcredentials" ]; then
mkdir /etc/smbcredentials
fi
if [ ! -f "/etc/smbcredentials/storage.cred" ]; then
    echo "username=$storagename" >> /etc/smbcredentials/storage.cred
    echo "password=$password" >> /etc/smbcredentials/storage.cred
fi
sudo chmod 600 /etc/smbcredentials/storage.cred

echo "//$storagename.file.core.windows.net/myshare /mnt/myshare cifs nofail,credentials=/etc/smbcredentials/storage.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30" >> /etc/fstab
mount -t cifs //$storagename.file.core.windows.net/myshare /mnt/myshare -o credentials=/etc/smbcredentials/storage.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30