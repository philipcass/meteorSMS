'''
Created on 16 Apr 2010

@author: phil
'''

import httplib
import urllib

class MeteorSMS:
    '''
    classdocs
    '''
    #The headers for the HTTP POSTs
    headers = {"User-Agent": "Mozilla/5.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   'Keep-Alive':'300',
                   'Referer':'https://www.mymeteor.ie/',
                   'Connection':'keep-alive'}
    def __init__(self, userinfo):
        self.login(userinfo)
        
        pass
    
    def login(self, userDetails):
        headers = self.headers

        params = urllib.urlencode({'returnTo':'/',
                        'username':userDetails['username'],
                        'userpass':userDetails['userpass'],
                        'x':0,
                        'y':0})

        http = httplib.HTTPSConnection('www.mymeteor.ie', 443)
        http.connect()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        rawData = "username=" + userDetails['username'] + "&userpass=" + userDetails['userpass'] + "&x=0&y=0&returnTo=%2F"
        headers["Content-Length"] = len(rawData)
    
    
        #Login!
        http.request("POST", "https://www.mymeteor.ie/go/mymeteor-login-manager", params, headers)
        res = http.getresponse()
        
        print res.getheader("location")
    
        #Check the redirect for a login success
        if res.getheader("location").find("stat=success") != -1:
            print "Login Successful! "
            headers["Cookie"] = res.getheader("Set-Cookie")
            self.http = http
        else:
            http.close()
            try:
                raise Exception()
            except Exception:
                print "Login Failed. Please check your username and password"

        
    def createMessage(self):
        return Message()
        
    def sendMessage(self, message):
        headers = self.headers
        http = self.http
        rawData = "ajaxRequest=addEnteredMSISDNs&remove=-&add=0%7C"+message.messageData["recipent"]
        headers["Content-Length"] = len(rawData)
    
        params = urllib.urlencode({'add':'0|'+message.messageData["recipent"],
                                        'ajaxRequest':'addEnteredMSISDNs',
                                        'remove':'-'})
    
        http.request("POST", "https://www.mymeteor.ie/mymeteorapi/index.cfm?event=smsAjax&func=addEnteredMsisdns", params,headers)
        http.send((rawData))
        res = http.getresponse()
    
        #print res.read()
        #print "Add number: ", res.status, res.reason
        if res.status == httplib.OK:
            print "Added: "+message.messageData["recipent"]
    
        rawData = "ajaxRequest=sendSMS&messageText="+urllib.quote(message.messageData["text"])
        headers["Content-Length"] = len(rawData)
    
        params = urllib.urlencode({'ajaxRequest':'sendSMS',
                                    'messageText':message.messageData["text"]})
    
    
        http.request("POST", "https://www.mymeteor.ie/mymeteorapi/index.cfm?event=smsAjax&func=sendSMS&"+rawData, params,headers)
        http.send((rawData))
        res = http.getresponse()
    
        #print res.read() 
    
        if res.status == httplib.OK:
            print "Message Sent!"
        else:
            print "Sending Failed"
            
    def closeSession(self):
        self.http.close()
    
    
class Message():
    messageData = {"recipent":"","text":""}
    
    def __init__(self):
        pass

    def addRecipient(self,number):
        self.messageData["recipent"] = number
    
    def setMessage(self,text):
        self.messageData["text"] = text
        

