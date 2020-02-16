import urllib.request as request
import xml.etree.ElementTree as ET
from models import ExchangeModel

class CurrencyServices:

    def __getEuroBasedCurrencyRates(self):
        URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        namespaces = {
            "gesmes": "http://www.gesmes.org/xml/2002-08-01",
            "eurofxref": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref",
        }

        response = request.urlopen(URL).read()
        tree = ET.ElementTree(ET.fromstring(response))

        root = tree.getroot()
        currencyRates = []
        for child in root.findall("./eurofxref:Cube/eurofxref:Cube/eurofxref:Cube", namespaces):
            rate = float(child.attrib['rate'])
            currency = child.attrib['currency']
            base = 'EUR'
            exchange = ExchangeModel(base, currency, rate)

            currencyRates.append(exchange)

        return currencyRates

    def __getViceVersa(self, exchanges: [ExchangeModel]) -> [ExchangeModel]:
        newExchanges = []
        for exchange in exchanges:
            rate = 1 / exchange.rate
            base = exchange.currency
            currency = exchange.base
            newExchange = ExchangeModel(base, currency, rate)
            newExchanges.append(newExchange)
        return newExchanges

    def getAllCurrencyRates(self) -> [ExchangeModel]:
        euroCurrencyRates = self.__getEuroBasedCurrencyRates()
        allCurrencyRates = []

        for exchange1 in euroCurrencyRates:
            for exchange2 in euroCurrencyRates:
                if exchange1.currency == exchange2.currency:
                    continue
                rate = exchange1.rate / exchange2.rate
                base = exchange2.currency
                currency = exchange1.currency
                exchange = ExchangeModel(base, currency, rate)
                allCurrencyRates.append(exchange)
        allCurrencyRates.extend(euroCurrencyRates)
        euroCurrencyRatesViceVersa = self.__getViceVersa(euroCurrencyRates)
        allCurrencyRates.extend(euroCurrencyRatesViceVersa)

        return allCurrencyRates
#
# currencyService = CurrencyServices()
# rates = currencyService.getAllCurrencyRates()
# for exchange in rates:
#     print(exchange.toString)
