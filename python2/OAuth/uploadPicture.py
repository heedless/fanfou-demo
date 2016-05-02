# -*- coding:utf-8 -*-
import urlparse
import oauth2 as oauth
import sys,urllib,re
from urllib2 import Request,urlopen

consumer_key = ''
consumer_secret = ''
image = 'test.jpg'
status = '上传了一张图片。'

request_token_url = 'http://fanfou.com/oauth/request_token'
access_token_url = 'http://fanfou.com/oauth/access_token'
authorize_url = 'http://fanfou.com/oauth/authorize'

''' get the token '''
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
resp, content = client.request(request_token_url,"GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s. " % resp['status'])
request_token = dict(urlparse.parse_qsl(content))
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']

''' get the oauth_token '''
print "Go to the following link in your browser:"
print "%s?oauth_token=%s&oauth_callback=oob" % (authorize_url, request_token['oauth_token'])

accepted = 'n'
while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
oauth_verifier = raw_input('What is the PIN? ')

token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(access_token_url, "GET")
if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
access_token = dict(urlparse.parse_qsl(content))
print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print "You may now access protected resources using the access tokens above." 
oauth_token        = access_token['oauth_token']
oauth_token_secret = access_token['oauth_token_secret']


''' upload picture and send status to fanfou.com '''
import urlparse,sys,urllib,re
import oauth2 as oauth
from urllib2 import Request,urlopen

url = 'http://api.fanfou.com/photos/upload.json'
consumer = oauth.Consumer(consumer_key, consumer_secret)
token = oauth.Token(oauth_token,oauth_token_secret)
request = oauth.Request.from_consumer_and_token(consumer,
                                                token,                      
                                                http_url=url,              
                                                http_method='POST'
                                                )
signature_method = oauth.SignatureMethod_HMAC_SHA1()
request.sign_request(signature_method, consumer, token)
def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    auth_header = 'OAuth realm="%s"' % realm
    for k, v in request.iteritems():
        if k.startswith('oauth_') or k.startswith('x_auth_'):
            auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}

headers=request_to_header(request)

# 在 urllib2 上注册 http 流处理句柄
from poster.streaminghttp import register_openers
register_openers()
#import poster.streaminghttp
#opener = poster.streaminghttp.register_openers()

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

