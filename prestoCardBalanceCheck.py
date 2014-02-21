# Presto Card Balance Check
#
# The following program will ask the user for their Presto Card login in
# credentials and print out their current Presto Card balance.
#
# Created by Nick Salerni.
# Copyright (c) 2014 Nick Salerni. All rights reserved.

import mechanize
import cookielib
import string
import getpass

# Method which returns the balance of my presto card.
def prestoCardBalance():
	
	# URL of the website
	url = 'https://www.prestocard.ca/en-US/Pages/TransactionalPages/AccountLogin.aspx'
    
	# Mechanize browser object. This emulates a broswer (object).
	br = mechanize.Browser()
    
	# set cookies
	cookies = cookielib.LWPCookieJar()
	br.set_cookiejar(cookies)
    
	# browser settings (used to emulate a browser)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_debug_http(False)
	br.set_debug_responses(False)
	br.set_debug_redirects(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 5)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
	# Opens the URL
	br.open(url)
    
	# Fills in the selected form in the case (nr = 0) the first form on the webpage
	br.select_form(nr = 0)
    
	# Fills in the username (appropriate textbox names were obtained from the HTML source of the login page).
	br['ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$textboxRegisteredLogin'] = raw_input('Username: ')
    
    # Fills in the password (appropriate textbox names were obtained from the HTML source of the login page).
	br['ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$textboxPassword'] = getpass.getpass()
    
	# Submits the login request using the appropriate 'login' button (appropriate button name were obtained from the HTML source of the login page).
	br.submit(name = 'ctl00$SPWebPartManager1$AccountLoginWebpartControl$ctl00$webpartRegisteredUserLogin$ctl00$buttonSubmit')
    
	# Opens the page after login and saves the HTML source to variable html.
	html = br.open('https://www.prestocard.ca/en-US/Pages/TransactionalPages/RegisteredUserWelcome.aspx').read()
    
	# Finds the index of the balance id (in the HTML source).
	index = html.find('labelDisplayBalance')
    
	# Gets a substring of the HTML source that includes the balance.
	balanceString = html[index : index + 50]
    
	# Gets the balance as a digit with the '$' in front
	all = string.maketrans('','')
	nodigs = all.translate(all, "[^0123456789.$]")
	prestoBalance = "Presto Card Balance: " + balanceString.translate(all, nodigs)
	
	# Logs out of website.
	br.open('https://www.prestocard.ca/en-US/Pages/Logout.aspx')
	
	# Prints the balance (for use in terminal)
	print prestoBalance
    
	# Returns the balance
	return prestoBalance

# Calls the function which will print the current balance of your presto card.
prestoCardBalance()