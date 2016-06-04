#!/usr/bin/python3

from minio import Minio
from minio.error import ResponseError
import argparse,os
import time_compare

parser=argparse.ArgumentParser()
parser.add_argument('path',type=str,help='You programm track')
parser.add_argument('quit',type=str,help='Exit key')
parser.add_argument('--s3',type=str,help='Your host')
parser.add_argument('--access_key',type=str,help='Your access key')
parser.add_argument('--secret_key',type=str,help='Your secret key')
parser.add_argument('--dir',type=str,help='Folder directory')
args=parser.parse_args()
# Initialize minioClient with an endpoint and access/secret keys.
#print("s3:{0},access:{1},secret:{2},dir:{3}".format(args.s3,args.access_key,args.secret_key,args.dir))
minioClient = Minio(args.s3,access_key=args.access_key,secret_key=args.secret_key,secure=False)

print('-'*40)

def all_objects(bucket):
    objects = minioClient.list_objects(bucket, prefix='',recursive=True)
    return objects

def load_object(bucket,obj):
	try:
		minioClient.fget_object(bucket,obj, args.dir+'/'+obj)
	except ResponseError as err:
		print(err)

def upload_object(bucket,obj):
	try:
		file_stat = os.stat(obj)
		file_data = open(obj, 'rb')
		minioClient.put_object(bucket,obj , file_data, file_stat.st_size)
	except ResponseError as err:
		print(err)
"""
# Put a file with 'application/csv'.
	try:
		file_stat = os.stat('my-testfile.csv')
		file_data = open('my-testfile.csv', 'rb')
		minioClient.put_object('sync', 'huggo', file_data,file_stat.st_size, content_type='application/csv')
	except ResponseError as err:
		print(err)
"""

def get_hash(bucket,obj): 
	try:
		res=minioClient.stat_object(bucket, obj)
		return res
	except ResponseError as err:
		print(err)

def remove_object(bucket,obj):
	try:
		minioClient.remove_object(bucket, obj)
	except ResponseError as err:
		print(err)

def remove_bucket(bucket):
	try:
		minioClient.remove_bucket(bucket)
	except ResponseError as err:
		print(err)

def check_bucket(bucket):
	try:
		print(minioClient.bucket_exists(bucket))
	except ResponseError as err:
		print(err)

def all_buckets():
	buckets = minioClient.list_buckets()
	return buckets

def create_bucket(bucket):
	try:
		minioClient.make_bucket(bucket, location="us-east-1")
	except ResponseError as err:
		print(err)

if __name__=='__main__':
	buckets=all_buckets()
	for bucket in buckets:
		print(bucket.name, bucket.creation_date)
		res=all_objects(bucket.name)
		for obj in res:
			print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,obj.etag, obj.size, obj.content_type)
	res1=get_hash('sync','yum')
	res2=get_hash('yummi','yum')
	if (res1.size==res2.size) and (res1.etag==res2.etag) and (res1.content_type==res2.content_type):
		print('Yes')
	else:
		print('No')

