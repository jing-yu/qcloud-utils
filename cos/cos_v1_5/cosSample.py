#coding=utf-8
'''
Created on 2013-4-28

@author: mucdullge
'''
import time
import copy
from cosAPI import COSAPI
from cosUtil import *
from multiprocessing import Pool
        
host="cosapi.myqcloud.com"
accessId="1000231"
accessKey="ioQUE8B4M9N6Vho/0LSRI+eh"
secretId="AKIDVILqkf83C0DslAhWT4szfGAgVcIPfV0J"
 
cos = COSAPI(host,accessId,accessKey,secretId)
cos.setLogPath(".")

def mkdirDemo():
    params = {}
    params.update({"bucketId":"op"})
    params.update({"path":"哈哈"})
    
    starttime = time.time()
    requestString = cos.mkdir(params)
    difftime = time.time() - starttime
    
    print("mkdir use time :%f  request string :%s " % (difftime ,requestString))

    
def rmdirDemo():
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"path":"哈哈"})
    
    starttime = time.time()
    
    requestString = cos.rmdir(params)
    
    difftime = time.time() - starttime
    
    print("rmdir use time : %f  request string :%s " % (difftime, requestString))
    
def getmetaDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    #params.update({"path":"哈哈"})
    params.update({"path":"/bigfile.zip"})
    
    starttime = time.time()
    requestString = cos.getMeta(params)
    
    difftime = time.time() - starttime
    print("getmeta use time : %f  request string :%s " % (difftime, requestString))
    
def setmetaDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"path":"哈哈"})
    params.update({"expires":223})
    params.update({"cacheControl":"max-age=23"})
    
    starttime = time.time()
    requestString = cos.setMeta(params)
    
    difftime = time.time() - starttime
    print("setmeta use time : %f  request string :%s " % (difftime, requestString))
    
def listFileDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"path":"/"})
    
    starttime = time.time()
    
    requestString = cos.listFile(params)
    
    difftime = time.time() - starttime
    print("listFile use time : %f  request string :%s " % (difftime, requestString))
    
def deleteFileDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"path":"/"})
    params.update({"deleteObj":"test.zip"})
    #params.update({"deleteObj":"cc.txt|a.jpg|b.jpg"})
    starttime = time.time()
    requestString = cos.deleteFile(params)
    
    difftime = time.time() - starttime
    print("deleteFile use time : %f  request string :%s " % (difftime, requestString))

def renameDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"spath":"/aa2.txt"})
    params.update({"dpath":"/cc.txt"})
    
    starttime = time.time()
    requestString = cos.rename(params)
    
    difftime = time.time() - starttime
    print("rename use time : %f  request string :%s " % (difftime, requestString))

def createBucketDemo():
    
    params = {}
    
    params.update({"bucketId":"del"})
    
    starttime = time.time()
    requestString = cos.createBucket(params)
    
    difftime = time.time() - starttime
    print("createBucket use time : %f  request string :%s " % (difftime, requestString))

def deleteBucketDemo():
    
    params = {}
    
    params.update({"bucketId":"del"})
    
    starttime = time.time()
    requestString = cos.deleteBucket(params)
    
    difftime = time.time() - starttime
    print("deleteBucket use time : %f  request string :%s " % (difftime, requestString))
    
def getBucketDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    
    starttime = time.time()
    requestString = cos.getBucket(params)
    
    difftime = time.time() - starttime
    print("getBucket use time : %f  request string :%s " % (difftime, requestString))
    
def setBucketDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"acl":"0"})
    params.update({"referer":"*.qq.com"})
    
    starttime = time.time()
    requestString = cos.setBucket(params)
    
    difftime = time.time() - starttime
    print("setBucket use time : %f  request string :%s " % (difftime, requestString))
    
def listBucketDemo():
    
    params = {}
    
    starttime= time.time()
    requestString = cos.listBucket(params)
    
    difftime = time.time() - starttime
    print("listBucket use time : %f  request string :%s " % (difftime, requestString))
    

def uploadFileDemo():
    
    params = {}
    
    starttime = time.time()
    
    params.update({"bucketId":"op"})
    params.update({"path":"/"})
    params.update({"cosFile":"aa2.txt"})
    params.update({"localFilePath":"/aa.txt"})
    
    requestString = cos.uploadFile(params)
    
    print(requestString)
    
    
def downFileDemo():
    
    params = {}
    
    params.update({"bucketId":"op"})
    params.update({"path":"aa2.txt"})
    
    requestString = cos.makeDownFileUrl(params)
    
    print(requestString)


def getUploadFileUrl():
    
    params={}
    
    params.update({"bucketId":"bucket_test"})
    params.update({"path":"/"})
    params.update({"cosFile":"aa1.txt"})
    
    requestString = cos.makeUploadFileUrl(params)
    
    print(requestString)
    
    
def compressFileUpload():
    
    params={}
    
    params.update({"compressBucketId":"op"})
    params.update({"compressFilePath":"/a.jpg"})
    params.update({"uploadBucketId":"op"})
    params.update({"uploadFilePath":"/b.jpg"})
    params.update({"WMText":"大大松"})
    params.update({"WMFontType":"仿宋"})
    
    params.update({"zoomType":"2"})
    params.update({"height":"200"})
    params.update({"width":"200"})

    params.update({"localFilePath":"/test.jpg"})
    
    requestString = cos.uploadFileWithCompress(params)
    
    print(requestString)
    
def UploadFileFromOffset(block):
    requestString = cos.multipartUpload(block["params"], block["content"])
    return requestString

def multipartUpload():
    params = {}
    
    starttime = time.time()
    
    params.update({"bucketId":"op"})
    params.update({"path":"/"})
    params.update({"cosFile":"bigfile.zip"})
    
    target_file = "/bigfile.zip"
    per_size = 1 * 1024 * 1024
    offset = 0
    pool = Pool(4)
    block = []
    with open(target_file, 'rb') as f:
        while True:
            content = f.read(per_size)
            if sys.version_info >= (3, 0): 
                if content == b'':
                    break;
            else:
                if content == '':
                    break;

            params.update({"offset":offset})
            #requestString = cos.multipartUpload(params, content)
            #print(requestString)
            para = {}
            para["params"] = copy.copy(params)
            para["content"] = copy.copy(content)
            block.append(para)
            offset += len(content)
    
    res = pool.map(UploadFileFromOffset, block)
    pool.close()
    pool.join()
    print res

    params_complete = {}
    params_complete.update({"bucketId":"op"})
    params_complete.update({"path":"/bigfile.zip"})
    requestString = cos.completeMultipartUpload(params_complete)
    print(requestString)
    
deleteFileDemo()
mkdirDemo()
rmdirDemo()
mkdirDemo()
setmetaDemo()
getmetaDemo()
listFileDemo()
createBucketDemo()
setBucketDemo()
getBucketDemo()
uploadFileDemo()
listBucketDemo()
deleteBucketDemo()
downFileDemo()
compressFileUpload()
getUploadFileUrl()
renameDemo()
deleteFileDemo()
multipartUpload()
