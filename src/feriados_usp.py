from datetime import date as dt
import requests
from bs4 import BeautifulSoup
import re

feriados = {}
aulas = {}
matri = {}

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
        elif texto.find('DAS AULAS') != -1:
            texto = re.search('^[^-.]+',texto)[0].strip()
            dia = re.search('\d+',data)[0]
            aulas[dt(2021,meses_pt.get(mes),int(dia))] = texto
        elif texto.find('nteração') != -1 or texto.find('trancamento') != -1:
            texto = re.search('^[^-.]+',texto)[0].strip()
            dia = re.search('\d+',data)[0]
            matri[dt(2021,meses_pt.get(mes),int(dia))] = texto 

#print(feriados)
#print(aulas)
#print(matri)

# {
#     datetime.date(2021, 4, 21): 'Tiradentes',
#     datetime.date(2021, 5, 1): 'Dia do Trabalho',
#     datetime.date(2021, 6, 3): 'Corpus Christi',
#     datetime.date(2021, 6, 4): 'Recesso (Corpus Christi)',
#     datetime.date(2021, 7, 9): 'Revolução  Constitucionalista de 1932',
#     datetime.date(2021, 7, 10): 'Recesso (Revolução  Constitucionalista de 1932)',
#     datetime.date(2021, 9, 6): 'Recesso (Independência do Brasil)',
#     datetime.date(2021, 9, 7): 'Independência do Brasil',
#     datetime.date(2021, 10, 29): 'Recesso (Consagração ao Funcionário Público)',
#     datetime.date(2021, 11, 1): 'Recesso (Finados)',
#     datetime.date(2021, 11, 2): 'Finados'
# }

