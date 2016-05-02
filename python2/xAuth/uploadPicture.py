# -*- coding:utf-8 -*-
import sys, urllib, oauth2 as oauth, re
from urllib2 import Request, urlopen

consumer_key = ''
consumer_secret = ''
image = 'test.jpg'
status = '上传了一张图片。'

access_token_url = 'http://fanfou.com/oauth/access_token'

def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    auth_header = 'OAuth realm="%s"' % realm
        # Add the oauth parameters.
    #if request.parameters:
    #    for k, v in request.parameters.iteritems():
    #        if k.startswith('oauth_') or k.startswith('x_auth_'):
    #            auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    
    ''' 这里少个判断request是否没有参数'''
    for k, v in request.iteritems():
        if k.startswith('oauth_') or k.startswith('x_auth_'):
            auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}

# get username and password from command line 
username = sys.argv[1]
passwd = sys.argv[2]

consumer = oauth.Consumer(consumer_key, consumer_secret)
params = {}
params["x_auth_username"] = username
params["x_auth_password"] = passwd
params["x_auth_mode"] = 'client_auth'
request = oauth.Request.from_consumer_and_token(consumer,
                                                http_url=access_token_url,
                                                parameters=params
                                                     )
signature_method = oauth.SignatureMethod_HMAC_SHA1()
request.sign_request(signature_method, consumer, None)
headers=request_to_header(request)
resp = urlopen(Request(access_token_url, headers=headers))

token = resp.read()
print token  # access_token got
m = re.match(r'oauth_token=(?P<key>[^&]+)&oauth_token_secret=(?P<secret>[^&]+)', token)
if m:

    ''' upload a picture and send status to fanfou.com'''
    url = 'http://api.fanfou.com/photos/upload.json'
    oauth_token = oauth.Token(m.group('key'), m.group('secret'))
    request = oauth.Request.from_consumer_and_token(consumer,
                                                     token=oauth_token,
                                                     http_url=url,
                                                     http_method='POST',
                                                     parameters=params    
                                                     )
    request.sign_request(signature_method, consumer, oauth_token)
    headers=request_to_header(request)

    # 在 urllib2 上注册 http 流处理句柄
    from poster.streaminghttp import register_openers
    register_openers()

    import poster.encode
    import poster.streaminghttp

    all_upload_params = {
	'photo':open(image, 'rb'), 'status':status
    }

    # 开始对文件 "test.jpg" 的 multiart/form-data 编码
    # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
    # headers 包含必须的 Content-Type 和 Content-Length
    # datagen 是一个生成器对象，返回编码过后的参数，这里如果有多个参数的话依次添加即可
    datagen, headers2 = poster.encode.multipart_encode(all_upload_params)

    #添加headers
    headers = dict(headers, **headers2)

    resp = urlopen(Request(url,data=datagen,headers=headers))
    resp = resp.read()
    print "Best Wishes!"

