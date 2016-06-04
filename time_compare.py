#!/usr/bin/python3

import os
import time

def timecompare(dir1, dir2):
	res1 = os.popen("find {0} -printf '%TY-%Tm-%Td %TT\n' | sort -r".format(dir1)).readlines()
	res2 = os.popen("find {0} -printf '%TY-%Tm-%Td %TT\n' | sort -r".format(dir2)).readlines()
	dt1 = time.strptime(res1[0][0:-12], "%Y-%m-%d %H:%M:%S")
	dt2 = time.strptime(res2[0][0:-12], "%Y-%m-%d %H:%M:%S")
	return (dt1 > dt2)

if __name__ == '__main__':
	print(timecompare('/home/anton/a', '/home/anton/b' ))