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
        list = []
        list2 = []
        x = 0
        while x < len(hddSizeInfo):
            list.append(hddSourceInfo[x] + hddSizeInfo[x])
            x = x + 1

        list2.append('<table>')
        list2.append('<tbody>')

        list2.append('<tr>')
        list2.append('<th> <b> Файловая система </b> </th>')
        list2.append('<th> <b> Размер </b> </th>')

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
        ip = GetServerInfo.getIpAddress(client)
        table = [['Внутренний IP адрес '], [ip]]
        return HtmlTables.getHTMLTable(table)


    def ServerNameInfoHtml(client):
        serverName = GetServerInfo.getServerName(client)
        table = [['Имя Сервера '], [serverName]]
        return HtmlTables.getHTMLTable(table)

    def BaseProgrammInstalledHtml(client):
        programInfo = GetServerInfo.getBaseProgramEnv(client)
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



