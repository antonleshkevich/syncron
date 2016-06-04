#!/usr/bin/python3

import os
import sync_catalogs
import time_compare
import shutil
BLOCKSIZE = 1024*1024
pid = ''

def intersect(seq1, seq2):
	return [item for item in seq1 if item in seq2]

def comparetrees(dir1, dir2, diffs, verbose=False):
	print('----------------------------')
	names1 = os.listdir(dir1)
	names2 = os.listdir(dir2)
	if not sync_catalogs.comparedirs(dir1, dir2, names1, names2):
		diffs.append('unique files at %s - %s ' % (dir1, dir2))
	print('Comparing contents...')
	common = intersect(names1, names2)
	missed = common[ : ]

	for name in common:
		path1 = os.path.join(dir1, name)
		path2 = os.path.join(dir2, name)
		if os.path.isfile(path1) and os.path.isfile(path2):
			missed.remove(name)
			file1 = open(path1, 'rb')
			file2 = open(path2, 'rb')
			while True:
				bytes1 = file1.read(BLOCKSIZE)
				bytes2 = file2.read(BLOCKSIZE)
				if (not bytes1) and (not bytes2):
					if verbose:
						print(name, 'mathes')
					break
				if bytes1 != bytes2:
					shutil.copy2(path1, dir2)
					diffs.append('file differ at %s - %s' % (path1, path2))
					print(name, 'DIFFERS')
					break
	for name in common:
		path1 = os.path.join(dir1, name)
		path2 = os.path.join(dir2, name)
		if os.path.isdir(path1) and os.path.isdir(path2):
			missed.remove(name)
			comparetrees(path1, path2, diffs, verbose)
	for name in missed:
		diffs.append('file missed at %s - %s: %s' % (dir1, dir2, name))
		print(name, 'DIFFERS')


def action(): #dir2 - buffer
	global pid
	dir1, dir2, pid = sync_catalogs.getargs()
	diffs = []
	count = 0
	if time_compare.timecompare(dir1, dir2) == True:
		comparetrees(dir1, dir2, diffs, True)
		count = 1
	else:
		comparetrees(dir2, dir1, diffs, True)
		count = 2		
	print('='*40)
	while True:
		if not diffs:
			print('No diffs found')
			break
		else:
			print('Diffs found:', len(diffs))
			for diff in diffs:
				print('-', diff)
			diffs = []
			if count == 1:
				comparetrees(dir1, dir2, diffs, True)
			else:
				comparetrees(dir2, dir1, diffs, True)

def getpid():
	global pid
	dir1, dir2, pid = sync_catalogs.getargs()
	return pid
