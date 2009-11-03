from BeautifulSoup import BeautifulSoup
from kenlib import *
import re
import urllib

class Job():
	def __init__(self, title="", closingDate="", agency="", location="", salary=""):
		self.title = title
		self.closingDate = closingDate
		self.agency = agency
		self.location = location
		self.salary = salary
		# self.details = details
	def __str__(self):
		return str(self.title)  

# html = urllib.urlopen('http://jobsearch.usajobs.gov/search.aspx').read() 	# INERNET 
# html = open('./search.html').read() 	# LOCAL
html = open('./pages/output').read() 	# LOCAL
soup = BeautifulSoup(''.join(html))

def scrapePage():
	b, resultSet = [], []	# Initiate Collectors
	types = ['title', 'closingDate', 'agency', 'location', 'salary', 'details']
	for type in types:
		b.append(getResults(type))

	for i in range(len(b[0])):
		toAppend = []
		for j in range(len(b)):
			toAppend.append(b[j][i].contents)
		resultSet.append(toAppend)

	return resultSet

def getResults(rtype):
	def getTitles():
		rType = 'a'
		rTitle = 'lnkTitle'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(rType, { 'id' : rg})
		
	def getClosingDates():
		rType = 'span'
		rTitle = 'lblDateMiles'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(rType, { 'id' : rg})
		
	def getAgencies():
		rType = 'span'
		rTitle = 'lblCompany'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(rType, { 'id' : rg})
		
	def getLocations():
		rType = 'span'
		rTitle = 'lblArea'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(rType, { 'id' : rg})
	
	def getSalaries():
		rType = 'span'
		rTitle = 'lblSalary'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(rType, { 'id' : rg})
			
	def getDetails():
		rType = 'div'
		rTitle = 'jobDetailBodyDiv'
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		content = soup.findAll(rType, { 'id' : rg})

	if	   rtype == 'title': 		return getTitles()
	elif	rtype == 'closingDate':	return getTitles()
	elif	rtype == 'agency': 		return getTitles()
	elif	rtype == 'location': 	return getTitles()
	elif	rtype == 'salary':		return getTitles()
	elif	rtype == 'details':		return getTitles()
	
if __name__ == '__main__':
	for job in scrapePage():
		print job
	
	