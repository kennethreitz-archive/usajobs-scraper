from BeautifulSoup import BeautifulSoup
from kenlib import *
import re
import urllib
import MySQLdb

class Job():
	def __init__(self, title, closingDate, agency, location, salary, details, vacancy, apply, plan, appointmentTerm, jobStatus, openingDate, salaryRange):
		try:
			self.title = title[0].encode('utf-8').replace('\n','')
			self.closingDate = closingDate[0].encode('utf-8').replace('\n','')
			self.agency = agency[0].encode('utf-8').replace('\n','')
			self.location = location[0].encode('utf-8').replace('\n','')
			self.salary = salary[0].encode('utf-8').replace('\n','')
			self.details = details[0].encode('utf-8').replace('\n','')
			self.vacancy = vacancy[0].encode('utf-8').replace('\n','')
			self.apply = apply[0].encode('utf-8').replace('\n','')
			self.plan = plan[0].encode('utf-8').replace('\n','')
			self.appointmentTerm = appointmentTerm[0].encode('utf-8').replace('\n','')
			self.jobStatus = jobStatus[0].encode('utf-8').replace('\n','')
			self.openingDate = openingDate[0].encode('utf-8').replace('\n','')
			self.salaryRange = salaryRange[0].encode('utf-8').replace('\n','')
		except Exception, e:
			self.title = ""
			self.closingDate = ""
			self.agency = ""
			self.location = ""
			self.salary = ""
			self.details = ""
			self.vacancy = ""
			self.apply = ""
			self.plan = ""
			self.appointmentTerm = ""
			self.jobStatus = ""
			self.openingDate = ""
			self.salaryRange = ""
		
		
	def __str__(self):
		return "%s -> %s" % (self.title, self.vacancy) 
		
	def store(self):
		conn = MySQLdb.connect(host="kennethreitz.com", user="admin", passwd="drummer42", db="scraper")
		cursor = conn.cursor ()
		# title, closingDate, agency, location, salary, details, vacancy, apply, plan, appointmentTerm, jobStatus, openingDate, salaryRange
		query = "INSERT INTO jobs (title, closing_date, agency, location, salary, details, vacancy, apply, plan, appointment_term, job_status, opening_date, salary_range) " + \
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )" % \
		(conn.literal(self.title), conn.literal(self.closingDate), 
		 conn.literal(self.agency), conn.literal(self.location), 
		 conn.literal(self.salary), conn.literal(self.details), 
		 conn.literal(self.vacancy), conn.literal(self.apply), 
		 conn.literal(self.plan), conn.literal(self.appointmentTerm),
		 conn.literal(self.jobStatus), conn.literal(self.openingDate), 
		 conn.literal(self.salaryRange))
		cursor.execute (query)
		cursor.close ()
		conn.close ()
		
	def inspect(self):
		print self.title
		print self.closingDate
		print self.agency
		print self.location
		print self.salary
		print self.details
		print self.vacancy
		print self.apply
		print self.plan
		print self.appointmentTerm
		print self.jobStatus
		print self.openingDate
		print self.salaryRange
		print '\n' * 4
		
html = open('./output').read() 	# LOCAL
soup = BeautifulSoup(''.join(html))

def scrapePage():
	b = [getResults('title'), getResults('closingDate'), getResults('agency'), getResults('location'), getResults('salary'), getResults('details'), getResults('vacancy'), getResults('apply'), getResults('plan'), getResults('appointmentTerm'), getResults('jobStatus'), getResults('openingDate'), getResults('salaryRange')]
	resultSet = []
	for i in range(len(b[0])):
		newJob 	= 	Job(	b[0][i].contents, b[1][i].contents, b[2][i].contents, 
								b[3][i].contents, b[4][i].contents, b[5][i].contents, 
								b[6][i].contents, b[7][i].contents, b[8][i].contents, 
								b[9][i].contents, b[10][i].contents, b[11][i].contents, 
								b[12][i].contents
							 )
		resultSet.append(newJob)
		
	return resultSet

def getResults(rtype):
	
	def getMeta(type, title):
		print "fetching ", title
		re0='MasterPage1_middleContent__ctlResultsFlat_rptResults__ctl(\d)(\d)?_%s$' % (title)
		rg = re.compile(re0,re.IGNORECASE|re.DOTALL)
		return soup.findAll(type, { 'id' : rg})

	if	  rtype == 'title': 	  			return getMeta('a', 'lnkTitle')
	elif rtype == 'closingDate':		return getMeta('span', 'lblDateMiles')
	elif rtype == 'agency': 	  		return getMeta('span', 'lblCompany')
	elif rtype == 'location':   		return getMeta('span', 'lblArea')
	elif rtype == 'salary':	  			return getMeta('span', 'lblSalary')
	elif rtype == 'details':	  		return getMeta('div', 'jobDetailBodyDiv')
	elif rtype == 'vacancy':	  		return getMeta('span', 'lblVacancyAnnNumber')
	elif rtype == 'apply':		  		return getMeta('span', 'lblWhoMayApply')
	elif rtype == 'plan':		  		return getMeta('span', 'lblPayPlan')
	elif rtype == 'appointmentTerm':	return getMeta('span', 'lblAppointmentTerm')
	elif rtype == 'jobStatus':			return getMeta('span', 'lblJobStatus')
	elif rtype == 'openingDate':		return getMeta('span', 'lblOpeningDate')
	elif rtype == 'salaryRange':		return getMeta('span', 'lblSalaryRange')
	
	
if __name__ == '__main__':
	for job in scrapePage():
		print "Storing %s..." % (job.title)
		job.store()
		# print len(job)
	# for t in ['title', 'closingDate', 'agency', 'location', 'salary', 'details', 'vacancy', 'apply', 'plan', 'appointmentTerm', 'jobStatus', 'openingDate', 'salaryRange']:
		# print getResults(t)[0].contents[0].encode('utf-8').replace('\n','')
		# print '>'