import re


class MyScrapyCommons:
	re_robotsmap_page = re.compile(r'/(robots.txt|sitemap.\w+)$')
	emailsrch = re.compile(
		r"(?:[a-z0-9!#$%&'*+/=?^_{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
		flags=re.IGNORECASE)  # 100% RFC-2822, from http://scraping.pro/email-validation-regexes/
	clear_url1 = re.compile('^https?://')

	def clear_url(self, url):
		cleared_urls = []
		# clear_url2 = re.compile('^www\.')
		# for url in urls:
		url = url.rstrip(r'/')
		url = self.clear_url1.sub('', url)
		url = 'http://%s' % url
		return url

	# yield url
	# 	cleared_urls.append(url)
	# return cleared_urls

	def parse_emails_on_page(self, response, selenium_driver=None):
		# emails = set()
		# emails = []
		xpath_find_email_tags = "//a[contains(@href, 'mailto:')]"
		xpath_find_email_text = "//body//*[text()[contains(., '@')]]"
		if not selenium_driver:
			return self.parse_emails_on_page_no_selenium_driver(
				response,
				xpath_find_email_tags,
				xpath_find_email_text)
		else:
			return self.parse_emails_on_page_selenium(
				response, selenium_driver,
				xpath_find_email_tags,
				xpath_find_email_text)

	def parse_emails_on_page_no_selenium_driver(self, response):
		emails = set()
		em = response.xpath(xpath_find_email + "/@href")
		for e in em:
			email = e.extract().replace('mailto:', '')
			# self.add_email(email, emails)
			emails.add(email)
		# emails.add(e.extract().replace('mailto:', ''))
		em = response.xpath(xpath_find_email_text + "/text()")
		for e in em:
			email = e.extract().strip()
			# self.add_email(email, emails)
			emails.add(email)
		return emails

	def parse_emails_on_page_selenium(self, response, selenium_driver, xpath_find_email):
		emails = set()
		em = selenium_driver.find_elements_by_xpath(xpath_find_email)
		for e in em:
			# u = e.get_attribute('href')
			email = e.get_attribute('href').replace('mailto:', '')
			self.add_email(email, emails)
		# emails.add(e.get_attribute('href').replace('mailto:', ''))
		em = self.driver.find_elements_by_xpath(xpath_find_email_text)
		for e in em:
			self.add_email(e.text, emails)
		return emails

	def add_email(self, email, emails):
		"""Вместо set() используется список, чтобы сохранить порядок находок сверху вниз. Set() не сохраят порядок."""
		if email not in emails:
			emails.append(email)
		return emails
