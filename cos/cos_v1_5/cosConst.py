# -*- coding: utf-8 -*- 
'''
Created on 2013-4-30

@author: mucdullge
'''

class COSCONST:
    
    #外网cos api 域名
    HTTPHOST = "cosapi.myqcloud.com"
    
    #内网cos api域名
    INERTHOST = "cosapi.tencentyun.com"
    
    #外网cos 下载文件域名
    DOWNHOST = "cos.myqcloud.com"
    
    #内网cos 下载文件域名
    INERDOWNHOST = "cos.tencentyun.com"
    
    MKDIR_URL = "/api/cos_mkdir"
    
    RMDIR_URL = "/api/cos_rmdir"
    
    SETMETA_URL = "/api/cos_set_meta"
    
    GETMETA_URL = "/api/cos_get_meta"
    
    LISTFILE_URL = "/api/cos_list_file"
    
    DELETEFILE_URL = "/api/cos_delete_file"
    
    RENAME_URL = "/api/cos_rename"
    
    CREATEBUCKET_URL = "/api/cos_create_bucket"
    
    SETBUCKET_URL = "/api/cos_set_bucket"
    
    GETBUCKET_URL = "/api/cos_get_bucket"
    
    LISTBUCKET_URL = "/api/cos_list_bucket"
    
    DELETEBUCKET_URL = "/api/cos_delete_bucket"
    
    UPLOAD_URL = "/api/cos_upload"
    
    UPLOAD_WITHCOMPRESS_URL = "/api/cos_upload_with_compress"

    MULTIPART_UPLOAD = "/api/cos_multipart_upload"

    COMPLETE_MULTIPART_UPLOAD = "/api/cos_complete_multipart_upload"
    
    COMPRESS_FILE_URL = "/api/cos_compress_file"
    
    COS_TIME = "time"
    
    COS_ACCESSID = "accessId"
    
    COS_SECRETID = "secretId"
    
    COS_SIGN = "sign"
    
    FILE_MAX_LENGTH = 2147483647
