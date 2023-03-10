#!/bin/

# On each node
## Install packages
yum -y install epel-release
yum -y install pacemaker pcs fence-agents-scsi nginx corosync watchdog gfs2-utils.x86_64 lvm2-cluster.x86_64

## Install webapp
echo $HOSTNAME web site is ready! > /usr/share/nginx/html/index.html
mkdir /usr/share/nginx/html/shared

## Prepare for pacemaker
cp /usr/share/cluster/fence_scsi_check /etc/watchdog.d/
systemctl enable watchdog
systemctl enable pcsd
systemctl enable corosync
systemctl enable pacemaker
systemctl start watchdog
systemctl start pcsd
echo Azure12345678! | passwd --stdin hacluster

# Cluster

## Create cluster and start
pcs cluster auth vm1 vm2 -u hacluster -p Azure12345678!
pcs cluster setup --name mycluster vm1 vm2
pcs cluster start --all
pcs cluster enable --all
pcs property set stonith-enabled=true
pcs property set no-quorum-policy=freeze


## Create SCSI PR fencing
pcs stonith create scsi fence_scsi pcmk_host_list="vm1 vm2" devices="/dev/sdc" meta provides="unfencing"

## Configure NGINX as cluster service
pcs resource create nginx ocf:heartbeat:nginx configfile=/etc/nginx/nginx.conf op monitor interval=10s

## Colocate both resources
pcs constraint colocation add nginx with scsi INFINITY

## Create distributed lock for gfs2
pcs resource create dlm ocf:pacemaker:controld op monitor interval=30s on-fail=fence clone interleave=true ordered=true

# Run on ALL nodes
/sbin/lvmconf --enable-cluster

# Run on SINGLE node
pcs resource create clvmd ocf:heartbeat:clvm op monitor interval=30s on-fail=fence clone interleave=true ordered=true
pcs constraint order start dlm-clone then clvmd-clone
pcs constraint colocation add clvmd-clone with dlm-clone
pcs constraint colocation add clvmd-clone with scsi

pvcreate /dev/sdc
vgcreate -Ay -cy clustervg /dev/sdc 
lvcreate -L8G -n clusterlv clustervg

mkfs.gfs2 -O -j2 -p lock_dlm -t mycluster:sharedFS /dev/clustervg/clusterlv 

pcs resource create clusterfs Filesystem device="/dev/clustervg/clusterlv" directory="/usr/share/nginx/html/shared" fstype="gfs2" options="noatime" op monitor interval=10s on-fail=fence clone interleave=true

pcs constraint order start clvmd-clone then clusterfs-clone
pcs constraint colocation add clusterfs-clone with clvmd-clone

## Check cluster status
pcs status
pcs status cluster
pcs status nodes
pcs status resources


## Check STONITH and SCSI PRs
pcs stonith show scsi
stonith_admin -L

sg_persist -n -i -k -d /dev/sdc   # Should see two registrations
sg_persist -s /dev/sdc  
pcs stonith fence vm2             # Simulate vm2 failure

## Restart cluster
pcs cluster stop --all
pcs cluster start --all


yum install lvm2-cluster gfs2-utils dlm -y