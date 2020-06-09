from HtmlGen import HtmlGen
from ServerInfo import ServerInfo


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
        client = ServerInfo.getSShConnection(hosts[x], user, password, ports[x])
        generateHTMLTableBody(file, client, hosts[x], ports[x], user, password)
        x = x + 1
    file.write('</table')
    file.close()


def generateHTMLTableBody(file, client, host, port, user, password):
    baseProgram = HtmlGen.BaseProgrammInstalledHtml(client)
    hddInfo=HtmlGen.HDDInfoHtml(client)
    file.write('<tbody>')
    file.write('<tr>')
    file.write('<td>' + HtmlGen.ServerNameInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.ServerAddresseInfoHtml(client) + '</br>' + 'SSH из сети Интертраст </br>' + host + ':' + str(port) + '</td>' + '\n')
    file.write('<td>' + 'SSH: User - ' + user + '</br>' + ' Password - ' + password + '</td>' + '\n')
    file.write('<td>' + HtmlGen.OsInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.CPUinfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.MemoryInfoHtml(client) + '</td>' + '\n')
    for programm in baseProgram:
        file.write('<td>')
        file.write(programm)
        file.write('</td>')
    for hdd in hddInfo:
        file.write('<td>')
        file.write(hdd)
        file.write('</td>')
    file.write('</tr>')
    file.write('</tbody>')





