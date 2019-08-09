import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import date


PAPER_TEMPLATE = """
    <div class="card">
        <div class="card-horizontal">
            <div class="card-body card-body-left">
                <h4><a href="{url}">{title}</a></h4>
                <p style="font-style: italic;">by {authors}</p>
                <p><b>{journal}</b></p>
            </div>
        </div>
        <div class="card-footer">
            <small class="text-muted">Published in <b>{year}</b> | Citations: <b>{n_citations}</b></small>
        </div>
    </div>
    """


class ScholarExporter(object):

    def __init__(self,
                 user: str,
                 page_size: int = 1000,
                 sort_by: str = 'citations') -> None:  # sort_by='pubdate'
        self.user = user
        self.url = 'https://scholar.google.co.uk/citations?' \
                   'user={}' \
                   '&pagesize={}' \
                   '&sortby={}'.format(self.user, page_size, sort_by)
        self.content = None
        self.parsed_papers = []

    def _parse_contents(self) -> None:
        parser = BeautifulSoup(self.content, features="html.parser")
        papers = parser.body.find_all('tr', attrs={'class': 'gsc_a_tr'})
        for paper in papers:
            paper_soup = BeautifulSoup(str(paper), features="html.parser")
            try:
                this_paper = {'title': paper_soup.find('a').text,
                              'year': paper_soup.find_all('span')[-1].text,
                              'n_citations': paper_soup.find('a', {'class': 'gsc_a_ac gs_ibl'}).text,
                              'authors': paper_soup.find_all('div', {'class': 'gs_gray'})[0].text,
                              'journal': paper_soup.find_all('div', {'class': 'gs_gray'})[1].text,
                              'url': '{}#d=gs_md_cita-d&u=%2F{}'.format(self.url,
                                                                        quote(paper_soup.find('a')['data-href'])[1:])}

                if not this_paper['n_citations']:
                    this_paper['n_citations'] = "0"

                if this_paper['journal'].endswith(', ' + this_paper['year']):
                    this_paper['journal'] = this_paper['journal'][:-len(', ' + this_paper['year'])]
                self.parsed_papers.append(this_paper)
            except IndexError:
                print('Warning: error parsing paper.')
            except AttributeError:
                print('Warning: error parsing paper.')

    def export(self,
               html_path: str,
               paper_template: str = None) -> None:
        self._get_and_check_response()
        self._parse_contents()
        if paper_template is None:
            paper_template = PAPER_TEMPLATE

        with open(html_path, 'w') as html_file:
            html_file.write('<p>Publications (<b>{total}</b>) last scraped from '
                            '<a href="{url}">Google Scholar</a> on '
                            '<b>{date}</b>.</p>'.format(total=len(self.parsed_papers),
                                                        url=self.url,
                                                        date=date.today().isoformat()))
            for paper in self.parsed_papers:
                html_file.write(paper_template.format(**paper))

    def _get_and_check_response(self) -> None:
        r = requests.get(self.url)
        if r.status_code == 200:
            self.content = r.content
        else:
            raise ConnectionError('Received {} status code for url {}.'
                                  'Please check that the user {} is correct, '
                                  'and the url format is not out of date.'.format(r.status_code,
                                                                                  self.url,
                                                                                  self.user))





