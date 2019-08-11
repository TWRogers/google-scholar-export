# Copyright 2019 Thomas W. Rogers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import date


PAPER_TEMPLATE = """
<div class="card">
    <div class="card-publication">
        <div class="card-body card-body-left">
            <h4><a href="{url}">{title}</a></h4>
            <p style="font-style: italic;">by {authors}</p>
            <p><b>{journal}</b></p>
        </div>
    </div>
    <div class="card-footer">
        <small class="text-muted">Published in <b>{year}</b> | 
        <a href="{citations_url}">Citations: <b>{n_citations}</b></a></small>
    </div>
</div>
"""

INTRO_TEXT = """
<p>Publications (<b>{total}</b>) last scraped for <a href="{url}">{scholar}</a> on <b>{date}</b> 
using <a href="https://github.com/TWRogers/google-scholar-export">google-scholar-export</a>.</p>
"""


class ScholarExporter(object):

    def __init__(self, url: str) -> None:  # sort_by='pubdate'
        self.url = url
        self.content = None
        self.parsed_papers = []
        self.scholar = 'N/A'

    @classmethod
    def from_user(cls,
                  user: str,
                  page_size: int = 1000,
                  sort_by: str = 'citations'):  # sort_by='pubdate'

        url = 'https://scholar.google.co.uk/citations?' \
              'user={}' \
              '&pagesize={}' \
              '&sortby={}'.format(user, page_size, sort_by)

        return cls(url)

    def export(self,
               html_path: str,
               paper_template: str = None) -> None:

        self._get_and_check_response()
        self._parse_contents()
        if paper_template is None:
            paper_template = PAPER_TEMPLATE

        with open(html_path, 'w') as html_file:
            html_file.write(INTRO_TEXT.format(scholar=self.scholar,
                                              total=len(self.parsed_papers),
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
                                  'Please check that the url is valid'
                                  'and that you have internet connection.'.format(r.status_code,
                                                                                  self.url))

    def _parse_contents(self) -> None:
        parser = BeautifulSoup(self.content, features="html.parser")
        self.scholar = parser.find('div', {'id': 'gsc_prf_in'}).text
        papers = parser.body.find_all('tr', attrs={'class': 'gsc_a_tr'})
        for paper in papers:
            paper_soup = BeautifulSoup(str(paper), features="html.parser")
            try:
                citations_a = paper_soup.find('a', {'class': 'gsc_a_ac gs_ibl'})
                if citations_a is None:
                    citations_a = paper_soup.find('a', {'class': 'gsc_a_ac gs_ibl gsc_a_acm'})

                this_paper = {'title': paper_soup.find('a').text,
                              'year': paper_soup.find_all('span')[-1].text,
                              'n_citations': citations_a.text,
                              'citations_url': citations_a['href'],
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
