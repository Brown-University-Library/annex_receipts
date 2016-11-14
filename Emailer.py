"""
Part of LAS-to-Josiah code.
Handle sending of email when files are found.
"""



import smtplib



class Emailer:



  smtpserver = settings.MAIL_SMTPSERVER
  AUTHREQUIRED = 0 # if you need to use SMTP AUTH set to 1
  smtpuser = ''  # for SMTP AUTH, set SMTP username here
  smtppass = ''  # for SMTP AUTH, set SMTP password here

  RECIPIENTS = settings.MAIL_RECIPIENTS

  SENDER = settings.MAIL_SENDER

  headerTo = settings.MAIL_HEADERTO
  headerCc = settings.MAIL_HEADERCC
  headerFrom = settings.MAIL_HEADERFROM
  headerSubject = settings.MAIL_SUBJECT
  basicHeaderInfo = headerTo + "\n" + headerCc + "\n" + headerFrom + "\n" + headerSubject + "\n"




  def sendEmail(self, message):

    session = smtplib.SMTP(self.smtpserver)
    if self.AUTHREQUIRED:
      session.login(self.smtpuser, self.smtppass)

    returnValue = "init"

    fullMessage = self.basicHeaderInfo + message
    try:
      smtpresult = session.sendmail(self.SENDER, self.RECIPIENTS, fullMessage)

#     if smtpresult:
#       errorString = ""
#       for recip in smtpresult.keys():
#         errorString = "Could not deliver mail to: " + recip + "\n"
#         errorString = errorString + "Server said: " + smtpresult[recip][0] + "\n"
#         errorString = errorString + smtpresult[recip][1] + "\n"
#         errorString = errorString + errstr
#       raise smtplib.SMTPException, errstr

    except:
      session.quit()
      print "\n"
      print "Attempt to send email failed with following errors: " + str(smtpresult)
      returnValue = smtpresult

    else:
      session.quit()
      returnValue = "success"

    return returnValue



# bottom
