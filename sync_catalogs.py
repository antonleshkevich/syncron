#!/usr/bin/python3

import os
import sys
import shutil

def reportdiffs(unique1, unique2, dir1, dir2):
	if not (unique1 or unique2):
		print('Directory list are idential')
	else:			
		if unique1:
			print('Files unique to', dir1)
			for file in unique1:
				temp = file
				file = (dir1 + '/' + file)
				if os.path.isdir(file):	
					res = (dir2 + '/' + temp)
					try:
						os.makedirs(res)
					except OSError:
						pass
				else:
					shutil.copy(file, dir2)
					print("!", file, dir2)
			for file in unique1:
				print('...', file)
		if unique2:
			for file in unique2:
				temp = file
				file = (dir2 + '/' + file)
				if os.path.isdir(file):
					shutil.rmtree(file)
				else:
					os.remove(file)

def difference(seq1, seq2):
	return [item for item in seq1 if item not in seq2]

def comparedirs(dir1, dir2, files1=None, files2=None):
	print('Comparing', dir1, 'to', dir2)
	files1 = os.listdir(dir1) if files1 is None else files1
	files2 = os.listdir(dir2) if files2 is None else files2
	unique1 = difference(files1, files2)
	unique2 = difference(files2, files1)
	reportdiffs(unique1, unique2, dir1, dir2)
	return not (unique1 or unique2)

def getargs():
	try:
		dir1, dir2, pid = sys.argv[1: ]
	except:
		print('Usage: dirdiff.py dir1 dir2')
		sys.exit(1)
	else:
		return (dir1, dir2, pid)

if __name__ == '__main__':
	dir1, dir2 = getargs()
	comparedirs(dir1, dir2)	