import os

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from datetime import date

class TestApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.file=""

    def setupFile(self, ticker):
        today = date.today()
        name = ticker+"-"+today.strftime("%b-%d-%Y")+".txt"
        self.file = open(name,"a")

    def error(self, reqId, errorCode, errorString):
        print("Error: ",  reqId, "", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def tickPrice(self, reqId, tickType, price, attribute):
        self.file.write("ticktype:"+TickTypeEnum.to_str(tickType)+", Price:"+str(price)+"\n")
        self.file.flush()
        os.fsync(self.file.fileno())
        print("Ticker Price. Ticker Id:", reqId, "ticktype:", TickTypeEnum.to_str(tickType), "Price:", price, end='\n')

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7496, 0)

    # contract = Contract()
    # contract.symbol = "AAPL"
    # contract.secType = "STK"
    # contract.exchange = "SMART"
    # contract.currency = "USD"
    # contract.primaryExchange = "NASDAQ"

    #create contract
    contract = Contract()
    contract.symbol = "USD"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "CAD"

    #setupfile for writing
    app.setupFile("USD.CAD")

    #setup request type
    app.reqMarketDataType(1)
    uniqueId = 1
    app.reqMktData(uniqueId, contract, "", False, False, [])
    app.reqContractDetails(uniqueId, contract)

    #final Run
    app.run() # process's the return

if __name__ == "__main__":
    main()
