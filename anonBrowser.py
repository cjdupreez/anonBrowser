#!/usr/bin/python
import sys, getopt, re, mechanize, os, traceback
from random import choice
#handle user input to specify site
def main(argv):
	site = ' '
	stop = 0
	try: 
		opts, args = getopt.getopt(argv, "hs:")
	except:
		print 'Usage: ./anonBrowser.py -s URL'
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: ./anonBrowser.py -s URL'
			sys.exit()
		elif opt in ("-s", "--site"):
			site = str(arg)
	print 'Site to retreive:',site
	#try different proxies until we find one that works
	for i in range(0,15):
		while True:
			try:
				def findProx():
					br = mechanize.Browser()
					path = br.retrieve('http://proxy-ip-list.com/download/free-proxy-list.txt', './proxies.txt')[0]
					array = []
					data = open( "./proxies.txt", "rU" )
					for line in data:
						match = re.search(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{1,5}\b', line)
						if match:
							array.append(match.group())
						else:
							continue
					data.close
					os.remove("./proxies.txt")
					global randProx
					randProx = choice(array)
				findProx()
				#specify how we want our browser to behave and present information
				def viewPage(url):
					userAgents = ['Mozilla/4.0 ','Firefox/6.01','ExactSearch','Nokia7110/1.0']
					index = choice(userAgents)
					br = mechanize.Browser()
					br.set_handle_robots(False)
					br.set_proxies({"http":randProx})
					page = br.open(url, timeout=5)
					source_code = page.read()
					headers = page.info()
					print headers
					print source_code
				viewPage(site)
				print "Proxy used: " + randProx
				return stop
			except:
				continue
			break
if __name__ == "__main__":
	main(sys.argv[1:])
