echo ### Installing services
apt update
apt install -y nginx

echo ### Configuring services
echo "Hello from Nginx" > /var/www/html/index.html
echo $(date) >> /var/www/html/index.html
