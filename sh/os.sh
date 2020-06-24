


DIR="/mnt/hgfs/iso"


mkdir -p customISO originISO
#mount /mnt/hgfs/iso/CentOS-7-x86_64-DVD-1908.iso /root/originISO/
mount ${DIR}/CentOS-7-x86_64-DVD-1611.iso /root/originISO/
rsync -a --exclude=Packages/  /root/originISO/ /root/customISO/



#!/bin/bash
rpm -qa  > package-list.txt
old_rpms='/root/originISO/Packages'
new_rpms='/root/customISO/Packages'
while read line; do
    cp ${old_rpms}/${line}*.rpm ${new_rpms} || echo "${line} not exist..."
done < package-list.txt
rm -f package-list.txt


yum install -y --downloadonly --downloaddir="/root/customISO/Packages/" autoconf automake bash-completion \
		bind-utils curl-devel dos2unix ethtool gcc gcc-c++ gdb git glib2-devel gzip \
		iptables-services ipvsadm iscsi-initiator-utils libcurl-devel lrzsz make \
		ncurses-devel net-tools openssh-clients openssl pam pam-devel pcre pcre-devel \
		readline-devel redhat-lsb tcpdump telnet unzip vim-enhanced wget yum-utils zlib zlib-devel



cd /root/customISO/
mv repodata/*comps.xml repodata/comps.xml
cd repodata/
ls | grep -v comps.xml$|xargs rm
yum -y install createrepo mkisofs dosfstools syslinux
cd /root/customISO/
ls -l /root/customISO/repodata
createrepo -g repodata/comps.xml /root/customISO/
ls -l /root/customISO/repodata


mkisofs -o ${DIR}/CentOS-7.3.iso -b isolinux/isolinux.bin -c isolinux/boot.cat --no-emul-boot --boot-load-size 4 --boot-info-table -J -R -V "CentOS 7 x86_64" .
isohybrid ${DIR}/CentOS-7.3.iso