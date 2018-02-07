import subprocess
import sys
from telnetlib import Telnet
import time
import getpass

print("Below is the pre-configured handset/imsi/msisdn information:\n\n"
      "A: Sony, IMSI: xxxxx6159999731, MSISDN: xx98999731\n"
      "B: Samsung, IMSI: xxxxx6159999732, MSISDN: xx98999732\n"
      "C: [phone3, IMSI: MSISDN]\n"
      "D: [multisim member 2]\n"
      "E: [unknown]\n")

aSerial = 'c5d9b0d5'
aMSISDN = 'xx97664378'
aIMSI = 'xxxxx7904099773'

bSerial = 'CB5A273T4Q'
bMSISDN = 'xx94374163'
bIMSI = 'xxxxx4375248088'

cSerial = 'c2b871ee'
cMSISDN = 'xx96864709'
cIMSI = 'xxxxx4376647041'
cfMSISDN = '96864709'

dSerial = 'c48063ff'
dMSISDN = 'xx87214648'
dcMSISDN = 'xx96816350'
dIMSI = 'xxxxx4375603570'

eSerial = ''
eMSISDN = ''
ecMSISDN = 'xx96816350'
eIMSI = ''

time.sleep(1)

print("Test case table: \n"
      "1.1 -> A calls B\n"
      "1.2 -> A calls B(CFU) to C\n"
      "1.3 -> A calls B(CFB) to C\n"
      "1.4 -> A calls B(CFNA) to C\n"
      "1.5 -> A calls B(CFNR) to C\n"
      "1.6 -> A calls barring(SS BAOC)\n"
      "1.7 -> A calls barring(SS BAIC)\n"
      "1.8 -> A calls barring(SS BOIC)\n"
      "1.9 -> A performs USSD\n"
      "1.10 -> A calls diverted to voicemail\n"
      "1.11 -> A calls to absent subscriber\n"
      "1.12 -> A calls B then conference to C\n"
      "1.13 -> A calls B for long\n"
      "1.14 -> A calls B with SRBT\n"
      "1.15 -> A calls B with video\n"
      "1.16 -> A calls common MSISDN(C, D) - B no answer\n"
      "1.17 -> A calls common MSISDN(C, D) - B busy\n"
      "1.18 -> A calls common MSISDN(C, D) - B detached\n"
      "1.19 -> A calls common MSISDN(C, D) - B no paging response\n"
      "1.20 -> C calls A\n"
      "1.21 -> D calls A\n"
      "1.22 -> A calls C(with C's MSISDN)\n"
      "1.23 -> A calls D(with D's MSISDN)\n"
      "1.24 -> C calls A(CFU) to B\n"
      "1.25 -> C calls A(CFB) to B\n"
      "1.26 -> C calls A(CFNA) to B\n"
      "1.27 -> C calls A(CFNR) to B\n"
      "1.28 -> A calls B(On Hold) calls C\n"
      "1.29 -> A(On Hold) calls B calls C\n"
      "1.30 -> A calls B and C swap to B\n"
      "1.31 -> A calls B and C swap to C\n"
      "1.32 -> A call VoLTE(Break-in)\n"
      "ALL\n")

testCase = input("Please enter the test case number, separated by comma: \n> ")

if testCase == 'ALL':
    testCaseList = ['1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9','1.10',
                    '1.11','1.12','1.13','1.14','1.15','1.16','1.17','1.18','1.19','1.20',
                    '1.21','1.22','1.23','1.24','1.25','1.26','1.27','1.28','1.29','1.30',
                    '1.31','1.31']
else:
    testCaseList = list(testCase.replace(' ','').split(','))

callSuccess = 0
callFail = 0
totalCall = len(testCaseList)
    
def makeCall(serial, MSISDN):
    command = "adb -s " + serial + " shell am start -a android.intent.action.CALL -d tel:+" + MSISDN
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if str(stdout) == "b'Starting: Intent { act=android.intent.action.CALL dat=tel:xxxxxxxxxxx }\\r\\r\\n'" or testCaseNo == '1.8':
        print("Call is made...")
    else:
        print("Not able to make call, please recheck.")
    time.sleep(20)

def answerCall(serial):
    command = "adb -s " + serial + " shell input keyevent 5"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if str(stdout) == "b''":
        print("Call is answered...")
    else:
        print("Not able to answer call, please recheck.")
    time.sleep(8)

def endCall(serial):
    command = "adb -s " + serial + " shell input keyevent 6"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if str(stdout) == "b''":
        print("Call is ended...")
    else:
        print("Not able to end call, please recheck.")
    time.sleep(1)

def captureLog(IMSI):
    command = "ZMCJ:IMSI=" + IMSI + ":;"
    tn.write(bytes(command, 'utf-8') + b"\r\n")
    output = tn.read_until(b"COMMAND EXECUTED").decode('ascii')
    print(output, file=open("D:\\autoTest\\" +  testCaseNo + ".txt", "a"))
    print("Log is being collected...")
    time.sleep(3)

def getCallStatus(serial):
    global callSuccess
    global callFail
    command = "adb -s " + serial + ' shell dumpsys telephony.registry | findstr "mCallState"' 
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if "mCallState=2" in str(stdout):
        callSuccess += 1
    else:
        callFail +=1
    time.sleep(1)

def captureTrace15sec():
    command = '"C:\\Program Files\\PuTTY\\plink.exe" -ssh -pw m1user root@172.30.12.225 "tcpdump -G 15 -ni eth3 -s 0 -w - not port 22" > D:\\autoTest\\'+testCaseNo+'.pcapng'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print('Trace is being captured...')

def turnAirplaneOnOff(serial):
    command = 'adb -s ' + serial + ' shell input keyevent 82'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell input touchscreen swipe 930 880 930 380'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell am start -a android.settings.AIRPLANE_MODE_SETTINGS'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell input keyevent 19'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell input keyevent 23'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell input keyevent 3'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.MAIN -c android.intent.category.HOME'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(3)

def pressEnter(serial):
    command = 'adb -s ' + serial + ' shell input keyevent 66'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(1)

def setCfuAct(serial, MSISDN):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*21*'+MSISDN+'%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfuDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2321%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfbAct(serial, MSISDN):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*67*'+MSISDN+'%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfbDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2367%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfnrAct(serial, MSISDN):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*61*'+MSISDN+'%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfnrDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2361%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfnaAct(serial, MSISDN):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*62*'+MSISDN+'%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setCfnaDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2362%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBaocAct(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*33*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBaocDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2333*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBaicAct(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*35*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBaicDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2335*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBoicAct(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*331*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setBoicDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%23331*1234%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def ussd(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*136%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setVoicemailAct(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"*67*1381%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def setVoicemailDea(serial):
    command = 'adb -s ' + serial + ' shell am start -a android.intent.action.CALL -d tel:"%2367%23"'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    time.sleep(2)

def mergeCall(serial): #only for sony xperia
    command = 'adb -s ' + serial + ' shell input tap 930 1150'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    command = 'adb -s ' + serial + ' shell input keyevent 66'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print("Call is merged...")
    time.sleep(10)

def makeVideoCall(serial, MSISDN):
    command = "adb -s " + serial + " shell am start -a android.intent.action.CALL -d tel:+" + MSISDN + " --ei android.telecom.extra.START_CALL_WITH_VIDEO_STATE 3"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if str(stdout) == "b'Starting: Intent { act=android.intent.action.CALL dat=tel:xxxxxxxxxxx }\\r\\r\\n'":
        print("Call is made...")
    else:
        print("Not able to make call, please recheck.")
    time.sleep(20)

"""
tn = Telnet(neIp)
tn.read_until(b"ENTER USERNAME < ")
tn.write(username.encode('ascii') + b"\r\n")
tn.read_until(b"ENTER PASSWORD < ")
tn.write(password.encode('ascii') + b"\r\n")
time.sleep(1)
"""

for testCaseNo in testCaseList:
    if testCaseNo == '1.1': #a calls b
        print("Executing test case no 1.1...")
        #captureTrace15sec()
        makeCall(aSerial, bMSISDN)
        answerCall(bSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.2': #a calls b cfu c
        print("Executing test case no 1.2...")
        #captureTrace15sec()
        setCfuAct(bSerial, cfMSISDN)
        makeCall(aSerial, bMSISDN)
        answerCall(cSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(cSerial)
        setCfuDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.3': #a calls b cfb c
        print("Executing test case no 1.3...")
        #captureTrace15sec()
        setCfbAct(bSerial, cfMSISDN)
        makeCall(aSerial, bMSISDN)
        endCall(bSerial)
        time.sleep(5)
        answerCall(cSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(cSerial)
        setCfbDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.4': #a calls b cfna c
        print("Executing test case no 1.4...")
        #captureTrace15sec()
        setCfnaAct(bSerial, cfMSISDN)
        pressEnter(bSerial)
        turnAirplaneOnOff(bSerial)
        makeCall(aSerial, bMSISDN)
        time.sleep(5)
        answerCall(cSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(cSerial)
        turnAirplaneOnOff(bSerial)
        setCfnaDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.5': #a calls b cfnr c
        print("Executing test case no 1.5...")
        setCfnrAct(bSerial, cfMSISDN)
        makeCall(aSerial, bMSISDN)
        time.sleep(30)
        answerCall(cSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(cSerial)
        setCfnrDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.6': #baoc
        print("Executing test case no 1.6...")
        setBaocAct(bSerial)
        makeCall(bSerial, aMSISDN)
        endCall(bSerial)
        setBaocDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.7': #baic
        print("Executing test case no 1.7...")
        setBaicAct(bSerial)
        makeCall(aSerial, bMSISDN)
        endCall(aSerial)
        setBaicDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.8': #boic
        print("Executing test case no 1.8...")
        setBoicAct(bSerial)
        makeCall(bSerial, '60121234567')
        endCall(bSerial)
        setBoicDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.9': #ussd
        print("Executing test case no 1.9...")
        ussd(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.10': #voicemail
        print("Executing test case no 1.10...")
        setVoicemailAct(bSerial)
        makeCall(aSerial, bMSISDN)
        endCall(bSerial)
        time.sleep(5)
        endCall(aSerial)
        setVoicemailDea(bSerial)
        pressEnter(bSerial)
        pressEnter(bSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.11': #absent
        print("Executing test case no 1.11...")
        makeCall(aSerial, '6596860014')
        endCall(aSerial)
        callSuccess += 1
        time.sleep(2)
    elif testCaseNo == '1.12': #conference
        print("Executing test case no 1.12...")
        makeCall(aSerial, bMSISDN)
        answerCall(bSerial)
        makeCall(bSerial, cMSISDN)
        answerCall(cSerial)
        mergeCall(bSerial) #only for sony xperia
        getCallStatus(bSerial)
        endCall(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.13': #long
        print("Executing test case no 1.13...")
        #captureTrace15sec()
        makeCall(aSerial, bMSISDN)
        answerCall(bSerial)
        time.sleep(600)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(bSerial)
        time.sleep(2)
    elif testCaseNo == '1.14': #srbt
        print("Executing test case no 1.14...")
        #captureTrace15sec()
        makeCall(aSerial, cMSISDN)
        time.sleep(5) #c has srbt
        answerCall(cSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(cSerial)
        time.sleep(2)
    elif testCaseNo == '1.15': #video
        print("Executing test case no 1.15...")
        #captureTrace15sec()
        makeVideoCall(aSerial, dcMSISDN)
        answerCall(dSerial)
        #captureLog(aIMSI)
        getCallStatus(aSerial)
        endCall(dSerial)
        time.sleep(2)
    elif testCaseNo == '1.16': #cmsisdn, no answer
        print("Executing test case no 1.16...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.17': #cmsisdn, busy
        print("Executing test case no 1.17...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.18': #cmsisdn, detached
        print("Executing test case no 1.18...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.19': #cmsisdn, no paging response
        print("Executing test case no 1.19...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.20': #c calls a
        print("Executing test case no 1.20...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.21': #d calls a
        print("Executing test case no 1.21...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.22': #a calls c's msisdn
        print("Executing test case no 1.22...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.23': #a calls d's msisdn
        print("Executing test case no 1.23...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.24': #c calls a cfu b
        print("Executing test case no 1.24...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.25': #c calls a cfb b
        print("Executing test case no 1.25...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.26': #c calls a cfna b
        print("Executing test case no 1.26...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.27': #c calls a cfnr b
        print("Executing test case no 1.27...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.28': #a calls b(on hold) calls c
        print("Executing test case no 1.28...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.29': #a(on hold) calls b calls c
        print("Executing test case no 1.29...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.30': #a calls b and c, swaps to b
        print("Executing test case no 1.30...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.31': #a calls b and c, swaps to c
        print("Executing test case no 1.31...")
        print("Sorry, it is not ready")
    elif testCaseNo == '1.32': #a calls volte break in
        print("Executing test case no 1.32...")
        print("Sorry, it is not ready")
    else:
        print("No test cases selected")

#tn.close()        
print("\nAll the selected test cases completed")

callSuccessRate = int(callSuccess/totalCall*100)
callFailRate = int(callFail/totalCall*100)

print("\nRESULT: ")
print("\tTotal test executed: "+str(totalCall))
print("\tTotal call succeeded: "+str(callSuccess))
print("\tTotal call failed: "+str(callFail))    

