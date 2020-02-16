from flask import Flask, jsonify
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from eu_central_bank_currency_service import CurrencyServices
from datetime import datetime
from mongo_database_service import DatabaseService


app = Flask(__name__)
mongo = MongoClient("localhost", 27017)
databaseService = DatabaseService(mongo)


scheduler = BackgroundScheduler(daemon=True)
currencyService = CurrencyServices()

def currencyLoaderJob():
    currencyRates = currencyService.getAllCurrencyRates()
    mapToBase = lambda exchange: exchange.base

    currencies = map(mapToBase,currencyRates)
    currencies = set(currencies)
    databaseService.saveCurrencyCodes(currencies)
    databaseService.saveAllExchanges(currencyRates)
    print("Job Success")


@app.route("/currencies/<base>")
def getCurrencyRates(base):
    exchanges = databaseService.getExchangeRatesOfCurrency(base)
    exchanges = list(map(lambda exchange: exchange.toDict, exchanges))
    if len(exchanges) == 0:
        messageText = "{} currency is not supported".format(base)
        return jsonify(message=messageText),404

    return jsonify(exchanges)


@app.route("/currencies")
def getAllCurrencyRates():
    exchanges = databaseService.getExchangeRatesOfCurrencies()
    exchanges = list(map(lambda exchange: exchange.toDict, exchanges))
    return jsonify(exchanges)


@app.route("/currencies/<base>-<currency>")
def getSpesificCurrencies(base, currency):

    exchange = databaseService.getSpesificCurrencies(base,currency)
    if exchange == None:
        messageText = "{}-{} currency conversion is not supported".format(base,currency)
        return jsonify(message=messageText),404


    return jsonify(exchange.toDict)


@app.route("/currency-codes")
def getCurrencyCodes():
    currencies = databaseService.getCurrenciesCodes()
    return jsonify(currencies)


scheduler.add_job(currencyLoaderJob, 'interval', minutes=60, next_run_time=datetime.now())

if __name__ == '__main__':
    scheduler.start()
    app.run(port=8080, debug=True, threaded=True)
