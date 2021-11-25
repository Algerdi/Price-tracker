import requests
import lxml
from bs4 import BeautifulSoup
import smtplib

YOUR_SMTP_ADDRESS = 'smtp.mail.ru'
YOUR_EMAIL = 'your email'
YOUR_PASSWORD = 'your password'
url = "https://www.amazon.com/Python-Crash-Course-2nd-Edition/dp/1593279280/ref=sr_1_1?keywords=python&qid=1637869523&sr=8-1"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(id="newBuyBoxPrice").get_text()
# print(price)
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
# print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
# print(title)

BUY_PRICE = 22

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )