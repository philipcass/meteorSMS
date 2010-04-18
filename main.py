'''
Created on 2 Apr 2010

@author: phil
'''
import meteorSMS
import pickle
import getpass

try:
    pkl_file = open('meteorSMSuser.pkl', 'rb')
    userDetails = pickle.load(pkl_file)
    pkl_file.close()
except IOError:    
    usernm = raw_input("Mobile number: ")
    passwd = getpass.getpass()
    userDetails = {'username':usernm,'userpass':passwd}
    output = open('meteorSMSuser.pkl', 'wb')
    pickle.dump(userDetails, output)
    output.close()


session = meteorSMS.MeteorSMS(userDetails)

newMessage = session.createMessage()

mess = raw_input("Message:\n")

recip = raw_input("Phone No.:\n")


newMessage.addRecipient(recip)

newMessage.setMessage(mess)

session.sendMessage(newMessage)

session.closeSession()

