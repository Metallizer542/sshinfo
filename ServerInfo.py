import paramiko
import socket

class ServerInfo():

    bad_chars = ['\n', '\'', '[', ']']

    def getSShConnection(host, user, password, port):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(host, port, user, password)
        return client

    def ExecCommandOnRemoteServer(client, command):
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.readlines()

    def getCpuFreqInfo(client):
        data = set(ServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/cpuinfo |grep MHz'))
        cpuTempList = []
        for x in data:
            cpuTempList.append(x)
        CpuMhzTemp = filter(str.isdigit, str(cpuTempList[0]))
        CpuMhz = int("".join(CpuMhzTemp))
        freq = round(CpuMhz/1000000, 1)
        return str(freq)

    def getCpuCoresInfo(client):
        data = set(ServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/cpuinfo |grep cores'))
        CpuTempCoresList = []
        for x in data:
            CpuTempCoresList.append(x)
        CpuTempCores = filter(str.isdigit, str(CpuTempCoresList[0]))
        CpuCores = int("".join(CpuTempCores))
        return str(CpuCores)

    def getMemInfo(client):
        memTotalTemp = str(ServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/meminfo |grep MemTotal'))
        tempData = filter(str.isdigit, memTotalTemp)
        memTotal = int("".join(tempData))
        mem = round(memTotal/1000000, 1)
        return str(mem)

    def getOsCoreInfo(client):
        RawLinuxCoreVersion = str(ServerInfo.ExecCommandOnRemoteServer(client, 'awk \'{print $1,$2,$3}\' /proc/version'))
        LinuxCoreVersion = ''.join(i for i in RawLinuxCoreVersion if not i in ServerInfo.bad_chars)
        return str(LinuxCoreVersion)

    def getOsInfo(client):
        RawOSVersion = str(ServerInfo.ExecCommandOnRemoteServer(client, 'cat /etc/centos-release |tr -s ''\r\n'' ' ''))
        OsVersion = ''.join(i for i in RawOSVersion if not i in ServerInfo.bad_chars)
        return str(OsVersion)

    def getFsTabInfo(client):
       remote_file = client.open('/etc/fstab')
       file = []
       try:
           for line in remote_file:
               if not line.startswith("#"):
                   file.append(line.replace('\n''', ' '))
           return file
       finally:
           remote_file.close()

    def dfDiskSizeInfo(client):
        RawFdiskInfoSize = ServerInfo.ExecCommandOnRemoteServer(client, 'df -h --output=size')
        dfdiskInfoSize = ''.join(i for i in RawFdiskInfoSize if not i in ServerInfo.bad_chars)
        list = dfdiskInfoSize.split("\n")
        return list

    def dfDiskSourceInfo(client):
        RawFdiskInfoSource = (ServerInfo.ExecCommandOnRemoteServer(client, 'df -h --output=source'))
        dfdiskInfoSource = ''.join(i for i in RawFdiskInfoSource if not i in ServerInfo.bad_chars)
        list = dfdiskInfoSource.split("\n")
        return list

    def getServerName(client):
        RawServerName = ServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/sys/kernel/hostname')
        serverName = ''.join(i for i in RawServerName if not i in ServerInfo.bad_chars)
        return serverName

    def getIpAddress(client):
        ServerInfo.ExecCommandOnRemoteServer(client, 'touch /home/intertrust/ip.txt')
        ServerInfo.ExecCommandOnRemoteServer(client, 'sudo ip -4 addr | grep "inet" | awk {\'print $2\'} | tee /home/intertrust/ip.txt')
        RawIpInfo = (ServerInfo.ExecCommandOnRemoteServer(client, 'cat /home/intertrust/ip.txt'))
        ServerInfo.ExecCommandOnRemoteServer(client, 'sudo rm -f /home/intertrust/ip.txt')
        return RawIpInfo[1]

    def getBaseProgramEnv(client):

        BaseProgramEnv = ['wildfly', 'tomcat', 'postgresql', 'logstash', 'zabbix', 'kibana', 'artemis', 'solr', 'haproxy', 'nginx', 'elasticsearch']
        ServerInfo.ExecCommandOnRemoteServer(client, 'touch /home/intertrust/java_version.txt')
        ServerInfo.ExecCommandOnRemoteServer(client, 'touch /home/intertrust/installed_services.txt')
        ServerInfo.ExecCommandOnRemoteServer(client, 'ls /etc/systemd/system  >> /home/intertrust/installed_services.txt')
        ServerInfo.ExecCommandOnRemoteServer(client, 'ls /usr/lib/systemd/system >> /home/intertrust/installed_services.txt')
        tempInfo = ServerInfo.readRemoteFile(client, '/home/intertrust/installed_services.txt')
        BaseProgramInstalledServices = []

        for x in tempInfo:
            for y in BaseProgramEnv:
                if x.__contains__(y):
                    BaseProgramInstalledServices.append(str(x.replace('.service', '')))

        ServerInfo.ExecCommandOnRemoteServer(client, 'sudo java -version 2>/home/intertrust/java_version.txt')
        javatmp = ServerInfo.readRemoteFile(client, '/home/intertrust/java_version.txt')
        BaseProgramInstalledServices.append(javatmp[0])
        ServerInfo.ExecCommandOnRemoteServer(client, 'sudo rm -f /home/intertrust/installed_services.txt')
        ServerInfo.ExecCommandOnRemoteServer(client, 'sudo rm -f /home/intertrust/java_version.txt')

        return BaseProgramInstalledServices

    def readRemoteFile(client, filepath):
        sftp_client = client.open_sftp()
        remote_file = sftp_client.open(filepath)
        file = []
        try:
            for line in remote_file:
                file.append(line.replace('\n', ' '))
            return file
        finally:
            remote_file.close()

