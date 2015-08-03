# -*- coding: utf-8 -*- 
'''
Created on 2013-4-27

@author: mucdullge
'''

import sys
if sys.version_info >= (3, 0):
    import http.client
    import urllib.request, urllib.parse, urllib.error
    import io	
else:
    import urllib
    import StringIO
    import httplib
	
import time
import base64
import json
import os

sys.path.insert(0,os.path.dirname(__file__))
from cosUtil import *
from cosConst import *




class COSAPI:
    
    DefaultContentType = 'application/octet-stream'
    
    def __init__(self, host, access_id, access_key='',secretId='', port=80):
        '''

        :type host: string       
        :param host: 服务器域名，根据运行环境设置内网或外网域名

        :type access_id: int       
        :param access_id: 开发商访问本服务的资源标识
        
        :type access_key: string       
        :param access_key: 访问Key, 用户用于签名的密钥。注册时返回，也可以在管理端查询

        :type port: int    
        :param port: 服务器端口
        '''
        if host is None:
            host = COSCONST.HTTPHOST
        if host is "":
            host = COSCONST.HTTPHOST
        
        self.host = host
        self.access_id = access_id
        self.access_key = access_key
        self.secretId = secretId
        self.port = port
        
    def setLogPath(self,path=''):
        global LOGGER
        LOGGER=initlog(LOG_LEVEL,path)
        
    def get_connection(self):
        '''
        :获取http连接
                
        '''
        host = ''
        port = self.port
        timeout = 300
        host_port_list = self.host.split(":")
        
        if len(host_port_list) == 1:
            host = host_port_list[0].strip()
        elif len(host_port_list) == 2:
            host = host_port_list[0].strip()
            port = int(host_port_list[1].strip())
        
        if port is None:
            port = 80
        if port is 0 :
            port = 80
        
        if sys.version_info >= (3, 0):
            return http.client.HTTPConnection(host=host, port=port, timeout=timeout)
        elif sys.version_info >= (2, 6):
            return httplib.HTTPConnection(host=host, port=port, timeout=timeout)
        else :
            return httplib.HTTPConnection(host=host, port=port)
        
    def http_request(self,method ,url, headers=None, body=''):
        '''
        http 请求并获取结果值
        :param method: http请求方式，例如GET或者为POST\PUT
        :param url:  http请求url
        :param headers: http请求的头设置结构（可以为空）
        :param body: body为http请求的数据(可以为空，在此场景中一般为文件内容)
        '''
        responsJson = ""
        if not headers:
           headers = {}
        #if isinstance(url , unicode):
        #url = url.encode('utf-8')

        headers['Host'] = self.host
        conn = self.get_connection()

        conn.request(method, url, body, headers)
        response = conn.getresponse()
        
        if response.status == 200:
            responsJson = response.read()
        conn.close()
        return responsJson
    
    
    def get_optional_param_for_bucket(self, in_params, out_params):
        '''
                 从传入的参数中提取设置bucket信息的可选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        if "acl" in in_params:
            out_params.update({"acl":in_params["acl"]})
        
        if "referer" in in_params:
            out_params.update({"referer":in_params["referer"]})
    
    
    def get_optional_param_for_list(self, in_params, out_params):
        '''
                 从传入的参数中提取list操作的可选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        if "offset" in in_params:
            offsetIn=in_params["offset"]
            offset_str="%d" % offsetIn  
            out_params.update({"offset":offset_str})
        
        if "count" in in_params:
            countIn=in_params["count"]
            count_str="%d" % countIn
            out_params.update({"count":count_str})
        
        if "prefix" in in_params:
            prefixIn=in_params["prefix"]
            prefix_str= prefixIn
            out_params.update({"prefix":prefix_str})
            

    def get_optional_param_for_dir(self, in_params, out_params):
        '''
                 从传入的参数中提取设置dir信息的可选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        if "expires" in in_params:
            expiresIn=in_params["expires"]
            expires_str="%d" % (expiresIn)
            out_params.update({"expires":expires_str})
        
        if "cacheControl" in in_params:
            out_params.update({"cacheControl":in_params["cacheControl"]})
        
        if "prefix" in in_params:
            out_params.update({"contentEncoding":in_params["contentEncoding"]})
            
        if "contentEncoding" in in_params:
            out_params.update({"contentEncoding":in_params["contentEncoding"]})
            
        if "contentDisposition" in in_params:
            out_params.update({"contentDisposition":in_params["contentDisposition"]})
        
        if "contentLanguage" in in_params:
            out_params.update({"contentLanguage":in_params["contentLanguage"]})
        
        if "mkType" in in_params:
            out_params.update({"mkType":in_params["mkType"]})
              

    def get_optional_param_for_compress(self, in_params, out_params):
        '''
                 从传入的参数中提取compress操作的可选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        if "uploadBucketId" in in_params:
            out_params.update({"uploadBucketId":in_params["uploadBucketId"]})
        
        if "uploadFilePath" in in_params:
            uploadFilePath = in_params["uploadFilePath"]
            if uploadFilePath[0:1] != "/":
                uploadFilePath = "/" + uploadFilePath
            out_params.update({"uploadFilePath":uploadFilePath})
        
        if "zoomType" in in_params:
            out_params.update({"zoomType":in_params["zoomType"]})
        
        if "width" in in_params:
            out_params.update({"width":in_params["width"]})
        
        if "height" in in_params:
            out_params.update({"height":in_params["height"]})
            
        if "compress" in in_params:
            out_params.update({"compress":in_params["compress"]})
        
        if "WMText" in in_params:
            out_params.update({"WMText":in_params["WMText"]})
        
        if "WMAlign" in in_params:
            out_params.update({"WMAlign":in_params["WMAlign"]})
        
        if "WMOffsetX" in in_params:
            out_params.update({"WMOffsetX":in_params["WMOffsetX"]})
        
        if "WMOffsetY" in in_params:
            out_params.update({"WMOffsetY":in_params["WMOffsetY"]})
            
        if "WMColor" in in_params:
            out_params.update({"WMColor":in_params["WMColor"]})
        
        if "WMFontType" in in_params:
            out_params.update({"WMFontType":in_params["WMFontType"]})
        
        if "WMFontSize" in in_params:
            out_params.update({"WMFontSize":in_params["WMFontSize"]})
        
        if "WMDegree" in in_params:
            out_params.update({"WMDegree":in_params["WMDegree"]})
    
    def get_partial_required_param(self, in_params, out_params):
        '''
                 从传入的参数中提取bucketId 和path 这两个必选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        ret = {}
        if "bucketId" not in in_params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "path" not in in_params:
            ret.update({"code":-29491})
            ret.update({"msg":"path is null"})
            return json.dumps(ret, sort_keys=True)
        
        out_params.update({"bucketId":in_params["bucketId"]})
        out_params.update({"path":in_params["path"]})
        return ""
    
    
    def get_partial_required_param_for_compress(self, in_params, out_params):
        '''
                 从传入的参数中提取compressBucketId 和compressFilePath 这两个必选参数
          
        :type in_params: dict       
        :param in_params: 输入参数
        
        :type out_params: dict       
        :param out_params: 输出参数
        ''' 
        ret = {}
        if "compressBucketId" not in in_params:
            ret.update({"code":-29494})
            ret.update({"msg":"compressBucketId is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "compressFilePath" not in in_params:
            ret.update({"code":-29491})
            ret.update({"msg":"compressFilePath is null"})
            return json.dumps(ret, sort_keys=True)
        
        out_params.update({"compressBucketId":in_params["compressBucketId"]})
        compressFilePath = in_params["compressFilePath"]
        if compressFilePath[0:1] != "/":
            compressFilePath = "/" + compressFilePath
        out_params.update({"compressFilePath":compressFilePath})
        return ""
        
        

    def get_http_data(self, params, method_name):
        '''
               以get方式向服务器发送请求

        :type params: dict       
        :param params: 用户访问api时的一些输入参数

        :type method_name: string       
        :param method_name: 调用的api，如：/api/cos_mkdir
        
        Returns:
            json string.
        ''' 
        access_id = self.access_id
        access_key = self.access_key
        secret_id = self.secretId
        host = self.host
        
        params.update({COSCONST.COS_ACCESSID:access_id})
        
        if secret_id is not "":
            params.update({COSCONST.COS_SECRETID:secret_id})
        
        nowTiemstampe = time.time()        
        params.update({COSCONST.COS_TIME:formatTime(str(nowTiemstampe))})
        
        sign = makeSign(params, method_name, access_key)               
        
        params.update({"sign":sign})
        
        url = makeUrl(params, host, method_name)

        response = self.http_request("GET", url)
        if sys.version_info >= (3, 0):
            return response.decode('utf-8')
        else:
            return response
    
    def post_http_data(self, parmas, method_name, fd, contentType):
        '''
                以post方式向服务器发送请求

        :type params: dict       
        :param params: 用户访问api时的一些输入参数

        :type method_name: string       
        :param method_name: 调用的api，如：/api/cos_mkdir

        :type fd: obj       
        :param fd: 本地文件句柄
        
        :type contentType: string       
        :param contentType: 文件类型，如"text/html"
                
        Returns:
            json string.
        '''         
        access_id = self.access_id
        access_key = self.access_key
        secret_id = self.secretId
        host = self.host
        
        parmas.update({COSCONST.COS_ACCESSID:access_id})
        
        if secret_id is not "":
            parmas.update({COSCONST.COS_SECRETID:secret_id})
        
        nowTiemstampe = time.time()        
        parmas.update({COSCONST.COS_TIME:formatTime(str(nowTiemstampe))})
        
        sign = makeSign(parmas, method_name, access_key)              
        parmas.update({"sign":sign})
        
        url = makeUrl(parmas, host, method_name)
        
        
        fd.seek(os.SEEK_SET, os.SEEK_END)
        
        filesize = fd.tell()
        fd.seek(os.SEEK_SET)
        
        httpheaders = {}
        httpheaders["Content-Type"] = contentType
        httpheaders["Content-Length"] = str(filesize)
        try:
            httpbody = fd.read(filesize)
        finally:
            fd.close()
            
        response = self.http_request("POST", url, httpheaders, httpbody)
        
        if sys.version_info >= (3, 0):
            return response.decode('utf-8')
        else:
            return response
    
    def check_local_file(self, local_file_path):
        '''
                 检查本地文件是否能够读取，并检查是否超过单次上传文件的最大值
        
        :type local_file_path: string
        :     local_file_path 本地文件全路径

        Returns:
            json string.
        '''  
        ret = {}

        if False == os.path.exists(local_file_path):
            ret.update({"code":-29489})
            ret.update({"msg":"local file is not exist"})
            return json.dumps(ret, sort_keys=True)
        
        if False == os.path.isfile(local_file_path):
            ret.update({"code":-29489})
            ret.update({"msg":"localFilePath is not file type"})
            return json.dumps(ret, sort_keys=True)

        file_length = os.path.getsize(local_file_path)
        if (file_length > COSCONST.FILE_MAX_LENGTH):
            ret.update({"code":-24968})
            ret.update({"msg":"invalid file size, file is too large"})
            return json.dumps(ret, sort_keys=True)
        
        return ""
            
               

    def mkdir(self,params):
        '''
                    创建目录
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        : type expires : int
        :      expires （可选,默认为空）例如：7200.该目录下的”直接”文件(一级文件)，下载时的Expires头

        : type cacheControl : string
        :      cacheControl（可选，默认为空） 例如：max-age=200 .文件被下载时的cache-control头
        
        : type contentEncoding : string
        :      contentEncoding（可选，默认为空）例如：utf-8 .文件被下载时的Content-Encoding头
        
        : type contentDisposition : string
        :      contentDisposition（可选，默认为空）例如：utf-8 .文件被下载时的Content-Disposition头
        
        : type contentLanguage : string
        :      contentLanguage（可选，默认为空） 例如：zh .文件被下载时的contentLanguage头    
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_dir(params, params_dict)
        
        return self.get_http_data(params_dict, COSCONST.MKDIR_URL)

    
    def rmdir(self,params):
        '''
                    删除目录
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str 
        
        return self.get_http_data(params_dict, COSCONST.RMDIR_URL)        

        
        
    def getMeta(self,params):
        '''
                    获取目录属性
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        return self.get_http_data(params_dict, COSCONST.GETMETA_URL)
    
    
    def setMeta(self,params):
        '''
                    设置目录属性
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        : type expires : int
        :      expires （可选,默认为空）例如：7200.该目录下的”直接”文件(一级文件)，下载时的Expires头

        : type cacheControl : string
        :      cacheControl（可选，默认为空） 例如：max-age=200 .文件被下载时的cache-control头
        
        : type contentEncoding : string
        :      contentEncoding（可选，默认为空）例如：utf-8 .文件被下载时的Content-Encoding头
        
        : type contentDisposition : string
        :      contentDisposition（可选，默认为空）例如：utf-8 .文件被下载时的Content-Disposition头
        
        : type contentLanguage : string
        :      contentLanguage（可选，默认为空） 例如：zh .文件被下载时的contentLanguage头    
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_dir(params, params_dict)
        
        return self.get_http_data(params_dict, COSCONST.SETMETA_URL)
    
    
    
    def listFile(self,params):
        '''
                    删除文件
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        : type offset : int
        :      offset （可选，默认为0）  大于等于0

        : type count : int
        :      count（可选，默认为100） 大于等于1，目前单次显示的最大个数为1000个
        
        : type prefix : string
        :      prefix（可选，默认为空） 匹配的前缀, 只允许传入长度小于等于255、字符（123456789 and A~Z and a~z  and _  - . ）
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_list(params, params_dict)
        
        return self.get_http_data(params_dict, COSCONST.LISTFILE_URL)
    
    
    def deleteFile(self,params):
        '''
                    删除文件
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        : type deleteObj : string
        :      deleteObj 需要删除的文件/空目录对象列表, deleteObj为用’|’隔开的obj列表. 
        :                每个文件名只允许传入长度小于等于255字符，不允许ascII字符(0-31,47,92, 127)；允许中文；
        
        Returns:
            json string.
        '''
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        ret = {}
        if "deleteObj" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"deleteObj is null"})
            return json.dumps(ret, sort_keys=True)        
        
        params_dict.update({"deleteObj":params["deleteObj"]})
        
        return self.get_http_data(params_dict, COSCONST.DELETEFILE_URL)
    
    def rename(self,params):
        '''
                    文件/文件夹重命名
        
        : type params : dict
        : param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type spath : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        : type dpath : string
        :      dpath dest路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        Returns:
            json string.
        '''
        ret = {}
        params_dict = {}
        
        if "bucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "spath" not in params:
            ret.update({"code":-29491})
            ret.update({"msg":"spath is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "dpath" not in params:
            ret.update({"code":-29491})
            ret.update({"msg":"dpath is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"bucketId":params["bucketId"]})
        params_dict.update({"spath":params["spath"]})
        params_dict.update({"dpath":params["dpath"]})
        
        return self.get_http_data(params_dict, COSCONST.RENAME_URL)
    
        
    def createBucket(self,params): 
        '''
                     创建 bucket
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        :type bucketId: string
        :     bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        :type acl: string
        :     acl     （可选，默认为0）  acl取值       0: bucket访问权限为私有读
                                                 1: bucket访问权限为公开读
        
        :type referer: string 
        :     referer （可选，默认为空） 允许访问 bucket的referer，允许访问 bucket的referer，如 "http://qq.com"
        
        Returns:
            json string.
        '''       
        ret = {}
        params_dict = {}
        
        if "bucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"bucketId":params["bucketId"]})
        self.get_optional_param_for_bucket(params, params_dict)
        
        return self.get_http_data(params_dict, COSCONST.CREATEBUCKET_URL)
    
        
    def deleteBucket(self,params):
        '''
                 删除 bucket
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        :type bucketId: string
        :     bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
               
        Returns:
            json string.
        ''' 
        ret = {}
        params_dict = {}
        
        if "bucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"bucketId":params["bucketId"]})
        
        return self.get_http_data(params_dict, COSCONST.DELETEBUCKET_URL)
 
    
    def setBucket(self,params):
        '''
                 设置 bucket meta信息
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        :type bucketId: string
        :     bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        :type acl: string
        :     acl     （可选，默认为0）  acl取值       0: bucket访问权限为私有读
                                                 1: bucket访问权限为公开读
        
        :type referer: string 
        :     referer （可选，默认为空） 允许访问 bucket的referer，允许访问 bucket的referer，如 "http://qq.com"
        
        Returns:
            json string.
        ''' 
        ret = {}
        params_dict = {}
        
        if "bucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"bucketId":params["bucketId"]})
        self.get_optional_param_for_bucket(params, params_dict)
        return self.get_http_data(params_dict, COSCONST.SETBUCKET_URL)
    
    def getBucket(self,params):
        '''
                 获取 bucket meta信息
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        :type bucketId: string
        :     bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        Returns:
            json string.
        ''' 
        ret = {}
        params_dict = {}
        
        if "bucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"bukcetId is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"bucketId":params["bucketId"]})
        
        return self.get_http_data(params_dict, COSCONST.GETBUCKET_URL)

        
    def listBucket(self,params):
        '''
                     获取 bucket 列表
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        :type offset: int
        :     offset (可选，默认为0）  大于等于0
        
        :type count: int
        :     count  可选，默认为100） 大于等于1，目前单次显示的最大个数为1000个
        
        :type prefix: string 
        :     prefix （可选，默认为空） 匹配的前缀, 只允许传入长度小于等于255、字符（123456789 and A~Z and a~z  and _  - . ）
        
        Returns:
            json string.
        '''
        params_dict = {}
        
        self.get_optional_param_for_list(params, params_dict)
        
        return self.get_http_data(params_dict, COSCONST.LISTBUCKET_URL)
    
    
    def uploadFile(self,params):
        '''
                    上传文件
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        :type cosFile: string 
        :     cosFile 存储到cos之后的对象名
        
        :type localFilePath: string 
        :     localFilePath 本地文件的路径
        
        Returns:
            json string.
        '''
        
        ret = {}
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str

        
        if "cosFile" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"cosFile is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"cosFile":params["cosFile"]})
        
        if "localFilePath" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"localFilePath is null"})
            return json.dumps(ret, sort_keys=True)        
        
        local_file_path = params["localFilePath"]
        json_str = self.check_local_file(local_file_path)
        if (0 != len(json_str)):
            return json_str        
        
        contentType = getFileType(local_file_path)
        fd = open(local_file_path,"rb")        
        
        response = self.post_http_data(params_dict, COSCONST.UPLOAD_URL, fd, contentType)
        
        if False == fd.closed:
            fd.close()
        
        return response
        
    def uploadFileByContent(self,params,content):
        '''
                    上传内容
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        :type cosFile: string 
        :     cosFile 存储到cos之后的对象名
        
        :type content: string 
        :param content : 为文件内容
        
        Returns:
            json string.
        '''        
        ret = {}
        params_dict = {}
        
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        if "cosFile" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"cosFile is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"cosFile":params["cosFile"]})
    
        contentType = "text/html"
        if sys.version_info >= (3, 0):
            fd = io.BytesIO(content)
        else:
            fd = StringIO.StringIO(content)
        
        response = self.post_http_data(params_dict, COSCONST.UPLOAD_URL, fd, contentType)
        
        if False == fd.closed:
            fd.close()
        
        return response
    
    def uploadFileWithCompressByFd(self,params,fd):
        '''
                     压缩上传文件
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type compressBucketId : string
        :      compressBucketId 压缩后文件存放的bucket, 长度<=64、字符（123456789 and A~Z and a~z and _-.）
        
        : type compressFilePath : string
        :      compressFilePath 压缩后文件的存放路径, 长度小于等于4096, 字符（123456789 and A~Z and a~z  
                            and _  - . /和utf8编码的中文), 以"/"开头
        
        :type localFilePath: string 
        :     localFilePath 本地文件的路径
        
        :type uploadBucketId: string 
        :     uploadBucketId 原始文件上传后存放的bucket（可选参数，如不保存源文件，则不传此参数）,
                                                                           长度<=64、字符（123456789 and A~Z and a~z  and _  - .）
        :type uploadFilePath: string 
        :     uploadFilePath 原始文件上传后存放的完整路径（可选参数，如不保存源文件，则不传此参数）长度小于等于4096、
                                                                字符（123456789 and A~Z and a~z  and _  - . / 和中文）, 以"/"开头
                                                                
         :type zoomType: string
        :     zoomType 0不缩放; 1等比缩放,不裁剪;2缩放裁剪
        
        :type width: string
              width 缩放后的宽度
        
        :type height: string
              height 缩放后的高度
        
        :type compress: string
              compress 1 or 0 是否需要压缩(质量为85),(默认值为1)
        
        :type WMText: string
              WMText 水印文字内容
        
        :type WMAlign: string
              WMAlign 1: 图片左上方; 2: 图片中上方;  3: 图片右上方;  4: 图片中间 齐左侧;  5: 图片正中;  6: 图片中间 齐右侧;  7: 图片左下方; 8: 图片中下方;  9: 图片右下方
        
        :type WMOffsetX: string
              WMOffsetX 水印的偏移像素值。 X轴  (向右为正)
        
        :type WMOffsetY: string
              WMOffsetY 水印的偏移像素值。 Y轴  (向下为正)
        
        :type WMColor:string
              WMColor 例如："#ff00007f",图片的RGBA值(“#RGBA”,红绿蓝+透明度)
        
        :type WMFontType:string
              WMFontType 水印字体类型. "仿宋";
        
        :type WMFontSize:string
              WMFontSize 水印文本字体大小
        
        :type WMDegree:string
              WMDegree 水印文本旋转角度，正数为顺时针旋转
              
        :type fd:文件流
        
        Returns:
            json string.
        '''
        ret = {}        
        params_dict = {}
        
        json_str = self.get_partial_required_param_for_compress(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_compress(params, params_dict)
        
        response = self.post_http_data(params_dict, COSCONST.UPLOAD_WITHCOMPRESS_URL, fd, contentType)
        
        return response
    
    def uploadFileWithCompress(self,params):
        '''
                     压缩上传文件
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type compressBucketId : string
        :      compressBucketId 压缩后文件存放的bucket, 长度<=64、字符（123456789 and A~Z and a~z and _-.）
        
        : type compressFilePath : string
        :      compressFilePath 压缩后文件的存放路径, 长度小于等于4096, 字符（123456789 and A~Z and a~z  
                            and _  - . /和utf8编码的中文), 以"/"开头
        
        :type localFilePath: string 
        :     localFilePath 本地文件的路径
        
        :type uploadBucketId: string 
        :     uploadBucketId 原始文件上传后存放的bucket（可选参数，如不保存源文件，则不传此参数）,
                                                                           长度<=64、字符（123456789 and A~Z and a~z  and _  - .）
        :type uploadFilePath: string 
        :     uploadFilePath 原始文件上传后存放的完整路径（可选参数，如不保存源文件，则不传此参数）长度小于等于4096、
                                                                字符（123456789 and A~Z and a~z  and _  - . / 和中文）, 以"/"开头
                                                                
         :type zoomType: string
        :     zoomType 0不缩放; 1等比缩放,不裁剪;2缩放裁剪
        
        :type width: string
              width 缩放后的宽度
        
        :type height: string
              height 缩放后的高度
        
        :type compress: string
              compress 1 or 0 是否需要压缩(质量为85),(默认值为1)
        
        :type WMText: string
              WMText 水印文字内容
        
        :type WMAlign: string
              WMAlign 1: 图片左上方; 2: 图片中上方;  3: 图片右上方;  4: 图片中间 齐左侧;  5: 图片正中;  6: 图片中间 齐右侧;  7: 图片左下方; 8: 图片中下方;  9: 图片右下方
        
        :type WMOffsetX: string
              WMOffsetX 水印的偏移像素值。 X轴  (向右为正)
        
        :type WMOffsetY: string
              WMOffsetY 水印的偏移像素值。 Y轴  (向下为正)
        
        :type WMColor:string
              WMColor 例如："#ff00007f",图片的RGBA值(“#RGBA”,红绿蓝+透明度)
        
        :type WMFontType:string
              WMFontType 水印字体类型. 仿宋;
        
        :type WMFontSize:string
              WMFontSize 水印文本字体大小
        
        :type WMDegree:string
              WMDegree 水印文本旋转角度，正数为顺时针旋转
        Returns:
            json string.
        '''
        ret = {}        
        params_dict = {}
        
        json_str = self.get_partial_required_param_for_compress(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_compress(params, params_dict)   
        
        if "localFilePath" not in params:
            ret.update({"code":-29491})
            ret.update({"msg":"localFilePath is null"})
            return json.dumps(ret, sort_keys=True) 
        
        local_file_path = params["localFilePath"]
        json_str = self.check_local_file(local_file_path)
        if (0 != len(json_str)):
            return json_str  
        
        contentType = getFileType(local_file_path)
        fd = open(local_file_path,"rb")
        
        response = self.post_http_data(params_dict, COSCONST.UPLOAD_WITHCOMPRESS_URL, fd, contentType)

        if False == fd.closed:
            fd.close()
        
        return response
        
    def uploadFileByContentWithCompress(self,params,content):
        '''
                    压缩上传内容
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type compressBucketId : string
        :      compressBucketId 压缩后文件存放的bucket, 长度<=64、字符（123456789 and A~Z and a~z and _-.）
        
        : type compressFilePath : string
        :      compressFilePath 压缩后文件的存放路径, 长度小于等于4096, 字符（123456789 and A~Z and a~z  
                            and _  - . /和utf8编码的中文), 以"/"开头
        
        :type uploadBucketId: string 
        :     uploadBucketId 原始文件上传后存放的bucket（可选参数，如不保存源文件，则不传此参数）,
                                                                           长度<=64、字符（123456789 and A~Z and a~z  and _  - .）
        :type uploadFilePath: string 
        :     uploadFilePath 原始文件上传后存放的完整路径（可选参数，如不保存源文件，则不传此参数）长度小于等于4096、
                                                                字符（123456789 and A~Z and a~z  and _  - . / 和中文）, 以"/"开头
                                                                
        :type params : string
        :param content : 文件内容
        
         :type zoomType: string
        :     zoomType 0不缩放; 1等比缩放,不裁剪;2缩放裁剪
        
        :type width: string
              width 缩放后的宽度
        
        :type height: string
              height 缩放后的高度
        
        :type compress: string
              compress 1 or 0 是否需要压缩(质量为85),(默认值为1)
        
        :type WMText: string
              WMText 水印文字内容
        
        :type WMAlign: string
              WMAlign 1: 图片左上方; 2: 图片中上方;  3: 图片右上方;  4: 图片中间 齐左侧;  5: 图片正中;  6: 图片中间 齐右侧;  7: 图片左下方; 8: 图片中下方;  9: 图片右下方
        
        :type WMOffsetX: string
              WMOffsetX 水印的偏移像素值。 X轴  (向右为正)
        
        :type WMOffsetY: string
              WMOffsetY 水印的偏移像素值。 Y轴  (向下为正)
        
        :type WMColor:string
              WMColor 例如："#ff00007f",图片的RGBA值(“#RGBA”,红绿蓝+透明度)
        
        :type WMFontType:string
              WMFontType 水印字体类型.仿宋;
        
        :type WMFontSize:string
              WMFontSize 水印文本字体大小
        
        :type WMDegree:string
              WMDegree 水印文本旋转角度，正数为顺时针旋转
              
        Returns:
            json string.
        '''
        ret = {}        
        params_dict = {}
        
        json_str = self.get_partial_required_param_for_compress(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        self.get_optional_param_for_compress(params, params_dict)
       
        contentType = "text/html"
        if sys.version_info >= (3, 0):
            fd = io.BytesIO(content)
        else:
            fd = StringIO.StringIO(content)
        
        response = self.post_http_data(params_dict, COSCONST.UPLOAD_WITHCOMPRESS_URL, fd, contentType)

        if False == fd.closed:
            fd.close()
        
        return response
        
        
    def compressOnlineFile(self,params):
        '''
                    在线压缩文件
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type srcBucketId : string
        :      srcBucketId 待压缩文件所在的bucket, 长度<=64、字符（123456789 and A~Z and a~z  and _  - .）
        
        : type dstBucketId : string
        :      dstBucketId 压缩后文件存放的bucket, 长度<=64、字符（123456789 and A~Z and a~z  and _  - .）
        
        :type srcFilePath: string 
        :     srcFilePath 待压缩文件所在路径, 长度小于等于4096, 字符（123456789 and A~Z and a~z  and _  - . / 
                                                         和中文), 以"/"开头
        :type dstFilePath: string 
        :     dstFilePath 压缩后文件的存放路径, 长度小于等于4096, 字符（123456789 and A~Z and a~z  and _  - . / 
                                                         和中文), 以"/"开头
        
         :type zoomType: string
        :     zoomType 0不缩放; 1等比缩放,不裁剪;2缩放裁剪
        
        :type width: string
              width 缩放后的宽度
        
        :type height: string
              height 缩放后的高度
        
        :type compress: string
              compress 1 or 0 是否需要压缩(质量为85),(默认值为1)
        
        :type WMText: string
              WMText 水印文字内容
        
        :type WMAlign: string
              WMAlign 1: 图片左上方; 2: 图片中上方;  3: 图片右上方;  4: 图片中间 齐左侧;  5: 图片正中;  6: 图片中间 齐右侧;  7: 图片左下方; 8: 图片中下方;  9: 图片右下方
        
        :type WMOffsetX: string
              WMOffsetX 水印的偏移像素值。 X轴  (向右为正)
        
        :type WMOffsetY: string
              WMOffsetY 水印的偏移像素值。 Y轴  (向下为正)
        
        :type WMColor:string
              WMColor 例如："#ff00007f",图片的RGBA值(“#RGBA”,红绿蓝+透明度)
        
        :type WMFontType:string
              WMFontType 水印字体类型. “仿宋”:仿宋;
        
        :type WMFontSize:string
              WMFontSize 水印文本字体大小
        
        :type WMDegree:string
              WMDegree 水印文本旋转角度，正数为顺时针旋转
                                                  
        Returns:
            json string.
        '''
        ret = {}        
        params_dict = {}
        
        if "srcBucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"srcBucketId is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "dstBucketId" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"dstBucketId is null"})
            return json.dumps(ret, sort_keys=True)
        
        
        if "srcFilePath" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"srcFilePath is null"})
            return json.dumps(ret, sort_keys=True)
        
        if "dstFilePath" not in params:
            ret.update({"code":-29494})
            ret.update({"msg":"dstFilePath is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"srcBucketId":params["srcBucketId"]})
        params_dict.update({"dstBucketId":params["dstBucketId"]})
        
        srcFilePath = params["srcFilePath"]
        if srcFilePath[0:1] != "/":
            srcFilePath = "/" + srcFilePath
        params_dict.update({"srcFilePath":srcFilePath})
        
        dstFilePath = params["dstFilePath"]
        if dstFilePath[0:1] != "/":
            dstFilePath = "/" + dstFilePath
        params_dict.update({"dstFilePath":dstFilePath})
        
        self.get_optional_param_for_compress(params, params_dict)      
        
        response = self.get_http_data(params_dict, COSCONST.COMPRESS_FILE_URL)
        
        return response
    
    def makeDownFileUrl(self,params):
      '''
                  获取下载文件url
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        
        Returns:
            json string.
      '''
      
      access_id = self.access_id
      access_key = self.access_key
      secret_id = self.secretId
      params_dict = {}
      json_str = self.get_partial_required_param(params, params_dict)
      if (0 != len(json_str)):
          return json_str
      
      path = params_dict["path"] 
      
      path = "/"+path
    
      path = path.replace("//","/");
      
      bucket_memo_str = self.getBucket(params_dict)
      jsonObj = json.loads(bucket_memo_str, "utf-8")
      
      code = jsonObj["code"]
      
      if code != 0:
           return bucket_memo_str
       
      acl = jsonObj["data"]["acl"]
      
      downUrl = COSCONST.DOWNHOST + "/" + self.access_id + "/"
      if sys.version_info >= (3, 0):
          downUrl = downUrl + params_dict["bucketId"] +  urllib.parse.quote(path) + "?"
      else:
          downUrl = downUrl + params_dict["bucketId"] +  urllib.quote(path) + "?"
      downUrl = downUrl + "res_content_disposition=attachement;"
      
      if secret_id is not "":
          downUrl = downUrl + "&secretId="+secret_id
    
      nowtime = formatTime(str(time.time()))
          
      downUrl = downUrl+"&time=" + nowtime
      
      downUrl = downUrl.replace("//","/")
      
      downUrl = "http://" + downUrl;
       
      if acl == 1:
          return downUrl
      
      if acl == 0:
          
          signParam = "accessId=" + access_id + "&bucketId=" + params_dict["bucketId"] + "&path=" + path
          signParam = signParam + "&res_content_disposition=attachement;"
          
          if secret_id is not "":
              signParam = signParam + "&secretId="+secret_id
              
          signParam = signParam + "&time=" + nowtime
          
          sign = makeDownSign(signParam, access_key)
          if sys.version_info >= (3, 0):
              downUrl = downUrl + "&sign=" + urllib.parse.quote(sign)
          else:
              downUrl = downUrl + "&sign=" + sign
          return downUrl
      
      
    def makeUploadFileUrl(self,params):
        '''
                    获取上传文件url
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        :type cosFile: string 
        :     cosFile 存储到cos之后的对象名
        
        Returns:
            json string.
        '''
        
        access_id = self.access_id
        access_key = self.access_key
        secret_id = self.secretId
        host = self.host
        method_name="/api/cos_upload"
        
          
        ret = {}
        params_dict = {}
        
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        if "cosFile" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"cosFile is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"cosFile":params["cosFile"]})
        
        

        params_dict.update({COSCONST.COS_ACCESSID:access_id})
        
        if secret_id is not "":
            params_dict.update({COSCONST.COS_SECRETID:secret_id})
        
        nowTiemstampe = time.time()        
        params_dict.update({COSCONST.COS_TIME:formatTime(str(nowTiemstampe))})
        
        sign = makeSign(params_dict, method_name, access_key)              
        params_dict.update({"sign":sign})
        
        url = makeUrl(params_dict, host, method_name)
        
        return url
        
    def multipartUpload(self, params, content):
        '''
                    分片上传
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath source路径。不允许ascII字符(0-31, 92, 127)；允许中文；
        
        :type cosFile: string 
        :     cosFile 存储到cos之后的对象名
        
        :type offset: int 
        :     offset 该分片处于文件的什么位置, offset>=0(从0字节开始). offset必须能整除64*1024

        :type content: string 
        :param content : 为文件内容

        Returns:
            json string.
        '''
        
        ret = {}
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str

        
        if "cosFile" not in params:
            ret.update({"code":-29489})
            ret.update({"msg":"cosFile is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"cosFile":params["cosFile"]})
        
        if "offset" not in params:
            ret.update({"code":-29484})
            ret.update({"msg":"offset is null"})
            return json.dumps(ret, sort_keys=True)        

        offset = params["offset"]
        if offset < 0 or offset % 64*1024 != 0:
            ret.update({"code":-29484})
            ret.update({"msg":"offset is invalid"})
            return json.dumps(ret, sort_keys=True)        
        
        str_offset = "%d" % (offset)
        params_dict.update({"offset":str_offset})

        contentType = "text/html"
        if sys.version_info >= (3, 0):
            fd = io.BytesIO(content)
        else:
            fd = StringIO.StringIO(content)
        
        response = self.post_http_data(params_dict, COSCONST.MULTIPART_UPLOAD, fd, contentType)
        
        if False == fd.closed:
            fd.close()
        
        return response

    def completeMultipartUpload(self, params):
        '''
                    完成分片上传
          
        :type params: dict       
        :param params: 可包含的key-value字段为：
        
        : type bucketId : string
        :      bucketId 桶Id（长度小于等于64、字符（123456789 and A~Z and a~z  and _  - .））
        
        : type path : string
        :      spath 存储到COS的文件全路径名，以"/"开头。允许ascII字符(0-31, 92, 127)；允许中文；
        
        Returns:
            json string.
        '''
        
        ret = {}
        params_dict = {}
   
        json_str = self.get_partial_required_param(params, params_dict)
        if (0 != len(json_str)):
            return json_str
        
        if "path" not in params:
            ret.update({"code":-29491})
            ret.update({"msg":"path is null"})
            return json.dumps(ret, sort_keys=True)
        
        params_dict.update({"path":params["path"]})
        
        response = self.get_http_data(params_dict, COSCONST.COMPLETE_MULTIPART_UPLOAD)
        
        return response

