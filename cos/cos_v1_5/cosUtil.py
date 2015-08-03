# -*- coding: utf-8 -*- 
'''
Created on 2013-4-27

@author: mucdullge
'''
import sys
if sys.version_info >= (3, 0):
    import urllib.request, urllib.parse, urllib.error
    import io
else:
    import urllib
    import StringIO

import base64
import hmac
import time
from hashlib import sha1 as sha
import os
import json

LOG_LEVEL = "INFO" 
PROVIDER = "COS"
PATH = os.getcwd()

def initlog(log_level = LOG_LEVEL,path = PATH ):
    '''
    :type path: string
    :param path: 日志文件路径
    
    :type log_level: string
    :param log_level: 日志级别
    
    Returns:
        logger Object.
    '''

    import logging
    from logging.handlers import RotatingFileHandler
    
    if path is None:
        path = PATH
    
    if path is "" :
        path = PATH
    
    LOGFILE = os.path.join(path, 'log.txt')
    MAXLOGSIZE = 100*1024*1024 #Bytes
    BACKUPCOUNT = 5
    FORMAT = \
    "%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"
    hdlr = RotatingFileHandler(LOGFILE,
                                  mode='a',
                                  maxBytes=MAXLOGSIZE,
                                  backupCount=BACKUPCOUNT)
    formatter = logging.Formatter(FORMAT)
    hdlr.setFormatter(formatter)
    logger = logging.getLogger("cos")
    logger.addHandler(hdlr)
    if "DEBUG" == log_level.upper():
        logger.setLevel(logging.DEBUG)
    elif "INFO" == log_level.upper():
        logger.setLevel(logging.INFO)
    elif "WARNING" == log_level.upper():
        logger.setLevel(logging.WARNING)
    elif "ERROR" == log_level.upper():
        logger.setLevel(logging.ERROR)
    elif "CRITICAL" == log_level.upper():
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.ERROR)
    return logger

LOGGER=initlog(LOG_LEVEL)


def cosUrlEncoding(param):
    '''
    url encode编码
    
    :type param : string
    :param param : 被编码字符串
    
    Returns:
        encoding string.
    '''
    if sys.version_info >= (3, 0):
        param = urllib.parse.quote(param)
    else:
        param = urllib.quote(param)
    param = param.replace("/", "%2F")
    return param

def formatTime(timeParam):
    '''
           获得时间戳（秒）
    
    :type timeParam : string
    :param timeParam : 当前时间戳
    
    Returns:
        timestampe string.
    '''
    
    index = timeParam.find(".",0,len(timeParam))
    
    return timeParam[0:index]



def makeSign(dict,methodName,accessKey):
    '''
         获取签名
    
    :type dict: dict
    :param dict: 参数数据集
    
    :type methodName: string
    :param methodName: http接口名
    
    :type acccessKey: string
    :param accessKey: 用户的密钥值
    
    Returns:
                    签名 string.
    '''
    global LOGGER
    if sys.version_info >= (3, 0):
        keys = list(dict.keys())
    else:
        keys = dict.keys()
    keys.sort()
    
    param =methodName+"&"
    
    for key in keys:
        param = param + key +"="+str(dict[key])+"&"
        
    rindex = param.rfind("&",0,len(param))
    param = param[0:rindex]
    LOGGER.info("before param : %s " % (param))
    param = cosUrlEncoding(param)
    LOGGER.info("param : %s" % (param))
    if sys.version_info >= (3, 0):
        h = hmac.new(accessKey.encode(), param.encode(), sha)
        return base64.encodebytes(h.digest()).strip()
    else:
        h = hmac.new(accessKey, param, sha)
        return base64.encodestring(h.digest()).strip()

def makeDownSign(param,accessKey):
    '''
         获取下载签名
    
    
    :type param: string
    :param param: 签名传
    
    :type acccessKey: string
    :param accessKey: 用户的密钥值
    
    Returns:
                    签名 string.
    '''
    global LOGGER
    LOGGER.info("before sign param : %s " %(param))
    param = cosUrlEncoding(param)
    
    LOGGER.info("make down sign param : %s " %(param))

    if sys.version_info >= (3, 0):   
        h = hmac.new(accessKey.encode(), param.encode(), sha)
    else:
        h = hmac.new(accessKey, param, sha)
    return base64.encodestring(h.digest()).strip()

def makeUrl(param,host,methodName):
    '''
    
    :type param: dict
    :param param: 参数数据集
    
    :type host: string
    :param host: 主机域名
    
    :type methodName: string
    :param methodName: http接口名称
    
    Returns:
        url string.
    '''
    global LOGGER
    if sys.version_info >= (3, 0):
        keys = list(param.keys())
        url = methodName+"?"	
        for key in keys:
            url = url + key + "="+urllib.parse.quote(param[key])+"&"
    else:
        keys = param.keys()
        url = "http://" + host + methodName + "?"
        for key in keys:
            url = url + key + "="+urllib.quote(param[key])+"&"

    rindex = url.rfind("&",0,len(url))
    
    url = url[0:rindex]
    
    LOGGER.info("get url : %s" % (url));
    
    return url
    

def getFileType(fileName):
    '''
          获取文件类型
    
    :type fileName: string
    :param fileName: 文件名
    
    Returns:
        filetype string.
    '''
    
    suffix = ""
    name = os.path.basename(fileName)
    suffix = name.split('.')[-1]

    map = {}
    map['html'] = 'text/html'
    map['htm'] = 'text/html'
    map['asc'] = 'text/plain'
    map['txt'] = 'text/plain'
    map['c'] = 'text/plain'
    map['c++'] = 'text/plain'
    map['cc'] = 'text/plain'
    map['cpp'] = 'text/plain'
    map['h'] = 'text/plain'
    map['rtx'] = 'text/richtext'
    map['rtf'] = 'text/rtf'
    map['sgml'] = 'text/sgml'
    map['sgm'] = 'text/sgml'
    map['tsv'] = 'text/tab-separated-values'
    map['wml'] = 'text/vnd.wap.wml'
    map['wmls'] = 'text/vnd.wap.wmlscript'
    map['etx'] = 'text/x-setext'
    map['xsl'] = 'text/xml'
    map['xml'] = 'text/xml'
    map['talk'] = 'text/x-speech'
    map['css'] = 'text/css'

    map['gif'] = 'image/gif'
    map['xbm'] = 'image/x-xbitmap'
    map['xpm'] = 'image/x-xpixmap'
    map['png'] = 'image/png'
    map['ief'] = 'image/ief'
    map['jpeg'] = 'image/jpeg'
    map['jpg'] = 'image/jpeg'
    map['jpe'] = 'image/jpeg'
    map['tiff'] = 'image/tiff'
    map['tif'] = 'image/tiff'
    map['rgb'] = 'image/x-rgb'
    map['g3f'] = 'image/g3fax'
    map['xwd'] = 'image/x-xwindowdump'
    map['pict'] = 'image/x-pict'
    map['ppm'] = 'image/x-portable-pixmap'
    map['pgm'] = 'image/x-portable-graymap'
    map['pbm'] = 'image/x-portable-bitmap'
    map['pnm'] = 'image/x-portable-anymap'
    map['bmp'] = 'image/bmp'
    map['ras'] = 'image/x-cmu-raster'
    map['pcd'] = 'image/x-photo-cd'
    map['wi'] = 'image/wavelet'
    map['dwg'] = 'image/vnd.dwg'
    map['dxf'] = 'image/vnd.dxf'
    map['svf'] = 'image/vnd.svf'
    map['cgm'] = 'image/cgm'
    map['djvu'] = 'image/vnd.djvu'
    map['djv'] = 'image/vnd.djvu'
    map['wbmp'] = 'image/vnd.wap.wbmp'

    map['ez'] = 'application/andrew-inset'
    map['cpt'] = 'application/mac-compactpro'
    map['doc'] = 'application/msword'
    map['msw'] = 'application/x-dox_ms_word'
    map['oda'] = 'application/oda'
    map['dms'] = 'application/octet-stream'
    map['lha'] = 'application/octet-stream'
    map['lzh'] = 'application/octet-stream'
    map['class'] = 'application/octet-stream'
    map['so'] = 'application/octet-stream'
    map['dll'] = 'application/octet-stream'
    map['pdf'] = 'application/pdf'
    map['ai'] = 'application/postscript'
    map['eps'] = 'application/postscript'
    map['ps'] = 'application/postscript'
    map['smi'] = 'application/smil'
    map['smil'] = 'application/smil'
    map['mif'] = 'application/vnd.mif'
    map['xls'] = 'application/vnd.ms-excel'
    map['xlc'] = 'application/vnd.ms-excel'
    map['xll'] = 'application/vnd.ms-excel'
    map['xlm'] = 'application/vnd.ms-excel'
    map['xlw'] = 'application/vnd.ms-excel'
    map['ppt'] = 'application/vnd.ms-powerpoint'
    map['ppz'] = 'application/vnd.ms-powerpoint'
    map['pps'] = 'application/vnd.ms-powerpoint'
    map['pot'] = 'application/vnd.ms-powerpoint'

    map['wbxml'] = 'application/vnd.wap.wbxml'
    map['wmlc'] = 'application/vnd.wap.wmlc'
    map['wmlsc'] = 'application/vnd.wap.wmlscriptc'
    map['vcd'] = 'application/x-cdlink'
    map['pgn'] = 'application/x-chess-pgn'
    map['dcr'] = 'application/x-director'
    map['dir'] = 'application/x-director'
    map['dxr'] = 'application/x-director'
    map['spl'] = 'application/x-futuresplash'

    map['gtar'] = 'application/x-gtar'
    map['tar'] = 'application/x-tar'
    map['ustar'] = 'application/x-ustar'
    map['bcpio'] = 'application/x-bcpio'
    map['cpio'] = 'application/x-cpio'
    map['shar'] = 'application/x-shar'
    map['zip'] = 'application/zip'
    map['hqx'] = 'application/mac-binhex40'
    map['sit'] = 'application/x-stuffit'
    map['sea'] = 'application/x-stuffit'
    map['bin'] = 'application/octet-stream'
    map['exe'] = 'application/octet-stream'
    map['src'] = 'application/x-wais-source'
    map['wsrc'] = 'application/x-wais-source'
    map['hdf'] = 'application/x-hdf'

    map['js'] = 'application/x-javascript'
    map['sh'] = 'application/x-sh'
    map['csh'] = 'application/x-csh'
    map['pl'] = 'application/x-perl'
    map['tcl'] = 'application/x-tcl'

    map['skp'] = 'application/x-koan'
    map['skd'] = 'application/x-koan'
    map['skt'] = 'application/x-koan'
    map['skm'] = 'application/x-koan'
    map['nc'] = 'application/x-netcdf'
    map['cdf'] = 'application/x-netcdf'
    map['swf'] = 'application/x-shockwave-flash'
    map['sv4cpio'] = 'application/x-sv4cpio'
    map['sv4crc']  = 'application/x-sv4crc'
    map['t'] = 'application/x-troff'
    map['tr'] = 'application/x-troff'
    map['roff'] = 'application/x-troff'
    map['man'] = 'application/x-troff-man'
    map['me'] = 'application/x-troff-me'
    map['ms'] = 'application/x-troff-ms'
    map['latex'] = 'application/x-latex'
    map['tex'] = 'application/x-tex'
    map['texinfo'] = 'application/x-texinfo'
    map['texi'] = 'application/x-texinfo'
    map['dvi'] = 'application/x-dvi'
    map['xhtml'] = 'application/xhtml+xml'
    map['xht'] = 'application/xhtml+xml'

    map['au'] = 'audio/basic'
    map['snd'] = 'audio/basic'
    map['aif'] = 'audio/x-aiff'
    map['aiff'] = 'audio/x-aiff'
    map['aifc'] = 'audio/x-aiff'
    map['wav'] = 'audio/x-wav'
    map['mpa'] = 'audio/x-mpeg'
    map['abs'] = 'audio/x-mpeg'
    map['mpega'] = 'audio/x-mpeg'
    map['mp2a'] = 'audio/x-mpeg2'
    map['mpa2'] = 'audio/x-mpeg2'
    map['mid'] = 'audio/midi'
    map['midi'] = 'audio/midi'
    map['kar'] = 'audio/midi'
    map['mp2'] = 'audio/mpeg'
    map['mp3'] = 'audio/mpeg'
    map['m3u'] = 'audio/x-mpegurl'
    map['ram'] = 'audio/x-pn-realaudio'
    map['rm'] = 'audio/x-pn-realaudio'
    map['rpm'] = 'audio/x-pn-realaudio-plugin'
    map['ra'] = 'audio/x-realaudio'

    map['pdb'] = 'chemical/x-pdb'
    map['xyz'] = 'chemical/x-xyz'
    map['igs'] = 'model/iges'
    map['iges'] = 'model/iges'
    map['msh'] = 'model/mesh'
    map['mesh'] = 'model/mesh'
    map['silo'] = 'model/mesh'

    map['wrl'] = 'model/vrml'
    map['vrml'] = 'model/vrml'
    map['vrw'] = 'x-world/x-vream'
    map['svr'] = 'x-world/x-svr'
    map['wvr'] = 'x-world/x-wvr'
    map['3dmf'] = 'x-world/x-3dmf'
    map['p3d'] = 'application/x-p3d'

    map['mpeg'] = 'video/mpeg'
    map['mpg'] = 'video/mpeg'
    map['mpe'] = 'video/mpeg'
    map['mpv2'] = 'video/mpeg2'
    map['mp2v'] = 'video/mpeg2'
    map['qt'] = 'video/quicktime'
    map['mov'] = 'video/quicktime'
    map['avi'] = 'video/x-msvideo'
    map['movie'] = 'video/x-sgi-movie'
    map['vdo'] = 'video/vdo'
    map['viv'] = 'video/viv'
    map['mxu'] = 'video/vnd.mpegurl'

    map['ice'] = 'x-conference/x-cooltalk'
    mime_type = ""

    if sys.version_info >= (3, 0):
        if suffix in map:
            mime_type = map[suffix]
        else:
            mime_type = 'application/octet-stream'
    else:
        if map.has_key(suffix):
            mime_type = map[suffix]
        else:
            mime_type = 'application/octet-stream'
    return mime_type
    



