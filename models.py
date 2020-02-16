class ExchangeModel:
    __base = ""
    __currency = ""
    __rate = 0.0

    def __init__(self, base, currency, rate):
        self.__base = base
        self.__currency = currency
        self.__rate = round(rate, 4)

    @property
    def base(self):
        return self.__base

    @property
    def currency(self):
        return self.__currency

    @property
    def rate(self):
        return self.__rate

    @property
    def toString(self):
        return "{} {} {}".format(self.base, self.currency, self.rate)

    @property
    def toDict(self):
        return dict(base=self.__base, currency=self.__currency, rate=self.__rate)