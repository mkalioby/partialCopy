#! /usr/bin/python
from __future__ import print_function
import sys,os,datetime,subprocess
from . import Common, Config

def run(excuter,Wait=True,output=True):
	PIPE=subprocess.PIPE
	print ("Running",excuter)
	if output:      p=subprocess.Popen(excuter,stdout=PIPE,stderr=PIPE,shell=True)
	else: p=subprocess.Popen(excuter,stdout=None,stderr=None,shell=True)
	if Wait and output:
		out=""
		while p.poll() is None:
			out+= "".join(p.stdout.readlines())
		return out
	elif Wait:
		while p.poll() is None: 
			continue
		return p.returncode
	else:
		return p

def run2(excuter,Wait=True):
	PIPE=subprocess.PIPE
	p=subprocess.Popen(excuter,stdout=PIPE,stderr=PIPE,shell=True)
	if Wait:
		p.wait()
		st=p.stderr.read()
		if len(st)>0:
			return "Childerr: "+ st +" ||| "+ p.stdout.read()
		else:
			return p.stdout.read()
	else:
		return p


def canBeCopied(folder,dest):
	if checkDest(dest)>(checkSrcSize(folder) * 0.05): return True
	return False

def checkSrcSize(folder):
	cmd="du -s %s"%folder
	lines=Common.run2(cmd)
	line=lines[0]
	try:
		csize=long(line.split()[0])
	except:
		csize=long(lines[-1].split()[2])
	return csize

def checkDest(dest):
	lines=Common.run2("df %s"%dest).split("\n")
	line=lines[1]
	try:
		csize=long(line.split()[3])
	except:
		csize=long(lines[2].split()[2])
	return csize

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def copy(src,dest,**kwargs):
	print (kwargs)
	if kwargs["dry_run"]:	 print("Running in Dry run mode")
	doneFiles=[]
	if src[-1]!="/": src+="/"
	logfile=kwargs.get("log",src+".pcp_log") 
	if logfile==None: logfile=src+".pcp_log"
	lstfile=kwargs.get("lst",src+".pcp_lst")
	if lstfile==None: lstfile=src+".pcp_lst"
	rsync_list=kwargs.get("rsync-list",src+".pcp_rsync_list/")
	if rsync_list==None: rsync_list=src+".pcp_rsync_list/"
	if os.path.exists(logfile):
		doneFolders=[l.strip() for l in open(logfile,'r').readlines()]
	logFile=open(logfile,"a")
	rsync_options=kwargs.get("rsync","")
	if rsync_options  == None: rsync_options=""
	if  kwargs["no_scan"] and os.path.exists(lstfile):
		files=[l.strip() for l in open(lstfile,"r").readlines()]
	else:
		print("Finding files to copy........")
		fparams=kwargs.get("find_params",None) if kwargs.get("find_params",None) else ""
		files=run("find %s %s"%(src,fparams))
		print(lstfile)
		lst=open(lstfile,"w")
		lst.write(files)
		lst.close()
		print("Wrote file list to %s"%lstfile)
		files=files.split("\n")
		print("Found %s files"%str(len(files)-1))
		
		
	i=0
	if not os.path.exists(dest): os.makedirs(dest)
	if not os.path.exists(rsync_list): os.makedirs(rsync_list)
	dest_size=checkDest(dest)
	dest_limit=dest_size*0.95
	original_dest_limit=dest_limit
	total=len(files)
	copy_list=[]
	rlist_files=[f for f in os.listdir(rsync_list) if ".pcp." in f]
	badfiles=[]
	bigfiles=[]
	for file in files:
		i+=1
		if file=='': continue
		if file  in doneFiles:
			eprint(file,"copied before")
			continue
		try:
			fsize=float(os.path.getsize(file))
		except:
			badfiles.append(file)
			continue
		print("File Size ",fsize)
		print ("dest limit",dest_limit)
		if fsize<=dest_limit:
			copy_list.append(file)
			dest_limit-=fsize
		else:
			if fsize > original_dest_limit:
				bigfiles.append(file)
			rl_name=rsync_list+".pcp."+str(len(rlist_files)+1)
			rl=open(rl_name,"w")
			files_count=len(copy_list)
			rlist_files.append(rl_name)
			rl.write("\n".join(copy_list))
			rl.close()
			copy_list=[]
			print("%s saved to %s"%(files_count,rl_name))
			if kwargs["dry_run"]:	
				dest_limit=original_dest_limit
				copy_list.append(file)
				dest_limit-=fsize
			else:
				print("HDD is full, breaking....")
				break
				
	rl_name=rsync_list+".pcp."+str(len(rlist_files)+1)
	rl=open(rl_name,"w")
	files_count=len(copy_list)
	rlist_files.append(rl_name)
	rl.write("\n".join(copy_list))
	rl.close()
	copy_list=[]
	print("%s saved to %s"%(files_count,rl_name))
#			exit(-125)	
	if not kwargs["dry_run"]:
		print (datetime.datetime.now())
		res='rsync --safe-links %s %s --files %s %s'%(Config.rsync_options,rsync_options,rsync_list[-1],savePath)
		print(res)
		code=run(res,output=False)
		print (datetime.datetime.now())
		if code==0:
			files=open(rsync_list[-1]).read()
			logFile.write(files)
			logFile.flush()
	print ("The following files aren't copied")
	print (badfiles)
	print ("The following files are big and can't be  copied to the current media")
	print (bigfiles)

if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("src", help="Source Directory")
	parser.add_argument("dest", help="Dest Mountpoint")
	parser.add_argument("-lg", "--log", help="Log File to use")
	parser.add_argument("-ls", "--lst", help="List File to use")
        parser.add_argument("-rf","--rsync-list",help="Where to save rsync list")
	parser.add_argument("-ns", "--no-scan", help="Don't rescan the folder, this needs a previous run",action='store_true')
	parser.add_argument("-d", "--dry-run", help="don't run rsync, just break file list, assume equal size drives",action='store_true')
	parser.add_argument("-rs", "--rsync", help="Extra rsync parameters")
	parser.add_argument("-fp", "--find-params", help="Parameters to find command")
	args = parser.parse_args()
	copy(**vars(args))
