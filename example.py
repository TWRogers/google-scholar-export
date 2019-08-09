from exporter import ScholarExporter
from bs4 import BeautifulSoup

s = ScholarExporter('X0xrjrsAAAAJ')
s.export()

soup = BeautifulSoup(s.content, features="html.parser")
print(soup.prettify())
