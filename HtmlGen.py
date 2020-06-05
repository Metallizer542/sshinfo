import ServerInfo
from tabulate import tabulate


class HtmlGen():

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



