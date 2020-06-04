import jinja2
import simpletable
import ServerInfo
from tabulate import tabulate
import math

class HtmlGen():

    def getHTMLTable(table):
        tableForm = (tabulate(table, tablefmt='html'))
        return tableForm

    def fstabInfoHtml(client):
        sftp_client = client.open_sftp()
        fstab = ServerInfo.ServerInfo.getFsTabInfo(sftp_client)
        return HtmlGen.getHTMLTable(fstab)

    def CPUinfoHtml(client):
        freq = str(ServerInfo.ServerInfo.getCpuFreqInfo(client))
        cores = str(ServerInfo.ServerInfo.getCpuCoresInfo(client))
        table = [['CPU frequency', 'CPU cores'], [freq + " GHZ", cores]]
        return HtmlGen.getHTMLTable(table)

    def MemoryInfoHtml(client):
        mem = str(ServerInfo.ServerInfo.getMemInfo(client))
        table = [['Memory size'], [mem + " GB", ]]
        return HtmlGen.getHTMLTable(table)


    def OsInfoHtml(client):
        osLinuxCore = ServerInfo.ServerInfo.getOsCoreInfo(client)
        osVersion = ServerInfo.ServerInfo.getOsInfo(client)
        table = [['ОС', 'Версия ядра Linux'], [osVersion, osLinuxCore]]
        return HtmlGen.getHTMLTable(table)


    def HDDInfoHtml(filepath, client):
        file = open(filepath, 'w')
        file.write('<h4> Hard Disk Info </h4>' + '\n')
        hddSizeInfo = ServerInfo.ServerInfo.dfDiskSizeInfo(client)
        hddSourceInfo = ServerInfo.ServerInfo.dfDiskSourceInfo(client)
        list = []
        x = 0
        while x < len(hddSizeInfo):
            list.append(hddSourceInfo[x] + hddSizeInfo[x])
            x = x + 1

        file.write('<table border="1">')
        file.write('<thead>')
        file.write('<tr>')
        file.write('<th> Файловая система </th>')
        file.write('<th> Размер </th>')
        file.write('</tr>')
        file.write('</thead>')
        file.write('<tbody>')
        x = 1
        while x < len(list):
            file.write('<tr>')
            file.write('<td>' + hddSourceInfo[x] + '</td>' + '\n')
            file.write('<td>' + hddSizeInfo[x] + '</td>' + '\n')
            file.write('</tr>')
            if x == len(list) - 2:
                break
            x = x + 1

        file.write('</tbody>')
        file.write('</table>')
        file.close()


    def ServerAddresseInfoHtml(client):
        ip = ServerInfo.ServerInfo.getIpAddress(client)
        table = [['Внутренний IP адрес '], [ip]]
        return HtmlGen.getHTMLTable(table)


    def ServerNameInfoHtml(client):
        serverName = ServerInfo.ServerInfo.getServerName(client)
        table = [['Имя Сервера '], [serverName]]
        return HtmlGen.getHTMLTable(table)

    def BaseProgrammInstalledHtml(client):
        programInfo = ServerInfo.ServerInfo.getBaseProgramEnv(client)
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



