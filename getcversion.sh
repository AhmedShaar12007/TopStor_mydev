#!/usr/bin/sh
cd /TopStor/
echo $@ > /root/getcversion
leaderip=`echo $@ | awk '{print $1}'`
leader=`echo $@ | awk '{print $2}'`
myhost=`echo $@ | awk '{print $3}'`
version=`git branch | grep '*' | awk '{print $2}'`
commit=`git show --abbrev-commit | grep commit | head -1 | awk '{print $2}'`
./etcdput.py $leaderip cversion/$myhost $version-$commit
./etcdput.py $leaderip sync/cversion/_____/request $version-$commit
./etcdput.py $leaderip sync/cversion/_____/request/$leader $version-$commit