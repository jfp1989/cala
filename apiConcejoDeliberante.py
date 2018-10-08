from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

@app.route("/file/<numero_expediente>")
def getData(id):
    url = "http://www.concejodeliberante.laplata.gov.ar/MesaEntradas/expediente.asp?Numero={}&Buscar=Enviar".format(numero_expediente)
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    #falta refactorizar
    expediente = {
        "id": [text for text in soup.table.find_all('tr')[0].find_all('li')[0].stripped_strings][1],
        "started": [text for text in soup.table.find_all('tr')[0].find_all('li')[1].stripped_strings][1],
        "started_date": [text for text in soup.table.find_all('tr')[0].find_all('li')[2].stripped_strings][1],
        "presentation_type": [text for text in soup.table.find_all('tr')[0].find_all('li')[3].stripped_strings][1],
        "detail": [text for text in soup.table.find_all('tr')[0].find_all('li')[4].stripped_strings][1],
        "status": [text for text in soup.table.find_all('tr')[1].find_all('li')[0].stripped_strings][1],
        "last_update": soup.table.find_all('tr')[1].find_all('li')[1].get_text().split(':')[1].replace(u'\xa0',''),
        "resolution_id": soup.table.find_all('tr')[1].find_all('li')[2].get_text().split(':')[1].replace(u'\xa0','').replace(u'\xb0','')
    }
    return expediente
    #print(expediente)

if __name__ == '__main__':
    app.run(debug= True, port= 8000 )