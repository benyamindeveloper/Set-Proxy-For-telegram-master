import os
import json
import urllib.request
import requests
import time

####################################### Variable General ##############################################
countUbuntu = 0
isNotErrorFirst = True
####################################### Variable Servers ##############################################
aws_access_key = "AKIA2PFODQOLTI7ZROH3"
aws_secret_access_key = "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"
region_config_group_A_ubuntu_1 = "ap-northeast-1"
region_config_group_A_ubuntu_2 = "ap-northeast-1"
region_config_group_B_ubuntu_3 = "ap-south-1"
region_config_group_B_ubuntu_4 = "ap-south-1"
address_ping = "http://45.82.138.73:81/myip/"
##################################### Variable General ################################################
# region Variable General
isEnableDNS = True
# endregion Variable General

##################################### first Time Disable ################################################

firstTimeDisableA = 0
firstTimeDisableB = 0

##################################### Variable DNS Server and records ################################################
##################################### Variable DNS Server and records ################################################
# region Variable DNS Server and records
DNS_Server_APIKey = "2KY1MXMXDgWNzfNgc1a8faWM8KSgphhY"
idDns1GroupA = "8833804"
idDns2GroupA = ""
idDns3GroupA = ""
idDns4GroupA = ""
idDns1GroupB = "8833804"
idDns2GroupB = ""
idDns3GroupB = ""
idDns4GroupB = ""
idRecordDns1GroupA = "4462013"
idRecordDns2GroupA = "4462550"
idRecordDns3GroupA = ""
idRecordDns4GroupA = ""
idRecordDns1GroupB = "4466760"
idRecordDns2GroupB = "4466763"
idRecordDns3GroupB = ""
idRecordDns4GroupB = ""
myIP1 = "1.1.1.1"
myIP2 = "3.3.3.3"
myIP3 = "3.3.3.3"
myIP4 = "4.4.4.4"



# endregion Variable DNS Server and records

####################################### Function #######################################
def ConfigAWS(regionName, description):
    os.system("aws configure set aws_access_key_id  " + aws_access_key)
    os.system("aws configure set aws_secret_access_key  " + aws_secret_access_key)
    os.system("aws configure set region  " + regionName)
    os.system("aws configure set output  json")
    print("# Configuration  " + description)


# *************************************** Method Stop First Time **********************************************
def StopServerFirst(instanceName):
    print("# Stop " + instanceName)
    os.system("aws lightsail stop-instance --instance-name " + instanceName)


# *************************************** Method Stop Loop While **********************************************
def StopTwoserverTogther(instanceName1, description1, isFirstTime1, instanceName2, description2, isFirstTime2):
    while True:
        strstop1 = CheckStateService(instanceName1).lstrip()
        strstop2 = CheckStateService(instanceName2).lstrip()
        if ((strstop1 == "stopped") and (isFirstTime1 == True) and (strstop2 == "stopped") and (isFirstTime2 == True)):
            os.system("aws lightsail stop-instance --instance-name " + instanceName1)
            os.system("aws lightsail stop-instance --instance-name " + instanceName2)
            print("# Stop " + description1 + "# Stop " + description2)
            break
        else:
            if isFirstTime1 == True and isFirstTime2 == True:
                print(" The " + description1 + " not is stopped ")
            if isFirstTime1 == False and isFirstTime2 == False:
                os.system("aws lightsail stop-instance --instance-name " + instanceName1)
                os.system("aws lightsail stop-instance --instance-name " + instanceName2)
                print("# Stop " + description1 + "# Stop " + description2)
                break
        time.sleep(10)

# *************************************** Method Stop Loop While **********************************************
def StopServer(instanceName, description, isFirstTime):
    while True:
        strstop = CheckStateService(instanceName).lstrip()
        if ((strstop == "stopped") and (isFirstTime == True)):
            os.system("aws lightsail stop-instance --instance-name " + instanceName)
            print("# Stop " + description)
            break
        else:
            if isFirstTime == True:
                print(" The " + description + " not is stopped ")
            if isFirstTime == False:
                os.system("aws lightsail stop-instance --instance-name " + instanceName)
                print("# Stop " + description)
                break
        time.sleep(10)


# *************************************** Method Check State Service **********************************************
def CheckStateService(instanceName):
    data = json.loads(os.popen("aws lightsail get-instance-state --instance-name " + instanceName).read())
    Array = data["state"]
    return Array["name"]


# *************************************** Method Start Server **********************************************
def StartServer(instanceName, description):
    while True:
        strStart = CheckStateService(instanceName).lstrip();
        if (strStart == "stopped"):
            os.system("aws lightsail start-instance --instance-name " + instanceName)
            print("# Start " + description)
            break
        else:
            print("# The " + instanceName + " not yet stopped")
        time.sleep(10)
# *************************************** Method Start Server **********************************************
def StartTwoserverTogther(instanceName1, description1, instanceName2, description2):
    while True:
        strStart1 = CheckStateService(instanceName1).lstrip();
        strStart2 = CheckStateService(instanceName2).lstrip();
        if (strStart1 == "stopped" and strStart2 == "stopped"):
            os.system('aws lightsail start-instance --instance-name ' + instanceName1)
            os.system('aws lightsail start-instance --instance-name ' + instanceName2)
            print("# Start " + description1, "# Start " + description2)
            break
        else:
            print("# The " + instanceName1 + " not yet stopped" + "# The " + instanceName2 + " not yet stopped")
        time.sleep(10)


# *************************************** Check Filter Server **********************************************
def CheckFilterServer(Ip, description):
    _Ip = Ip
    _description = description
    try:
        time.sleep(30)
        with urllib.request.urlopen(address_ping + Ip) as f:
            readping = str(f.read()).split('<div>')[1].split('</div>')[0]
            print("# Check ping from " + description)
            return readping
    except:

        CheckFilterServer(_Ip, _description)


# *************************************** Get IP Service **********************************************
def GetIPService(instanceName, description):
    while True:
        strGetIp = CheckStateService(instanceName).lstrip();
        if (strGetIp == "running"):
            data = json.loads(os.popen("aws lightsail get-instance --instance-name " + instanceName).read())
            Array = data["instance"]
            print("# Get ip from " + description)
            return Array["publicIpAddress"]
        else:
            print("# The Server not is running " + description)
        time.sleep(10)


####################################### Group A ##############################################
while True:
    if countUbuntu == 0:
        print('Starting Group A')
        if firstTimeDisableA == 0:
            firstTimeDisableA = 1
            # region disbale group A
            headers = {
                'accept': 'application/json',
                'API-Key': '' + DNS_Server_APIKey + '',
                'Content-Type': 'application/json',
            }
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns1GroupA + '',
                          headers=headers,
                          data='{"nodeName":"","recordType":"A","state":false,group:"A","ipv4Address":"' + myIP1 + '"}')
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns2GroupA + '',
                          headers=headers,
                          data='{"nodeName":"","recordType":"A","state":false,group:"A","ipv4Address":"' + myIP2 + '"}')
            isEnableDNS = False
            print("# Disbale group A")
            # endregion disbale group A
            print("# endregion disbale group A start time sleep 60")
            time.sleep(60)

        # region config AWS
        ConfigAWS(region_config_group_A_ubuntu_1, "Group A _ubuntu_1")
        ConfigAWS(region_config_group_A_ubuntu_2, "Group A _ubuntu_2")
        # endregion config AWS
        # region Stop AWS server A
        StopTwoserverTogther("Ubuntu-1", "Group A", False,"Ubuntu-2", "Group A", False)
        # endregion Stop AWS server A
        # region Start AWS server A
        StartTwoserverTogther("Ubuntu-1", "Group A server Ubuntu-1", "Ubuntu-2", "Group A server Ubuntu-2")
        # endregion Start AWS server A
        IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
        print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
        IP_ubuntu_2 = GetIPService("Ubuntu-2", "Group A server Ubuntu-2")
        print("******* Group A server Ubuntu-2 : " + IP_ubuntu_2)

        # time.sleep(60)
        resultCheckIPUbuntu_1 = CheckFilterServer(IP_ubuntu_1, "Group A")
        print("*******************CHECK Group A Ubuntu-1 IP: " + resultCheckIPUbuntu_1)
        # if ping is false
        if resultCheckIPUbuntu_1 == 'false':
           while  True:
               StopServer("Ubuntu-1", "Group A", False)
               StartServer("Ubuntu-1", "Group A server Ubuntu-1")
               IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
               resultCheckIPUbuntu_1 = CheckFilterServer(IP_ubuntu_1, "Group A")
               print("******* Group A server Ubuntu-1  : " + resultCheckIPUbuntu_1)
               if resultCheckIPUbuntu_1 == 'true':
                   break

        resultCheckIPUbuntu_2 = CheckFilterServer(IP_ubuntu_2, "Group A")
        print("*******************CHECK Group A Ubuntu-2 IP: " + resultCheckIPUbuntu_2)
        # if ping is false
        if CheckFilterServer(IP_ubuntu_2, "Group A") == 'false':
            while True:
                StopServer("Ubuntu-2", "Group A", False)
                StartServer("Ubuntu-2", "Group A server Ubuntu-2")
                IP_ubuntu_2 = GetIPService("Ubuntu-2", "Group A server Ubuntu-2")
                resultCheckIPUbuntu_2 = CheckFilterServer(IP_ubuntu_2, "Group A")
                print("******* Group A server Ubuntu-2  : " + resultCheckIPUbuntu_2)
                if resultCheckIPUbuntu_2 == 'true':
                    break

        if resultCheckIPUbuntu_1 == 'true' and  resultCheckIPUbuntu_2 == 'true':
            # region update ip dns server
            headers = {
                'accept': 'application/json',
                'API-Key': '' + DNS_Server_APIKey + '',
                'Content-Type': 'application/json',
            }
            data = '{"nodeName":"","recordType":"A","state":true,group:"A","ipv4Address":"' + IP_ubuntu_1 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns1GroupA + '',
                          headers=headers,
                          data=data)
            data = '{"nodeName":"","recordType":"A","state":true,group:"A","ipv4Address":"' + IP_ubuntu_2 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns2GroupA + '',
                          headers=headers,
                          data=data)
            print("# Updated DNS ip Group A")
            # endregion update ip dns server

            countUbuntu = 1
            firstTimeDisableA = 0
            isEnableDNS = True
            time.sleep(150)

        else:
            print('# Error ip ping Group A')

####################################### Group B ##############################################
    if countUbuntu == 1:
        print('Starting Group B')
        if firstTimeDisableB == 0:
            firstTimeDisableB = 1
            # region disbale group B
            headers = {
               'accept': 'application/json',
               'API-Key': '' + DNS_Server_APIKey + '',
               'Content-Type': 'application/json',
            }
            data = '{"nodeName":"","recordType":"A","state":false,group:"B","ipv4Address":"' + myIP3 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns1GroupB + '',
                         headers=headers,
                         data=data)
            data = '{"nodeName":"","recordType":"A","state":false,group:"B","ipv4Address":"' + myIP4 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns2GroupB + '',
                         headers=headers,
                         data=data)
            isEnableDNS = False
            print("# Disbale group B")
            # endregion disbale group B
            print("# endregion disbaled group B start time sleep 60")
            # time.sleep(60)



        # region config AWS
        ConfigAWS(region_config_group_B_ubuntu_3, "Group B _ubuntu_3")
        ConfigAWS(region_config_group_B_ubuntu_4, "Group B _ubuntu_4")
        # endregion config AWS
        # region Stop AWS server A
        StopTwoserverTogther("Ubuntu-3", "Group B server Ubuntu-3", False, "Ubuntu-4", "Group B server Ubuntu-4", False)
        # endregion Stop AWS server A
        # region Start AWS server A
        StartTwoserverTogther("Ubuntu-3", "Group B server Ubuntu-3", "Ubuntu-4", "Group B server Ubuntu-4")
        # endregion Start AWS server A
        IP_ubuntu_3 = GetIPService("Ubuntu-3", "Group B")
        print("******* Group B server Ubuntu-3 : " + IP_ubuntu_3)
        IP_ubuntu_4 = GetIPService("Ubuntu-4", "Group B")
        print("******* Group B server Ubuntu-4 : " + IP_ubuntu_4)

        # time.sleep(60)
        resultCheckIPUbuntu_3 = CheckFilterServer(IP_ubuntu_3, "Group B")
        print("*******************CHECK Group B Ubuntu-3 IP: " + resultCheckIPUbuntu_3)
        # if ping is false
        if resultCheckIPUbuntu_3 == 'false':
            while True:
                StopServer("Ubuntu-3", "Group B", False)
                StartServer("Ubuntu-3", "Group B server Ubuntu-3")
                IP_ubuntu_3 = GetIPService("Ubuntu-3", "Group B server Ubuntu-3")
                resultCheckIPUbuntu_4 = CheckFilterServer(IP_ubuntu_4, "Group B")
                print("******* Group B server Ubuntu-3  : " + resultCheckIPUbuntu_4)
                if resultCheckIPUbuntu_4 == 'true':
                    break
        resultCheckIPUbuntu_4 = CheckFilterServer(IP_ubuntu_4, "Group B")
        print("*******************CHECK Group B Ubuntu-4 IP: " + resultCheckIPUbuntu_4)
        # if ping is false
        if resultCheckIPUbuntu_4 == 'false':
            while True:
                StopServer("Ubuntu-4", "Group B", False)
                StartServer("Ubuntu-4", "Group B server Ubuntu-4")
                IP_ubuntu_4 = GetIPService("Ubuntu-4", "Group B server Ubuntu-4")
                resultCheckIPUbuntu_4 = CheckFilterServer(IP_ubuntu_4, "Group B")
                print("******* Group B server Ubuntu-4  : " + resultCheckIPUbuntu_4)
                if resultCheckIPUbuntu_4 == 'true':
                    break
        if resultCheckIPUbuntu_3 == 'true' and resultCheckIPUbuntu_4 == 'true':
            # region Update ip dns server
            headers = {
                'accept': 'application/json',
                'API-Key': '' + DNS_Server_APIKey + '',
                'Content-Type': 'application/json',
            }
            data = '{"nodeName":"","recordType":"A","state":true,group:"B","ipv4Address":"' + IP_ubuntu_3 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns1GroupB + '',
                          headers=headers,
                          data=data)
            data = '{"nodeName":"","recordType":"A","state":true,group:"B","ipv4Address":"' + IP_ubuntu_4 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns2GroupB + '',
                          headers=headers,
                          data=data)
            print("# Updated DNS ip Group B")
            # endregion update ip dns server

            countUbuntu = 0
            firstTimeDisableB = 0
            isEnableDNS = True
            time.sleep(150)

        else:
            print('# Error ip ping Group B')
