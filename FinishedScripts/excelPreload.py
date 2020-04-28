import pandas as pd
import sys
sys.path.append('C:\TWS API 9.79\source\pythonclient')
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
sys.path.append('D:\Dropbox\Projects\Finacial Database\postGreSQLCode')
from pgCode import sqlLink
import time

class twsFirstLoadApp(EWrapper, EClient):

    def __init__(self, sqlLink, priceTableNameIndex, sizeTableNameIndex):
        EClient.__init__(self, self)
        self.file=""
        self.sqlLink= sqlLink
        self.priceTableNameIndex=priceTableNameIndex
        self.sizeTableNameIndex=sizeTableNameIndex

    def error(self, reqId, errorCode, errorString):
        print("Error: ",  reqId, "", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def tickPrice(self, reqId, tickType, price, attribute):
        self.sqlLink.insertRow(self.priceTableNameIndex[reqId], "price", price, "quote_type", TickTypeEnum.to_str(tickType))
        print("Ticker Price. Ticker Id:", reqId, " Table Name:", self.priceTableNameIndex[reqId], "ticktype:", TickTypeEnum.to_str(tickType), "Price:", price, "Attribute", attribute, end='\n')

    def tickSize(self, reqId, tickType, size):
        self.sqlLink.insertRow(self.sizeTableNameIndex[reqId], "Size", size, "quote_type", TickTypeEnum.to_str(tickType))
        print("Ticker Size. Ticker Id:", reqId, " Table Name:", self.sizeTableNameIndex[reqId], "ticktype:", TickTypeEnum.to_str(tickType), "Size:", size, end='\n')
    # def tickGeneric(self, reqId, tickType, value):
    #     print("Ticker Value. Ticker Id:", reqId, " Table Name:", self.tableNameIndex[reqId], "ticktype:", TickTypeEnum.to_str(tickType), "Value:", value, end='\n')
    # def tickString(self, reqId, tickType, value):
    #     print("Ticker string. Ticker Id:", reqId, " Table Name:", self.tableNameIndex[reqId], "ticktype:", TickTypeEnum.to_str(tickType), "Value:", value, end='\n')

# create Sql link
PreSqlLink = sqlLink()
PreSqlLink.connect("DATA_IB_TWS")

# import excel spreadsheetsss into dfPrice/dfSize
dfPrice = pd.read_excel(r'D:\Dropbox\Projects\Python\TWS\tickerList.xlsx')
dfSize = pd.read_excel(r'D:\Dropbox\Projects\Python\TWS\tickerSizeList.xlsx')

# checks if there exists data table with the same name as listed in columnSQL_table.  If not, makes the table as per dictated by the columns in the spreadsheet.
PreSqlLink.createTabledf(dfPrice)
PreSqlLink.createTabledf(dfSize)

# creates an index of contracts to be loaded
contractIndex=[]
priceTableNameIndex=[]
sizeTableNameIndex = []
for row in range(len(dfPrice)):
    contract = Contract()
    contract.symbol = dfPrice.Symbol[row]
    contract.secType = dfPrice.secType[row]
    contract.exchange = dfPrice.exchange[row]
    contract.currency = dfPrice.Currency[row]
    if type(dfPrice.Primary_Exchange[row])==str:
        contract.primaryExchange = dfPrice.Primary_Exchange[row]
    contractIndex.append(contract)
    priceTableNameIndex.append(dfPrice.SQL_table[row])
    sizeTableNameIndex.append(dfSize.SQL_table[row])

#setup TWS
twsApp = twsFirstLoadApp(PreSqlLink, priceTableNameIndex, sizeTableNameIndex)
twsApp.connect("127.0.0.1", 7496, 0)

#setup request type
twsApp.reqMarketDataType(1)

#can only do 50/second
for contract in enumerate(contractIndex):
    #gives the index of the contract in contractIndex as the unique ID
    uniqueId = contract[0]
    twsApp.reqMktData(uniqueId, contract[1], "", False, False, [])
    time.sleep(.03)
    twsApp.reqContractDetails(uniqueId, contract[1])
    time.sleep(.03)

#final Run
twsApp.run() # process's the return