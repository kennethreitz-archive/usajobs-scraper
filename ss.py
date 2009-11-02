from BeautifulSoup import BeautifulSoup
import re
import urllib
from kenlib import *

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		



# html = urllib.urlopen('http://jobsearch.usajobs.gov/search.aspx').read() 	# INERNET 
html = open('./search.aspx').read() 	# LOCAL

soup = BeautifulSoup(''.join(html))		# Soupify

def getResults(type, ):
	if	type == "title":
		rType = 
		tTitle = lnkTitle
			# Integer Number 1
re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s' % (rTitle)
rg = re.compile(re0,re.IGNORECASE|re.DOTALL)

# results = soup.findAll('span', { 'id' : r'MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl1_lblDateMiles'})
results = soup.findAll('a', { 'id' : rg})

for result in results:
    print result.contents

# print soup.find(resultsFlag)
# print soup.prettify()


def getNames():
	"""docstring for findNames"""
	pass