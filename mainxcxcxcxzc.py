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
region_config_group_A_ubuntu_1 = "ap-south-1"
region_config_group_A_ubuntu_2 = "ap-south-1"
region_config_group_B_ubuntu_3 = "ap-southeast-1"
region_config_group_B_ubuntu_4 = "ap-southeast-1"
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
myip1 = "13.233.111.158"
myip2 = "52.77.227.128"


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
            data = '{"nodeName":"","recordType":"A","state":false,group:"A","ipv4Address":"' + myip1 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns1GroupA + '',
                          headers=headers,
                          data=data)
            data = '{"nodeName":"","recordType":"A","state":false,group:"A","ipv4Address":"' + myip2 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupA + '/record/' + idRecordDns2GroupA + '',
                          headers=headers,
                          data=data)
            isEnableDNS = False
            print("# Disbale group A")
            # endregion disbale group A
            time.sleep(60)

        # region config AWS
        ConfigAWS(region_config_group_A_ubuntu_1, "Group A _ubuntu_1")
        ConfigAWS(region_config_group_A_ubuntu_2, "Group A _ubuntu_2")
        # endregion config AWS
        # region Stop AWS server A
        StopServer("Ubuntu-1", "Group A", False)
        StopServer("Ubuntu-2", "Group A", False)
        # endregion Stop AWS server A
        # region Start AWS server A
        StartServer("Ubuntu-1", "Group A server Ubuntu-1")
        StartServer("Ubuntu-2", "Group A server Ubuntu-2")
        # endregion Start AWS server A
        IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
        print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
        IP_ubuntu_2 = GetIPService("Ubuntu-2", "Group A server Ubuntu-2")
        print("******* Group A server Ubuntu-2 : " + IP_ubuntu_2)

        time.sleep(60)
        print("*******************CHECK Group A Ubuntu-1 IP: " + CheckFilterServer(IP_ubuntu_1, "Group A"))
        # if ping is false
        if CheckFilterServer(IP_ubuntu_1, "Group A") == 'false':
           while  True:
               StopServer("Ubuntu-1", "Group A", False)

               StartServer("Ubuntu-1", "Group A server Ubuntu-1")
               IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
               print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
               if IP_ubuntu_1 == 'true':
                   break

        print("*******************CHECK Group A Ubuntu-2 IP: " + CheckFilterServer(IP_ubuntu_2, "Group A"))
        # if ping is false
        if CheckFilterServer(IP_ubuntu_2, "Group A") == 'false':
            while True:
                StopServer("Ubuntu-2", "Group A", False)
                StartServer("Ubuntu-2", "Group A server Ubuntu-1")
                IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
                print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
                if IP_ubuntu_1 == 'true':
                    break




        if CheckFilterServer(IP_ubuntu_1, "server 1") == 'true' and \
                CheckFilterServer(IP_ubuntu_2, "server 2") == 'true':


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
            print("# Update DNS ip Group A")
            # endregion update ip dns server

            countUbuntu = 1
            firstTimeDisableA = 0
            isEnableDNS = True
            time.sleep(300)

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
            data = '{"nodeName":"","recordType":"A","state":false,group:"B","ipv4Address":"' + myip1 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns1GroupB + '',
                         headers=headers,
                         data=data)
            data = '{"nodeName":"","recordType":"A","state":false,group:"B","ipv4Address":"' + myip2 + '"}'
            requests.post('https://api.dynu.com/v2/dns/' + idDns1GroupB + '/record/' + idRecordDns2GroupB + '',
                         headers=headers,
                         data=data)
            isEnableDNS = False
            print("# Disbale group B")
            # endregion disbale group B
            time.sleep(60)



        # region config AWS
        ConfigAWS(region_config_group_B_ubuntu_3, "Group B _ubuntu_3")
        ConfigAWS(region_config_group_B_ubuntu_4, "Group B _ubuntu_4")
        # endregion config AWS
        # region Stop AWS server A
        StopServer("Ubuntu-3", "Group B server Ubuntu-3", False)
        StopServer("Ubuntu-4", "Group B server Ubuntu-4", False)
        # endregion Stop AWS server A
        # region Start AWS server A
        StartServer("Ubuntu-3", "Group B server Ubuntu-3")
        StartServer("Ubuntu-4", "Group B server Ubuntu-4")
        # endregion Start AWS server A
        IP_ubuntu_3 = GetIPService("Ubuntu-3", "Group B")
        print("******* Group B server Ubuntu-3 : " + IP_ubuntu_3)
        IP_ubuntu_4 = GetIPService("Ubuntu-4", "Group B")
        print("******* Group B server Ubuntu-4 : " + IP_ubuntu_4)

        time.sleep(60)
        print("*******************CHECK Group B Ubuntu-3 IP: " + CheckFilterServer(IP_ubuntu_3, "Group B"))
        # if ping is false
        if CheckFilterServer(IP_ubuntu_3, "Group B") == 'false':
            while True:
                StopServer("Ubuntu-1", "Group A", False)
                StartServer("Ubuntu-1", "Group A server Ubuntu-1")
                IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
                print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
                if IP_ubuntu_1 == 'true':
                    break
        print("*******************CHECK Group B Ubuntu-4 IP: " + CheckFilterServer(IP_ubuntu_4, "Group B"))
        # if ping is false
        if CheckFilterServer(IP_ubuntu_4, "Group B") == 'false':
            while True:
                StopServer("Ubuntu-1", "Group A", False)
                StartServer("Ubuntu-1", "Group A server Ubuntu-1")
                IP_ubuntu_1 = GetIPService("Ubuntu-1", "Group A server Ubuntu-1")
                print("******* Group A server Ubuntu-1  : " + IP_ubuntu_1)
                if IP_ubuntu_1 == 'true':
                    break
        if CheckFilterServer(IP_ubuntu_3, "Group B") == 'true' and \
                CheckFilterServer(IP_ubuntu_4, "Group B") == 'true':

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
            print("# Update DNS ip Group B")
            # endregion update ip dns server

            countUbuntu = 0
            firstTimeDisableB = 0
            isEnableDNS = True
            time.sleep(300)

        else:
            print('# Error ip ping Group B')
