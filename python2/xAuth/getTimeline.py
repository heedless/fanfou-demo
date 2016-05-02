# -*- coding:utf-8 -*-
import sys, urllib, oauth2 as oauth, re
from urllib2 import Request, urlopen

consumer_key = ''
consumer_secret = ''
page = 1

access_token_url = 'http://fanfou.com/oauth/access_token'
url = 'http://api.fanfou.com/statuses/user_timeline.xml'

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
params["page"]=page
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
    ''' get timeline from fanfou.com'''
    oauth_token = oauth.Token(m.group('key'), m.group('secret'))
    request = oauth.Request.from_consumer_and_token(consumer,
                                                     token=oauth_token,
                                                     http_url=url)
    request.sign_request(signature_method, consumer, oauth_token)
    headers=request_to_header(request)
    resp = urlopen(Request(url, headers=headers))
    resp = resp.read()
    print resp
