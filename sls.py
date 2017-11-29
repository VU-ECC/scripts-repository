#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, re
import numpy as np
import subprocess
from datetime import datetime
from optparse import OptionParser
sys.dont_write_bytecode = True

instruction = \
 """This scripts library search (sls) script allows you to recursively search 
 the scripts directory tree for specific keywords. 
 Usage: sls.py < --option > < keywords >

 keywords: keywords to be searched

 option: one or more of the following options, 
       keyword: If set to true keywords are only searched the dedicated 
                keyword field in the scripts header (default is False, 
                meaning that the entire script is searched) 

          path: The top level of the (recursive) search path relative to the 
                location of this script (default is ".", the directory where 
                sls is in) 

         usage: Filter for how often a script is typically used by the person 
                who wrote it (0 = seldom to 10 = frequent). The number is used as 
                a low threshold of search results that are returned (default is 0, 
                which means no filtering on usage) 

          help: print out this documentation and quit."""

parser = OptionParser(add_help_option=False)
parser.add_option('-k','--keyword', action="store_true", dest='keyword', default=False)
parser.add_option('-p','--path', dest='toplev_path', default='.')
parser.add_option('-u','--usage', dest='usage', default=0)
parser.add_option('-h','--help', action="store_true", dest='help', default=False)
(options, args) = parser.parse_args()

# help
if options.help:
   print instruction
   sys.exit()

# log file
logfile = open('dont_remove_me.log', 'a+') 
now = datetime.now()
timestamp='{0:04d}-{1:02d}-{2:02d}'.format(now.year,now.month,now.day)

# set keywords
skeys=args
if options.keyword:
   skeys.append('\#keyword')

# search keywords
for root, dirs, files in os.walk(options.toplev_path):
   for file in files:
      fname=os.path.join(root,file)
      fid = open(fname,'r')
      lines = fid.readlines()

      grep_out=[]
      for ll in lines:
         if all(re.search(s,ll) for s in skeys):
            grep_out = grep_out + [ll]

      if int(options.usage) > 0:
         use_output=[] 
         for cline in grep_out:
            ll = cline.split()
            ll = np.array(map(str.strip, ll))
            if len(ll) > 0:
               ppos = np.where(ll == '#usage') 
               iusage = 0
               if len(ppos[0]) > 0: 
                  cusage = ll[ppos[0]+1]
                  iusage = int(cusage[0])
               if iusage >= int(options.usage): 
                  use_output.append(cline)
            
      else:
         use_output = grep_out

      if len(use_output) > 0: 
         for ll in use_output:
            if len(ll) > 0:
               print fname+': '+ll
               logfile.write(timestamp+': '+fname+'\n')

# close log file
logfile.close()

