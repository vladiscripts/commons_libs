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


# Scrapy, работа через сессию. Из консоли или Jypiter
from scrapy.http import TextResponse, Response


# request через сессию
def open_reqsession():
    s = requests.Session()
    s.headers = headers
    # s.proxies.update(proxyDict)
    return s


s = open_reqsession()
r = s.get(captcha_url)

# Scrapy: парсинг текстовой страницы
response = TextResponse(r.url, body=r.text, encoding='utf-8')

# Scrapy: парсинг и сохранение картинки в байтовом формате
response = Response(r.url, body=r.content)
with open('/tmp/captcha.jpg', 'wb') as out_image:
    out_image.write(response.body)

# Разгадывание капчи через rucaptcha
RUCAPTCHA_KEY = "74d07cbcef63e8e345548835f0ba430b"

# просто
capchasolve = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY, service_type='rucaptcha',
                                        save_format='const').captcha_handler(
    #     captcha_link=captcha_url,
    captcha_file=captcha_path,
)
captchatext = capchasolve['captchaSolve']


# с проверками на ошибки
def send_captcha_for_solve(captcha_link=None, captcha_file=None):
    # captcha_link = url, или captcha_file
    print('Sending captcha to the solve service')
    # # Возвращается строка-расшифровка капчи
    user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                            service_type='rucaptcha',
                                            # save_format='const'  # или 'temp' (по умолчанию)
                                            ).captcha_handler(captcha_link=captcha_link, captcha_file=captcha_file)
    if user_answer['errorId'] == 1:
        # Error, stop work
        # Тело ошибки, если есть
        print(user_answer['errorBody'])
        if 'ERROR_CAPTCHA_UNSOLVABLE' in user_answer['errorBody']:
            pass
        else:
            exit()

    elif user_answer['errorId'] == 0:
        # решение капчи
        print('captchaSolve: %s, taskId: %s' % (user_answer['captchaSolve'], user_answer['taskId']))
        return user_answer

    elif user_answer['errorId'] > 1:
        pass
