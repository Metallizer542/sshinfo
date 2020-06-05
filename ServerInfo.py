import paramiko
import socket

class ServerInfo():

    bad_chars = ['\n', '\'', '[', ']']
    homedirectory = str()


    def getSShConnection(host, user, password, port):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(host, port, user, password)
        getHomeDirectory(client)
        return client


    def getHomeDirectory(client):
        directory = ExecCommandOnRemoteServer(client, 'pwd')
        homedirectory = str(directory[0].replace('\n', ''))

    def ExecCommandOnRemoteServer(client, command):
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.readlines()

    def getCpuFreqInfo(client):
        data = set(ExecCommandOnRemoteServer(client, 'cat /proc/cpuinfo |grep MHz'))
        cpuTempList = []
        for x in data:
            cpuTempList.append(x)
        CpuMhzTemp = filter(str.isdigit, str(cpuTempList[0]))
        CpuMhz = int("".join(CpuMhzTemp))
        freq = round(CpuMhz/1000000, 1)
        return str(freq)

    def getCpuCoresInfo(client):
        data = set(ExecCommandOnRemoteServer(client, 'cat /proc/cpuinfo |grep cores'))
        CpuTempCoresList = []
        for x in data:
            CpuTempCoresList.append(x)
        CpuTempCores = filter(str.isdigit, str(CpuTempCoresList[0]))
        CpuCores = int("".join(CpuTempCores))
        return str(CpuCores)

    def getMemInfo(client):
        memTotalTemp = str(ExecCommandOnRemoteServer(client, 'cat /proc/meminfo |grep MemTotal'))
        tempData = filter(str.isdigit, memTotalTemp)
        memTotal = int("".join(tempData))
        mem = round(memTotal/1000000, 1)
        return str(mem)

    def getOsCoreInfo(client):
        ExecCommandOnRemoteServer(client, ' touch ' + homedirectory + '/linux_Core.txt')
        ExecCommandOnRemoteServer(client, 'awk \'{print $1,$2,$3}\' /proc/version >' + homedirectory +'/linux_Core.txt')
        RawLinuxCoreVerion = readRemoteFile(client, homedirectory +'/linux_Core.txt')
        LinuxCoreVersion = []
        for x in RawLinuxCoreVerion:
            LinuxCoreVersion.append(x)
        ExecCommandOnRemoteServer(client, ' rm -f '+ homedirectory +'/linux_Core.txt')
        return str(LinuxCoreVersion[0])

    def getOsInfo(client):
        ExecCommandOnRemoteServer(client, ' touch '+ homedirectory +'/сentos.txt')
        ExecCommandOnRemoteServer(client, 'cat /etc/centos-release > '+ homedirectory +'/сentos.txt')
        RawOSVersion = readRemoteFile(client, homedirectory +'/сentos.txt')
        OsVersion = []

        for x in RawOSVersion:
            OsVersion.append(x)
        ExecCommandOnRemoteServer(client, ' rm -f '+ homedirectory +'/сentos.txt')
        return str(OsVersion[0])

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
        RawFdiskInfoSize = ExecCommandOnRemoteServer(client, 'df -h --output=size')
        dfdiskInfoSize = ''.join(i for i in RawFdiskInfoSize if not i in bad_chars)
        list = dfdiskInfoSize.split("\n")
        return list

    def dfDiskFileSystemInfo(client):
        RawFdiskInfoFileSystem = (ExecCommandOnRemoteServer(client, 'df -h --output=source'))
        dfdiskInfoFileSystem = ''.join(i for i in RawFdiskInfoFileSystem if not i in bad_chars)
        list = dfdiskInfoFileSystem.split("\n")
        return list

    def getServerName(client):
        RawServerName = ExecCommandOnRemoteServer(client, 'cat /proc/sys/kernel/hostname')
        serverName = ''.join(i for i in RawServerName if not i in bad_chars)
        return serverName

    def getIpAddress(client):
        ExecCommandOnRemoteServer(client, 'touch + ' + homedirectory +'/ip.txt')
        ExecCommandOnRemoteServer(client, 'sudo ip -4 addr | grep "inet" | awk {\'print $2\'} >' + homedirectory + '/ip.txt')
        RawIpInfo = (ExecCommandOnRemoteServer(client, 'cat /' + homedirectory +'/ip.txt'))
        ExecCommandOnRemoteServer(client, ' rm -f '+ homedirectory +'/ip.txt')
        return RawIpInfo[1]

    def getBaseProgramEnv(client):

        BaseProgramEnv = ['wildfly', 'tomcat', 'postgresql', 'logstash', 'zabbix', 'kibana', 'artemis', 'solr', 'haproxy', 'nginx', 'elasticsearch']
        ExecCommandOnRemoteServer(client, ' touch '+ homedirectory +'/java_version.txt')
        ExecCommandOnRemoteServer(client, ' touch '+ homedirectory +'/installed_services.txt')
        ExecCommandOnRemoteServer(client, 'ls /etc/systemd/system  >> '+ homedirectory +'/installed_services.txt')
        ExecCommandOnRemoteServer(client, 'ls /usr/lib/systemd/system >>' + homedirectory +'/installed_services.txt')
        tempInfo = readRemoteFile(client, homedirectory +'/installed_services.txt')
        BaseProgramInstalledServices = []

        for x in tempInfo:
            for y in BaseProgramEnv:
                if x.__contains__(y):
                    BaseProgramInstalledServices.append(str(x.replace('.service', '')))

        ExecCommandOnRemoteServer(client, ' java -version 2>'+ homedirectory +'/java_version.txt')
       # javatmp = readRemoteFile(client, + homedirectory +'/java_version.txt')
        ExecCommandOnRemoteServer(client, ' rm -f '+ homedirectory +'/installed_services.txt')
        ExecCommandOnRemoteServer(client, ' rm -f '+ homedirectory +'/java_version.txt')

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

