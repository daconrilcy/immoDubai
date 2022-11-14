from datetime import datetime
import requests
import pandas as pd
from baseconstants import AED_IN_EURO, USD_IN_EURO, PATH_REP_HISTORY_FILE, URL_CONVERSION_BOURSORAMA


def requestboursorama(currency_name="AED", curto="EUR", tx_default=AED_IN_EURO):
    curfrom = currency_name
    print("mise à jour de taux de conversion " + curfrom + "/" + curto)
    reqfrom = "from=" + curfrom
    reqto = "&to=" + curto
    reqamount = "&amount=1"
    fullrequest = URL_CONVERSION_BOURSORAMA + reqfrom + reqto + reqamount
    response = requests.get(fullrequest)
    if response:
        return response.json()['convertedAmount']
    else:
        return tx_default


class Currency:
    def __init__(self, name="", conveteuros=1.00, filename=""):
        self.name = name
        self.convert_in_euros = conveteuros
        self.history_file_name = filename

    def euro_value(self, val=1):
        return val * self.convert_in_euros

    def from_euro(self, val=1):
        return val / self.convert_in_euros


class FileCurrencyHistory:

    def __init__(self):
        self.file_name = ''
        self.cur_name = ''
        self.path = ''
        self.csvfile = None
        self.last_cour = 0.00
        self.today = datetime.now()

    def get_last_conversion_rate(self, currencie=Currency()):
        self.cur_name = currencie.name
        self.set_file_name(currencie.history_file_name)
        self.set_file_history()
        self.last_cour = requestboursorama(currencie.name, "EUR", currencie.convert_in_euros)
        if self.is_file_need_update():
            print('la valeur de convertion de ' + self.cur_name + ' a besoin d\'être mise à jour')
            self.updatefilehistory()
        else:
            self.csvfile.sort_values('date')
        return self.last_cour

    def update_conversion_rate(self):
        self.updatefilehistory()

    def updatefilehistory(self):
        toadd = pd.DataFrame([[self.today, self.last_cour]], columns=['date', 'value'])
        print("valeur ajoutée:", toadd['date'].values[0], toadd['value'].values[0])
        self.csvfile = pd.concat([self.csvfile, toadd], ignore_index=True)
        self.csvfile.reset_index()
        self.csvfile.to_csv(self.path, index_label="n")

    def set_file_name(self, filename):
        if (filename != '') & (filename is not None):
            self.file_name = filename
            self.set_path_file()

    def set_file_history(self):
        self.csvfile = pd.read_csv(self.path, parse_dates=['date'], index_col="n")

    def set_path_file(self):
        self.path = PATH_REP_HISTORY_FILE + self.file_name

    def is_file_need_update(self):
        if self.csvfile is not None:
            lastupdate = pd.to_datetime(max(self.csvfile['date'].values))
            if pd.Timedelta(self.today - lastupdate).days > 0:
                return True
        return False


class Currencies:
    aed = None
    usd = None


def mainfunction():
    filehisto = FileCurrencyHistory()
    currencies = Currencies()
    currencies.aed = Currency('AED', AED_IN_EURO, 'history_AED.csv')
    currencies.usd = Currency('USD', USD_IN_EURO, 'history_USD.csv')
    currencies.aed.convert_in_euros = filehisto.get_last_conversion_rate(currencies.aed)
    currencies.usd.convert_in_euros = filehisto.get_last_conversion_rate(currencies.usd)

    return currencies
