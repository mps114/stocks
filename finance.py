import requests
from collections import OrderedDict
import json
import csv
import argparse
from time import sleep

def parse(ticker):
	url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
	print("Parsing %s"%(url))
	sleep(1)
	data = OrderedDict()
	link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules=assetProfile,financialData,defaultKeyStatistics,calendarEvents,incomeStatementHistory,cashflowStatementHistory,balanceSheetHistory".format(ticker)
	link_summary = requests.get(link)
	try:
		loaded_link =  json.loads(link_summary.text)
		revenue = loaded_link["quoteSummary"]["result"][0]["financialData"]["totalRevenue"]['raw']
		ebitda = loaded_link["quoteSummary"]["result"][0]["financialData"]["ebitda"]['raw']
		shares_outstanding = loaded_link["quoteSummary"]["result"][0]["defaultKeyStatistics"]["sharesOutstanding"]['raw']
		current_price = loaded_link["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']
		market_cap = shares_outstanding * current_price
		data.update({'finance_info':[{'ticker':ticker,'Market Cap':market_cap,'Revenue':revenue,'EBITDA':ebitda}]})
		return_data = json.dumps(data)
		return return_data
	except ValueError:
		print("Failed to parse json response")
		return {"error":"Failed to parse json response"}
		
if __name__== "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('ticker',help = '')
	args = argparser.parse_args()
	ticker = args.ticker
	print("Fetching data for %s"%(ticker))
	scraped_data = parse(ticker)

	# Now send it to an excel

	print("Writing data to output file")
	#with open('%s-summary.json'%(ticker),'w') as fp:
	 	#json.dump(scraped_data,fp,indent = 4)


	# check where we are in the csv file
	filename = 'finance_data.csv'
	count = 0

	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			count += 1
			if count >= 1:
				break

	full_data_parsed = json.loads(scraped_data)
	data_parsed = full_data_parsed['finance_info']
	excel_data = open('finance_data.csv','a')

	csvwriter = csv.writer(excel_data)

	for dat in data_parsed:
		# if the file is empty make the headers
		if count == 0:
			header = dat.keys()
			csvwriter.writerow(header)
			count += 1
		csvwriter.writerow(dat.values())

	excel_data.close()





