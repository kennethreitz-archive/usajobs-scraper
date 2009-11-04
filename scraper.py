from BeautifulSoup import BeautifulSoup
from kenlib import *
import re
import urllib
import MySQLdb

fields = ['id', 'title', 'closingDate', 'agency', 'locationCity', 'locationState', 'locationCountry', 'salary', 'details', 'vacancy', 'apply', 'plan', 'appointmentTerm', 'jobStatus', 'openingDate']
sqlfields = map(snake_case, fields[:])

# Open up output file
html = open('./output').read() 	# LOCAL
soup = BeautifulSoup(''.join(html))

class Job():
	def __init__(self, id, title, closingDate, agency, locationCity, locationState, locationCountry, salary, details, vacancy, apply, plan, appointmentTerm, jobStatus, openingDate):
		try:
			self.id = id
			self.title = title
			self.closingDate = closingDate
			self.agency = agency
			# self.location = ', '.join(location)
			self.locationCity = locationCity
			self.locationState = locationState
			self.locationCountry = locationCountry
			self.salary = salary
			self.details = details
			self.vacancy = vacancy
			self.apply = apply
			self.plan = plan
			self.appointmentTerm = appointmentTerm
			self.jobStatus = jobStatus
			self.openingDate = openingDate
		
		except Exception, e:
			del self
		
	def __str__(self):
		return "%s -> %s" % (self.title, self.vacancy) 
		
	def store(self):
		conn = MySQLdb.connect(host="localhost", user="admin", passwd="drummer42", db="scraper")
		cursor = conn.cursor ()
		query = "INSERT INTO jobs (%s) " % (', '.join(sqlfields))+ \
		"VALUES (%s )" % \
			', '.join(conn.literal(f) for f in 
				[self.id, self.title, self.closingDate, 
					self.agency, self.locationCity, self.locationState, self.locationCountry,
					self.salary, self.details,
					self.vacancy, self.apply,
					self.plan, self.appointmentTerm,
					self.jobStatus, self.openingDate ])
		cursor.execute (query)
		cursor.close ()
		conn.close ()
		del self
		
	def inspect(self):
		print self.title, self.id

def scrapePage():
	b = map(getResults, fields)
	resultSet = []
	for i in qrange(len(fields)):
		newJob = Job(*[b[j][i] for j in qrange(len(fields))])
		del b
		resultSet.append(newJob)
		del newJob
		
	return resultSet

def getResults(rtype):
	
	def getMeta(type, title):
		print "fetching " + title + "s"
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (title)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(type, { 'id' : rg})
	
	def scrub(dirty, meta = 'contents'):
		if meta == 'contents':
			for i in qrange(len(dirty)):
				dirty[i] = dirty[i].contents[0].replace('\n','')
			clean = utf8ify(dirty)
			
		elif meta == 'href':
			for i in qrange(len(dirty)):
				dirty[i] = dirty[i]['href']
			clean = utf8ify(dirty)
			
		return clean
		
	# begin proccessing

	if rtype == 'id':
		results = scrub(getMeta('a', 'lnkTitle'), 'href')
		for i in qrange(len(results)):
			results[i] = results[i][45:52]
		
	elif	rtype == 'title':
		results = scrub(getMeta('a', 'lnkTitle'))
		
	elif rtype == 'closingDate':		
		results = scrub(getMeta('span', 'lblDateMiles'))
		
	elif rtype == 'agency': 	  		
		results = scrub(getMeta('span', 'lblCompany'))
	
	elif rtype == 'location':
		results = scrub(getMeta('span', 'lblArea'))
		results = [item.split('-') for item in results]
		
	elif rtype == 'locationCity':
		results = scrub(getMeta('span', 'lblArea'))
		results = [item.split('-') for item in results]
		for i in range(len(results)):
			try:
				results[i] = results[i][2]
			except Exception, e:
				results[i] = results[i][1]
			
			
	elif rtype == 'locationState':		
		results = scrub(getMeta('span', 'lblArea'))
		results = [item.split('-') for item in results]
		for i in range(len(results)):
			results[i] = results[i][1]
			
	elif rtype == 'locationCountry':		
		results = scrub(getMeta('span', 'lblArea'))
		results = [item.split('-') for item in results]
		for i in range(len(results)):
			results[i] = results[i][0]

	elif rtype == 'salaryRange':		
		results = scrub(getMeta('span', 'lblArea'))
		
	elif rtype == 'salary':
		results = scrub(getMeta('span', 'lblSalary'))
		results = [item.replace(',', '').replace('$', '').replace('+', '').replace('.00', '') for item in results]

	elif rtype == 'details':	  		
		results = scrub(getMeta('div', 'jobDetailBodyDiv'))
		
	elif rtype == 'vacancy':	  		
		results = scrub(getMeta('span', 'lblVacancyAnnNumber'))
		
	elif rtype == 'apply':		  		
		results = scrub(getMeta('span', 'lblWhoMayApply'))
		
	elif rtype == 'plan':		  		
		results = scrub(getMeta('span', 'lblPayPlan'))
		
	elif rtype == 'appointmentTerm':	
		results = scrub(getMeta('span', 'lblAppointmentTerm'))
		
	elif rtype == 'jobStatus':			
		results = scrub(getMeta('span', 'lblJobStatus'))
		
	elif rtype == 'openingDate':		
		results = scrub(getMeta('span', 'lblOpeningDate'))
		
	elif rtype == 'salaryRange':		
		results = scrub(getMeta('span', 'lblSalaryRange'))
	
	else:
		raise NameError
		
	return results

def clearDB():
	print "clearing DB"
	conn = MySQLdb.connect(host="localhost", user="admin", passwd="drummer42", db="scraper")
	cursor = conn.cursor ()
	cursor.execute ("TRUNCATE TABLE jobs")
	cursor.close ()
	conn.close ()
	


if __name__ == '__main__':
	clearDB()
	for job in scrapePage():
		print "Storing: %s" % job.title
		job.store()
	
	# print getResults('salary')