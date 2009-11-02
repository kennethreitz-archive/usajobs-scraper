from BeautifulSoup import BeautifulSoup
from kenlib import *
import re
import urllib

class Job():
	def __init__(self, title, closingDate, agency, location, salary):
		self.title = title
		self.closingDate = closingDate
		self.agency = agency
		self.location = location
		self.salary = salary
	def __str__(self):
		return str(self.title) + str(self.agency) + str(self.salary) 

# html = urllib.urlopen('http://jobsearch.usajobs.gov/search.aspx').read() 	# INERNET 
html = open('./search.aspx').read() 	# LOCAL

soup = BeautifulSoup(''.join(html))


def scrapePage():
	b = [getResults('title'), getResults('closingDate'), getResults('agency'), getResults('location'), getResults('salary')]
	resultSet = []
	for i in range(len(b[0])):
		resultSet.append(Job(title=b[0][i].contents, closingDate=b[1][i].contents, agency=b[2][i].contents, location=b[3][i].contents, salary=b[4][i].contents))
	
	return resultSet

def getResults(rtype):
	if	rtype == 'title':
		rType = 'a'
		rTitle = 'lnkTitle'
	elif	rtype == 'closingDate':
		rType = 'span'
		rTitle = 'lblDateMiles'
	elif	rtype == 'agency':
		rType = 'span'
		rTitle = 'lblCompany'
	elif	rtype == 'location':
		rType = 'span'
		rTitle = 'lblArea'
	elif	rtype == 'salary':
		rType = 'span'
		rTitle = 'lblSalary'
		
	re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (rTitle)
	rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
	return soup.findAll(rType, { 'id' : rg})
	
if __name__ == '__main__':
	for job in scrapePage():
		print job