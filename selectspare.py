#!/bin/python3.6
import subprocess,sys,socket
import json
from ast import literal_eval as mtuple
from etcdget import etcdget as get
from etcdput import etcdput as put
from etcddel import etcddel as dels 
from poolall import getall as getall
from syncpools import syncmypools
import logmsg
disksvalue=[]


def mustattach(cmdline,disksallowed,defdisk,myhost):
   print('################################################')
   if len(disksallowed) < 1 : 
    return 'na'
   print('helskdlskdkddlsldssd#######################')
   cmd=cmdline
   spare=disksallowed[0][0]
   if spare['pool']==defdisk['pool']:
    cmdline=['/sbin/zpool', 'remove', defdisk['pool'],spare['name']]
    subprocess.run(cmdline,stdout=subprocess.PIPE)
   cmd.append(spare['name'])
   cmdline=['/sbin/zpool', 'labelclear','-f', spare['name']]
   subprocess.run(cmdline,stdout=subprocess.PIPE)
   print(spare['name'])
   dfasdkjd
   logmsg.sendlog('Dist2','info','system', defdisk['id'],spare['id'],myhost)
   try: 
    subprocess.check_call(cmd)
    logmsg.sendlog('Disu2','info','system', defdisk['id'],spare['id'],myhost)
    syncmypools('all')
    return spare['name'] 
   except subprocess.CalledProcessError:
    with open('/root/tmpselect','w') as f:
     f.write(str(cmd)+'\n')
    logmsg.sendlog('Difa2','error','system', defdisk['id'],spare['id'],myhost)
    disksallowed.pop(0)
    ret=mustattach(cmdline[:-1],disksallowed,defdisk,myhost) 
    return ret
 
def norm(val):
 units={'B':1/1024**2,'K':1/1024, 'M': 1, 'G':1024 , 'T': 1024**2 }
 if type(val)==float:
  return val
 if val[-1] != 'B':
  return float(val) 
 else:
  if val[-2] in list(units.keys()):
   return float(val[:-2])*float(units[val[-2]])
  else:
   return float(val[:-1])*float(units['B'])


def diskreplace(myhost,defdisks,hosts,alldisks,replacelist,raids,pools,exclude,mindisksize):
 if len(defdisks) < 1:
  print('no more defective disks checking for non-red host raids')
  if len(raids) < 1 :
   print('no raids too') 
   return
  raid=raids[0]
  raids.pop(0)
  if raid['name']=='free':
   return

  myhostpools=[pool['name'] for pool in pools if pool['host']==myhost ]
  disksinraid=[(disk['name'],disk['host'],disk['size']) for disk in alldisks if disk['raid'] == raid['name'] and disk['pool'] == raid['pool'] and disk['pool'] in myhostpools ]
  hcount=[]
  for host in hosts:
   hcount.append((host,str(disksinraid).count(host)))
  maxx=max(hcount,key=lambda x: x[1])
  nonblanced=[x for x in hcount if maxx[1]-1 > x[1]]
  selectdisk=[]
  if len(nonblanced) > 0:
   selectdisk=[x for x in disksinraid if x[1]==maxx[0]]
   diskinfo=[x for x in alldisks if x['name']==selectdisk[0][0]]
   mindisksize=min(disksinraid,key=lambda x:norm(x[2]))
   mindisksize=mindisksize[2]
   mindisksize=norm(mindisksize)
   diskreplace(myhost,diskinfo,hosts,alldisks,replacelist,raids,pools,'limithost',mindisksize)
   return
  diskreplace(myhost,[],hosts,alldisks,replacelist,raids,pools,exclude,mindisksize)
  return
 defdisk=defdisks[0]
 dontuse=exclude
 if 'limithost' in exclude:
  dontuse=defdisk['host']
 disksinraid=[disk for disk in alldisks if disk['raid']==defdisk['raid'] and disk['name'] != defdisk['name'] and 'ONLI' in disk['changeop']]
 runninghosts=[disk['host'] for disk in alldisks if disk['raid']==defdisk['raid'] and disk['name'] != defdisk['name'] and 'ONLI' in disk['changeop'] and disk['host'] not in dontuse ]
 if mindisksize < 0:
  mindisk=min(disksinraid,key=lambda x:norm(x['size']))
  mindisk=mindisk['size']
 else:
  mindisk=mindisksize
 disksvalues=[]
 for  rep in replacelist:
  diskvalue=float(0)
  if norm(rep['size']) == norm(mindisk) :
   diskvalue=diskvalue+1
  elif norm(rep['size']) > norm(mindisk): 
       diskvalue=diskvalue+float(1-(norm(rep['size']) - norm(mindisk))/norm(mindisk))
  else:
   diskvalue=-100000
  if dontuse in rep['host']:
   diskvalue=-100000
  if 'spare' in rep['raid']:
    diskvalue=diskvalue+10
  if rep['host'] not in runninghosts: 
   diskvalue=diskvalue+100
  disksvalues.append((rep,diskvalue)) 
 disksvalues=sorted(disksvalues,key=lambda x:x[1], reverse=True)
 if disksvalues[0][1] < -10000:
  return
 if 'spare' in defdisk['raid'] :
  logmsg.sendlog('Dist3','info','system', defdisk['id'],defdisk['host'])
  cmdline=['/sbin/zpool', 'remove', defdisk['pool'],defdisk['name']]
  subprocess.run(cmdline,stdout=subprocess.PIPE)
  ret=replacelist
 elif 'logs' in defdisk['raid'] :
  cmdline=['/sbin/zpool', 'remove', defdisk['pool'],defdisk['name']]
  try:
   subprocess.check_call(cmdline)
   if spare['pool']==defdisk['pool']:
    cmdline=['/sbin/zpool', 'remove', defdisk['pool'],spare['name']]
    subprocess.run(cmdline,stdout=subprocess.PIPE)
   cmdline=['/sbin/zpool', 'add', faultdiskpool,'log']
   try: 
    ret=mustattach(cmdline,disksvalues,defdisk,myhost)
   except subprocess.CalledProcessError:
    pass
  except:
   pass 
 elif 'cache' in defdisk['raid'] :
  cmdline=['/sbin/zpool', 'remove', defdisk['pool'],defdisk['name']]
  try:
   subprocess.check_call(cmdline)
   cmdline=['/sbin/zpool', 'add', defdisk['pool'],'cache']
   try: 
    ret=mustattach(cmdline,disksvalues,defdisk,myhost)
   except subprocess.CalledProcessError:
    pass
  except:
   pass 
 elif 'stripe' in defdisk['raid'] :
  cmdline=['/sbin/zpool', 'attach','-f', defdisk['pool'],disks[0]['name']]
  try: 
   ret=mustattach(cmdline,disksvalues,defdisk,myhost)
  except :
    pass
 elif 'mirror' in defdisk['name']:
  cmdline=['/sbin/zpool', 'detach', defdisk['pool'],defdisk['name']]
  subprocess.run(cmdline,stdout=subprocess.PIPE)
  ret=replacelist
 else:
  cmdline=['/sbin/zpool', 'replace', '-f',defdisk['pool'],defdisk['name']]
  try:
   ret=mustattach(cmdline,disksvalues,defdisk,myhost)
  except subprocess.CalledProcessError:
   pass 
 replacelist=[x for x in replacelist if x['name']!=ret]
 defdisks.pop(0)
 diskreplace(myhost,defdisks,hosts,alldisks,replacelist,raids,pools,exclude,mindisksize)
 
  
def selectspare(*args):
 myhost=args[0]
 newop=getall(myhost)
 if newop==[-1]:
  return
 #allop=getall(myhost,'old')
 #diffop={k:newop[k] for k in allop if allop[k] != newop[k] and 'disk' in k}
 diskreplace(myhost,newop['defdisks'],newop['hosts'],newop['disks'],newop['freedisks']+newop['sparedisks'],newop['raids'],newop['pools'],'allowall',-1)
 return
 
 
if __name__=='__main__':
 selectspare(*sys.argv[1:])
