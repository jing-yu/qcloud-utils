#!/usr/bin/python

import json
import sys

from settings import *
from cos_v1_5.cosAPI import COSAPI

COS_FILE_TYPE_FILE = 1
COS_FILE_TYPE_DIR  = 2

COS_ROOT_DIR = '/'

Cos = COSAPI(Host, AccessId, SecretKey, SecretId)

def list_bucket_files(bucket_id, path, offset=0, page=100, prefix=None):
    global Cos
    params = {'bucketId': bucket_id, 'offset': offset, 'count': page, 'path': path}
    if prefix:
        params['prefix'] = prefix

    data = Cos.listFile(params)
    #print data
    files = json.loads(data)['data']['files']

    file_list =[]
    dir_list =[]
    if files:
        for i in files:
            if i['type'] == COS_FILE_TYPE_FILE:
                file_list.append(i['name'])
            elif i['type'] == COS_FILE_TYPE_DIR:
                dir_list.append(i['name'])
    return file_list, dir_list

def delete_file(bucket_id, path, file_list):
    global Cos
    params = {'bucketId': bucket_id, 'path': path, 'deleteObj': '|'.join(file_list)}
    data = Cos.deleteFile(params)
    #print data
    data = json.loads(data)
    return data['code']

def delete_dir(bucket_id, path):
    global Cos
    params = {'bucketId': bucket_id, 'path': path}
    #print params
    data = Cos.rmdir(params)
    #print data
    data = json.loads(data)
    return data['code']


def delete_files_with_prefix(bucket_id, curr_dir, prefix, page=10):
    deleted = 0
    while True:
        files, dirs = list_bucket_files(bucket_id, curr_dir, prefix=prefix, page=page)
        if len(files) > 0:
            if delete_file(bucket_id, curr_dir, files) == 0:
                deleted += len(files)

        for i in dirs:
            if curr_dir[-1] == '/':
                deleted += delete_files_with_prefix(bucket_id, curr_dir + i, prefix, page=page)
            else:
                deleted += delete_files_with_prefix(bucket_id, curr_dir + '/' + i, prefix, page=page)

        if len(files) + len(dirs) == 0:
            delete_dir(bucket_id, curr_dir)
            break

    return deleted

def delete_dirs_with_prefix(bucket_id, curr_dir, prefix, page=10):
    while True:
        _, dirs = list_bucket_files(bucket_id, curr_dir, prefix=prefix, page=page)
        print dirs 
        if len(dirs) > 0:
            for i in dirs:
                if curr_dir[-1] == '/':
                    delete_dirs_with_prefix(bucket_id, curr_dir + i, preifx, page=page)
                else:
                    delete_dirs_with_prefix(bucket_id, curr_dir + '/' + i, preifx, page=page)
        else:
            delete_dir(bucket_id, curr_dir)
            return
 
if __name__ == '__main__':
    bucket_id = sys.argv[1]
    #import pdb;pdb.set_trace()
    print 'FILE:', ' - ', delete_files_with_prefix(bucket_id, COS_ROOT_DIR, None, page=20)
    print 'DIR :', ' - ', delete_dirs_with_prefix(bucket_id, COS_ROOT_DIR, None, page=20)

