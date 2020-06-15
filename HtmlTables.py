from GetServerInfo import GetServerInfo
from tabulate import tabulate


class HtmlTables():

    def getHTMLTable(table):
        tableForm = (tabulate(table, tablefmt='html'))
        return tableForm

    def fstabInfoHtml(client):
        sftp_client = client.open_sftp()
        fstab = GetServerInfo.getFsTabInfo(sftp_client)
        return HtmlTables.getHTMLTable(fstab)

    def CPUinfoHtml(client):
        freq = str(GetServerInfo.getCpuFreqInfo(client))
        cores = str(GetServerInfo.getCpuCoresInfo(client))
        table = [['CPU frequency', 'CPU cores'], [freq + " GHZ", cores]]
        return HtmlTables.getHTMLTable(table)

    def MemoryInfoHtml(client):
        mem = str(GetServerInfo.getMemInfo(client))
        table = [['Memory size'], [mem + " GB", ]]
        return HtmlTables.getHTMLTable(table)


    def OsInfoHtml(client):
        osLinuxCore = GetServerInfo.getOsCoreInfo(client)
        osVersion = GetServerInfo.getOsInfo(client)
        table = [['ОС', 'Версия ядра Linux'], [osVersion, osLinuxCore]]
        return HtmlTables.getHTMLTable(table)


    def HDDInfoHtml(client):

        hddSizeInfo = GetServerInfo.getDiskSizeInfo(client)
        hddSourceInfo =GetServerInfo.getDiskFileSystemInfo(client)
        listTmpInfo = []
        list2HddInfo = []

        x = 0
        while x < len(hddSizeInfo):
            listTmpInfo.append(hddSourceInfo[x] + hddSizeInfo[x])
            x = x + 1

        list2HddInfo.append('<table>')
        list2HddInfo.append('<tbody>')
        list2HddInfo.append('<tr>')
        list2HddInfo.append('<th> <b> Файловая система </b> </th>')
        list2HddInfo.append('<th> <b> Размер </b> </th>')
        list2HddInfo.append('</tr>')

        x = 1
        while x < len(listTmpInfo):
            list2HddInfo.append('<tr>')
            list2HddInfo.append('<td>' + hddSourceInfo[x] + '</td>' + '\n')
            list2HddInfo.append('<td>' + hddSizeInfo[x] + '</td>' + '\n')
            list2HddInfo.append('</tr>')
            if x == len(listTmpInfo) - 2:
                break
            x = x + 1

        list2HddInfo.append('</tbody>')
        list2HddInfo.append('</table>')
        return list2HddInfo


    def ServerAddresseInfoHtml(client):
        ip = GetServerInfo.getIpAddress(client)
        table = [['Внутренний IP адрес '], [ip]]
        return HtmlTables.getHTMLTable(table)


    def ServerNameInfoHtml(client):
        serverName = GetServerInfo.getServerName(client)
        table = [['Имя Сервера '], [serverName]]
        return HtmlTables.getHTMLTable(table)

    def BaseProgrammInstalledHtml(client):
        programList = GetServerInfo.getBaseProgramEnv(client)

        ProgramListHtml = []
        ProgramListHtml.append('<table>')
        ProgramListHtml.append('<tbody>')

        for x in programList:
            ProgramListHtml.append('<tr>')
            ProgramListHtml.append('<td>' + x.replace('.service', '') + '</td>' + '\n')
            ProgramListHtml.append('</tr>')

        ProgramListHtml.append('</tbody>')
        ProgramListHtml.append('</table>')
        return ProgramListHtml



