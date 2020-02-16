from pymongo import MongoClient
from models import ExchangeModel


class DatabaseService:
    __exchangesDoc = None
    __currencyDoc = None

    def __init__(self, mongo: MongoClient):
        self.__exchangesDoc = mongo.currency_db.exchanges
        self.__currencyDoc = mongo.currency_db.currencyCodes

    def saveAllExchanges(self, exchanges: [ExchangeModel]):
        mapToDict = lambda exchange: exchange.toDict
        exchangeAsDict = map(mapToDict, exchanges)
        self.__exchangesDoc.delete_many({})
        self.__exchangesDoc.insert_many(exchangeAsDict)


    def saveCurrencyCodes(self, currencyCodes: []):

        mapToDict = lambda code: dict(currency=code)
        codes = map(mapToDict,currencyCodes)
        self.__currencyDoc.delete_many({})
        self.__currencyDoc.insert_many(codes)

    def getCurrenciesCodes(self)->[str]:

        dbResult = self.__currencyDoc.find({})
        if dbResult == None:
            return []
        currencies = []
        for row in dbResult:
            currency = row['currency']
            currencies.append(currency)
        return currencies



    def getExchangeRatesOfCurrency(self,base)->[ExchangeModel]:
        dbResult = self.__exchangesDoc.find({"base": base})

        if dbResult == None:
            return []

        exchanges = []
        for row in dbResult:
            exchange = ExchangeModel(base,row['currency'],row['rate'])
            exchanges.append(exchange)

        return exchanges

    def getExchangeRatesOfCurrencies(self)->[ExchangeModel]:
        dbResult = self.__exchangesDoc.find({})

        if dbResult == None:
            return []

        exchanges = []
        for row in dbResult:
            exchange = ExchangeModel(row['base'],row['currency'],row['rate'])
            exchanges.append(exchange)

        return exchanges

    def getSpesificCurrencies(self,base,currency)->ExchangeModel:
        row = self.__exchangesDoc.find_one({"base":base,"currency":currency})


        return ExchangeModel(base,currency,row['rate'])

