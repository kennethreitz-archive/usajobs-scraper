#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands


def main():
	# commands.getoutput("cd ../pages/")
	for i in range(1, ((5000 / 50) + 1)):
		commands.getoutput("wget http://jobsearch.usajobs.gov/search.aspx?pg=%s" % (i))


if __name__ == '__main__':
	# commands.getoutput()
	main()

