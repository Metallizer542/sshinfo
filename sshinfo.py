import sys
import paramiko
from tabulate import tabulate

bad_chars = ['\n', '\'', '[', ']']
homedirectory = str()

def startProgram():

    if sys.argv[1] == '-h' or sys.argv[1] == '--hosts':
        file = open(sys.argv[2], 'r')
        list_servers = []
        try:
            for line in file:
                list_servers.append(line.replace('\n', ' '))
        finally:
            file.close()
        list_tmp = []
        for x in list_servers:
            list_tmp.append(x.split(':'))

        listAddresses = []
        for x in list_tmp:
            listAddresses.append(x[0])

        listPorts = []
        for x in list_tmp:
            listPorts.append(int(x[1]))
    else:
        print('Не задан путь к фалу списка серверов')
        sys.exit(1)


    if sys.argv[3] == '-u' or sys.argv[3] == '--user':
        user = sys.argv[4]
    else:
       print('Не задан параметр имени пользователя')
       sys.exit(1)

    if sys.argv[5] == '-p' or sys.argv[5]== '--password':
        password = sys.argv[6]
    else:
        print('Не задан параметр пароля пользователя')
        sys.exit(1)

    if sys.argv[7] == '-o' or sys.argv[7] == '--output':
        outputFilePath = sys.argv[8]
    else:
        print('Не задан путь для файла вывода')
        sys.exit(1)

    generateHtmlTableHeader(listAddresses, user, password, listPorts, outputFilePath)

def generateHtmlTableHeader(hosts,user,password,ports,filepath):
    file = open(filepath, 'w')
    file.write('<table border="1">')
    file.write('<thead>')
    file.write('<tr>')
    file.write('<th> Узел </th>')
    file.write('<th> Адрес </th>')
    file.write('<th> Учетные данные для подключения </th>')
    file.write('<th> Операционная система </th>')
    file.write('<th> CPU </th>')
    file.write('<th> RAM </th>')
    file.write('<th> Установленное ПО </th>')
    file.write('<th> HDD </th>')
    file.write('</tr>')
    file.write('</thead>')
    x = 0
    while(x<len(hosts)):
        client = getSShConnection(hosts[x], user, password, ports[x])
        generateHTMLTableBody(file, client, hosts[x], ports[x], user, password)
        x = x + 1
    file.write('</table')
    file.close()


def generateHTMLTableBody(file, client, host, port, user, password):
    baseProgram = BaseProgrammInstalledHtml(client)
    hddInfo=HDDInfoHtml(client)
    file.write('<tbody>')
    file.write('<tr>')
    file.write('<td>' + ServerNameInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + ServerAddresseInfoHtml(client) + '</br>' + 'SSH из сети Интертраст </br>' + host + ':' + str(port) + '</td>' + '\n')
    file.write('<td>' + 'SSH: User - ' + user + '</br>' + ' Password - ' + password + '</td>' + '\n')
    file.write('<td>' + OsInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + CPUinfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + MemoryInfoHtml(client) + '</td>' + '\n')
    for x in baseProgram:
        file.write('<td>' + x + '</td>')
    for x in hddInfo:
        file.write('<td>' + x + '</td>')
    file.write('</tr>')
    file.write('</tbody')

def getHTMLTable(table):
        tableForm = (tabulate(table, tablefmt='html'))
        return tableForm

def fstabInfoHtml(client):
        sftp_client = client.open_sftp()
        fstab = getFsTabInfo(sftp_client)
        return getHTMLTable(fstab)

def CPUinfoHtml(client):
        freq = str(getCpuFreqInfo(client))
        cores = str(getCpuCoresInfo(client))
        table = [['CPU frequency', 'CPU cores'], [freq + " GHZ", cores]]
        return getHTMLTable(table)

def MemoryInfoHtml(client):
        mem = str(getMemInfo(client))
        table = [['Memory size'], [mem + " GB", ]]
        return getHTMLTable(table)


def OsInfoHtml(client):
        osLinuxCore = getOsCoreInfo(client)
        osVersion = getOsInfo(client)
        table = [['ОС', 'Версия ядра Linux'], [osVersion, osLinuxCore]]
        return getHTMLTable(table)


def HDDInfoHtml(client):

        hddSizeInfo = dfDiskSizeInfo(client)
        hddSourceInfo = dfDiskFileSystemInfo(client)
        list = []
        list2 = []
        x = 0
        while x < len(hddSizeInfo):
            list.append(hddSourceInfo[x] + hddSizeInfo[x])
            x = x + 1

        list2.append('<table>')
        list2.append('<tbody>')

        list2.append('<tr>')
        list2.append('<td> <b> Файловая система </b> </th>')
        list2.append('<td> <b> Размер </b> </th>')

        list2.append('</tr>')


        x = 1
        while x < len(list):
            list2.append('<tr>')
            list2.append('<td>' + hddSourceInfo[x] + '</td>' + '\n')
            list2.append('<td>' + hddSizeInfo[x] + '</td>' + '\n')
            list2.append('</tr>')
            if x == len(list) - 2:
                break
            x = x + 1
        list2.append('</tbody>')
        list2.append('</table>')
        return list2


def ServerAddresseInfoHtml(client):
        ip = getIpAddress(client)
        table = [['Внутренний IP адрес '], [ip]]
        return getHTMLTable(table)


def ServerNameInfoHtml(client):
        serverName = getServerName(client)
        table = [['Имя Сервера '], [serverName]]
        return getHTMLTable(table)

def BaseProgrammInstalledHtml(client):
        programInfo = getBaseProgramEnv(client)
        listHtml = []

        listHtml.append('<table>')
        listHtml.append('<tbody>')
        x = 1
        while x < len(programInfo):
            listHtml.append('<tr>')
            listHtml.append('<td>' + programInfo[x] + '</td>' + '\n')
            listHtml.append('</tr>')
            if x == len(programInfo) - 2:
                break
            x = x + 1
        listHtml.append('</tbody>')
        listHtml.append('</table>')
        return listHtml
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

startProgram()