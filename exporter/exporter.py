import requests
from bs4 import BeautifulSoup


class ScholarExporter(object):

    def __init__(self, user: str) -> None:
        self.user = user
        self.url = 'https://scholar.google.co.uk/citations?user={}'.format(self.user)
        self.content = None
        self.parsed_papers = {}

    def _get_and_check_response(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            self.content = r.content
        else:
            raise ConnectionError('Received {} status code for url {}.'
                                  'Please check that the user {} is correct, '
                                  'and the url format is not out of date.'.format(r.status_code, self.url, self.user))

    def _parse_contents(self):
        parser = BeautifulSoup(self.content, features="html.parser")
        papers = parser.body.find_all('tr', attrs={'class': 'gsc_a_tr'})
        for paper in papers:
            paper_soup = BeautifulSoup(str(paper), features="html.parser")
            title = paper_soup.find('a').text
            year = paper_soup.find_all('span')[-1].text
            n_citations = paper_soup.find('a', {'class': 'gsc_a_ac gs_ibl'}).text
            authors = paper_soup.find_all('div', {'class': 'gs_gray'})[0].text
        raise NotImplementedError

    def export(self):
        self._get_and_check_response()
