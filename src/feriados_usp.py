from datetime import date as dt
import requests
from bs4 import BeautifulSoup
import re

feriados = {}

meses_pt = {
    'Janeiro': 1,
    'Fevereiro': 2,
    'Março': 3,
    'Abril': 4,
    'Maio': 5,
    'Junho': 6,
    'Julho': 7,
    'Agosto': 8,
    'Setembro': 9,
    'Outubro': 10,
    'Novembro': 11,
    'Dezembro': 12
}

calendario = 'https://uspdigital.usp.br/jupiterweb/jupCalendario2021.jsp'

pagina = requests.get(calendario)
soup = BeautifulSoup(pagina.content, 'html.parser')
tabelas = soup.find_all('table','table_border')
tabelas = tabelas[:-6] # Remove os meses de 2022

for tabela in tabelas:
    linhas = tabela.find_all('tr')
    mes = linhas[0].find('div').get_text().strip()
    linhas = linhas[1:] # Remove a primeira linha, pois é apenas o nome do mês
    for linha in linhas:
        colunas = linha.find_all('td')
        data = colunas[0].get_text().strip().replace('º','')
        data = re.sub('\\r\\n +', ' ', data)
        texto = colunas[1].get_text().strip()
        texto = re.sub('\\r\\n +', ' ', texto)
        if texto.find('Não haverá aula') != -1:
            texto = re.search('^[^-.]+',texto)[0].strip()
            dia = re.search('\d+',data)[0]
            feriados[dt(2021,meses_pt.get(mes),int(dia))] = texto

print(feriados)
