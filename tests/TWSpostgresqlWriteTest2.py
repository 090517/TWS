import os
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from datetime import date
from postGreSQLCode import pgCode

class TestApp(EWrapper, EClient):

    def __init__(self, sqlLink):
        EClient.__init__(self, self)
        self.file=""
        self.sqlLink= sqlLink

    def error(self, reqId, errorCode, errorString):
        print("Error: ",  reqId, "", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def tickPrice(self, reqId, tickType, price, attribute):
        #self.file.write("ticktype:"+TickTypeEnum.to_str(tickType)+", Price:"+str(price)+"\n")
        #self.file.flush()
        #os.fsync(self.file.fileno())
        #self.sqlLink.insertRow('USD.CAD', "price", price, "quote_type", TickTypeEnum.to_str(tickType))
        print("Ticker Price. Ticker Id:", reqId, "ticktype:", TickTypeEnum.to_str(tickType), "Price:", price, end='\n')

def main():
    # setup postgreSQL
    sqlLink = pgCode.sqlLink()
    sqlLink.connect("DATA_IB_TWS")

    #setup TWS
    twsApp = TestApp(sqlLink)
    twsApp.connect("127.0.0.1", 7496, 1)

    contract2 = Contract()
    contract2.symbol = "USD"
    contract2.secType = "CASH"
    contract2.exchange = "IDEALPRO"
    contract2.currency = "JPY"

    #setupfile for writing
    #twsApp.setupFile("USD.CAD")

    #setup request type
    twsApp.reqMarketDataType(1)
    uniqueId = 2
    twsApp.reqMktData(uniqueId, contract2, "", False, False, [])
    twsApp.reqContractDetails(uniqueId, contract2)

    #final Run
    print("Run")

    twsApp.run() # process's the return

if __name__ == "__main__":
    main()
