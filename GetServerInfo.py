import paramiko
import logging
class GetServerInfo():

    bad_chars = ['\n', '\'', '[', ']']
    homedirectory = str()


    def getSShConnection(host, user, password, port):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(host, port, user, password)
        print('установлено соединение с сервером ' + host + ':' + port)
        GetServerInfo.getHomeDirectory(client)
        return client

    def getHomeDirectory(client):
        directory =GetServerInfo.ExecCommandOnRemoteServer(client, 'pwd')
        GetServerInfo.homedirectory = str(directory[0].replace('\n', ''))

    def ExecCommandOnRemoteServer(client, command):
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.readlines()

    def getCpuFreqInfo(client):
        data = set(GetServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/cpuinfo |grep MHz'))
        cpuTempList = []
        for x in data:
            cpuTempList.append(x)
        CpuMhzTemp = filter(str.isdigit, str(cpuTempList[0]))
        CpuMhz = int("".join(CpuMhzTemp))
        freq = round(CpuMhz/1000000, 1)
        print('получена информация о частоте cpu')
        return str(freq)

    def getCpuCoresInfo(client):
        data = set(GetServerInfo.ExecCommandOnRemoteServer(client, 'lscpu |grep \'CPU(s):\' |awk {\'print$2\'} |head -n1'))
        CpuTempCoresList = []
        for x in data:
            CpuTempCoresList.append(x)
        CpuTempCores = filter(str.isdigit, str(CpuTempCoresList[0]))
        CpuCores = int("".join(CpuTempCores))
        print('получена информация о количестве ядер cpu')
        return str(CpuCores)

    def getMemInfo(client):
        memTotalTemp = str(GetServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/meminfo |grep MemTotal'))
        tempData = filter(str.isdigit, memTotalTemp)
        memTotal = int("".join(tempData))
        mem = round(memTotal/1000000, 1)
        print('получена информация об объеме ОЗУ')
        return str(mem)

    def getOsCoreInfo(client):
        GetServerInfo.ExecCommandOnRemoteServer(client, ' touch ' + GetServerInfo.homedirectory + '/linux_Core.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, 'awk \'{print $1,$2,$3}\' /proc/version >' + GetServerInfo.homedirectory + '/linux_Core.txt')
        RawLinuxCoreVerion = GetServerInfo.readRemoteFile(client, GetServerInfo.homedirectory + '/linux_Core.txt')
        LinuxCoreVersion = []
        for x in RawLinuxCoreVerion:
            LinuxCoreVersion.append(x)
        GetServerInfo.ExecCommandOnRemoteServer(client, ' rm -f ' + GetServerInfo.homedirectory + '/linux_Core.txt')
        print('получена информация о ядре Linux')
        return str(LinuxCoreVersion[0])

    def getOsInfo(client):
        GetServerInfo.ExecCommandOnRemoteServer(client, ' touch ' + GetServerInfo.homedirectory + '/сentos.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, 'cat /etc/centos-release > ' + GetServerInfo.homedirectory + '/сentos.txt')
        RawOSVersion = GetServerInfo.readRemoteFile(client, GetServerInfo.homedirectory + '/сentos.txt')
        OsVersion = []

        for x in RawOSVersion:
            OsVersion.append(x)
        GetServerInfo.ExecCommandOnRemoteServer(client, ' rm -f ' + GetServerInfo.homedirectory + '/сentos.txt')
        print('получена информация о версии системы')
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

    def getDiskSizeInfo(client):
        RawFdiskInfoSize = GetServerInfo.ExecCommandOnRemoteServer(client, 'df -h --output=size')
        dfdiskInfoSize = ''.join(i for i in RawFdiskInfoSize if not i in GetServerInfo.bad_chars)
        list = dfdiskInfoSize.split("\n")
        print("получена информация об объеме hdd")
        return list

    def getDiskFileSystemInfo(client):
        RawFdiskInfoFileSystem = (GetServerInfo.ExecCommandOnRemoteServer(client, 'df -h --output=source'))
        dfdiskInfoFileSystem = ''.join(i for i in RawFdiskInfoFileSystem if not i in GetServerInfo.bad_chars)
        list = dfdiskInfoFileSystem.split("\n")
        print("получена информация об файловых системах hdd")
        return list

    def getServerName(client):
        RawServerName =GetServerInfo.ExecCommandOnRemoteServer(client, 'cat /proc/sys/kernel/hostname')
        serverName = ''.join(i for i in RawServerName if not i in GetServerInfo.bad_chars)
        print('получена информация об имени сервера')
        return serverName

    def getIpAddress(client):
        GetServerInfo.ExecCommandOnRemoteServer(client, '/usr/sbin/ip -4 addr | grep "inet" | awk {\'print $2\'} > $(pwd)/ip.txt')
        RawIpInfo = (GetServerInfo.ExecCommandOnRemoteServer(client, 'cat /' + GetServerInfo.homedirectory + '/ip.txt'))
        GetServerInfo.ExecCommandOnRemoteServer(client, 'rm -f ' + GetServerInfo.homedirectory + '/ip.txt')
        if(len(RawIpInfo)<1):
            print('возникли проблемы при получении ip адреса')
        print('получена информация об IP адресе ')
        return RawIpInfo[1]

    def getBaseProgramEnv(client):

        BaseProgramEnv = ['wildfly', 'tomcat', 'postgresql', 'logstash', 'zabbix', 'kibana', 'artemis', 'solr', 'haproxy', 'nginx', 'elasticsearch']
        GetServerInfo.ExecCommandOnRemoteServer(client, ' touch ' + GetServerInfo.homedirectory + '/java_version.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, ' touch ' + GetServerInfo.homedirectory + '/installed_services.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, 'ls /etc/systemd/system > ' + GetServerInfo.homedirectory + '/installed_services.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, 'ls /usr/lib/systemd/system >>' + GetServerInfo.homedirectory +'/installed_services.txt')
        tempInfo = GetServerInfo.readRemoteFile(client, GetServerInfo.homedirectory + '/installed_services.txt')
        BaseProgramInstalledServices = []


        for service in tempInfo:
            str1 = str(service)

            for base_program in BaseProgramEnv:
                str2 = str(base_program)
                if str1.__contains__(str2):
                    BaseProgramInstalledServices.append(str1)


        GetServerInfo.ExecCommandOnRemoteServer(client, 'java -version 2>' + GetServerInfo.homedirectory + '/java_version.txt')
        javatmp = GetServerInfo.readRemoteFile(client, GetServerInfo.homedirectory +'/java_version.txt')
        BaseProgramInstalledServices.append(javatmp[0])
        GetServerInfo.ExecCommandOnRemoteServer(client, 'rm -f ' + GetServerInfo.homedirectory +' /installed_services.txt')
        GetServerInfo.ExecCommandOnRemoteServer(client, 'rm -f ' + GetServerInfo.homedirectory + '/java_version.txt')
        print('получена информация об установленых сервисах')
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

