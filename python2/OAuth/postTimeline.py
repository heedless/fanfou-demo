# -*- coding:utf-8 -*-
import urlparse
import oauth2 as oauth
import sys, urllib, re
from urllib2 import Request, urlopen

consumer_key = ''
consumer_secret = ''
status = '人是万物的尺度：是存在者存在的尺度，也是不存在者不存在的尺度。——普罗泰格拉'

request_token_url = 'http://fanfou.com/oauth/request_token'
access_token_url = 'http://fanfou.com/oauth/access_token'
authorize_url = 'http://fanfou.com/oauth/authorize'

'''get token'''
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
request_token = dict(urlparse.parse_qsl(content))
print request_token
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']

'''用户授权,获取oauth_token'''
print "Go to the following link in your browser:"
print "%s?oauth_token=%s&oauth_callback=oob" % (authorize_url, request_token['oauth_token'])
print 

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
print

oauth_token        = access_token['oauth_token']
oauth_token_secret = access_token['oauth_token_secret']

'''send status to fanfou.com'''
params={}
params['status']=status
url = 'http://api.fanfou.com/statuses/update.xml'

consumer = oauth.Consumer(consumer_key, consumer_secret)
token = oauth.Token(oauth_token,oauth_token_secret)

request = oauth.Request.from_consumer_and_token(consumer,
                                                token,
                                                http_url=url,
                                                http_method='POST',
                                                parameters=params    
                                                )
signature_method = oauth.SignatureMethod_HMAC_SHA1()
request.sign_request(signature_method, consumer, token)

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

headers=request_to_header(request)
data = {'status':status}
data = urllib.urlencode(data)
resp = urlopen(Request(url,data=data,headers=headers))
resp = resp.read()
print "Best Wishes!"

