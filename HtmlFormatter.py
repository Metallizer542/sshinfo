from HtmlGen import HtmlGen
import ServerInfo
from string import ascii_letters, whitespace

host = '169.254.10.67'
user = 'intertrust'
password = '39CgjVfkHtf<ea'
port = 3322
client = ServerInfo.ServerInfo.getSShConnection(host, user, password, port)
filepath = '/Users/daniilkutyrev/Desktop/test.html'


def generateHtmlTableHeader():
    file = open('/Users/daniilkutyrev/Desktop/test.html', 'w')
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
    file.write('</tr>')
    file.write('</thead>')
    generateHTMLTableBody(file, client)
    file.write('</table')
    file.close()


def generateHTMLTableBody(file, client):
    baseProgram = HtmlGen.BaseProgrammInstalledHtml(client)
    file.write('<tbody>')
    file.write('<tr>')
    file.write('<td>' + HtmlGen.ServerNameInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.ServerAddresseInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + 'SSH: User - ' + user + '\n' + 'Password - ' + password + '</td>' + '\n')
    file.write('<td>' + HtmlGen.OsInfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.CPUinfoHtml(client) + '</td>' + '\n')
    file.write('<td>' + HtmlGen.MemoryInfoHtml(client) + '</td>' + '\n')
    for x in baseProgram:
        file.write('<td>' + x + '</td>')
    #HtmlGen.BaseProgrammInstalledHtml(client)
    file.write('</tr>')
    file.write('</tbody')

generateHtmlTableHeader()





