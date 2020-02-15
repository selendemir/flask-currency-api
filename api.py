from flask import Flask, jsonify
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from rates import CurrencyServices
from datetime import datetime


mongo = MongoClient("localhost", 27017)
db = mongo.currency_db
currencyDoc = db.currencies
app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)

currencyService = CurrencyServices()


def currencyLoaderJob():
    currencyRates = currencyService.getAllCurrencyRates()
    jsonConverter = lambda exchange: exchange.toDict
    currencyRatesDictList = map(jsonConverter, currencyRates)
    currencyDoc.delete_many({})
    currencyDoc.insert_many(currencyRatesDictList)
    print("Job Successe")






@app.route("/currencies/<searchBase>", methods=["GET","POST"])
def getCurrencyRates(searchBase):
    dbResult = currencyDoc.find({"base": searchBase})

    exchanges = []
    for row in dbResult:
        exchange = dict(currency=row['currency'], rate=row['rate'])
        exchanges.append(exchange)


    return jsonify(exchanges)

scheduler.add_job(currencyLoaderJob, 'interval', minutes = 60, next_run_time=datetime.now())

if __name__ == '__main__':
    scheduler.start()
    app.run(port=8080, debug=True, threaded= True)

