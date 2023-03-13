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
    <li class="relative flex items-center justify-between rounded-xl p-4 hover:bg-slate-100">
        <div class="flex gap-4">
          <div class="w-full text-md leading-6">
            <a href="{url}" target="_blank"
               class="font-semibold text-slate-900">
                <span class="inset-0 rounded-xl" aria-hidden="true">
                {title}
                </span>
            </a>
            <div class="flex">
                <div class="basis-8/12 text-sm ">
                    <p class="font-medium text-slate-600">
                        by <span class="italic"> {authors}</span>
                    </p>
                    <p class="font-semibold text-slate-500">
                        {journal}
                    </p>
                </div>
                <div class="basis-4/12">
                    <p class="font-medium text-slate-800">
                        Published in <span class="font-bold text-slate-1000">{year}</span>
                    </p>
                    <a class="hover:text-slate-500"  href="{citations_url}" target="_blank">
                        Citations: <span class="font-bold">{n_citations}</span>
                    </a>
                </div>
            </div>
           
          </div>
        </div>
      </li>
"""

INTRO_TEXT = """
<script src="https://cdn.tailwindcss.com"></script>

<div class="px-4">
    <p class="mx-auto max-w-lg2 bg-white p-2 shadow text-md">Publications (<span class="font-bold ">{total}</span>) last scraped for 
        <a href="{url}" target="_blank">
            <span class="hover:text-slate-500">{scholar}</span> </a> on <b>{date}</b> 
        using <a href="https://github.com/murez/google-scholar-export" target="_blank"><span class="italic hover:text-slate-500">google-scholar-export</span></a>.</p>
    <ul role="list" class="mx-auto max-w-lg2 bg-white p-2 shadow">
"""
END_TEXT = """
    </ul>
</div>
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

        url = 'https://scholar.google.com/citations?' \
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
            html_file.write(END_TEXT)

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
                                                                        quote(paper_soup.find('a')['href'])[1:])}

                if not this_paper['n_citations']:
                    this_paper['n_citations'] = "0"

                if this_paper['journal'].endswith(', ' + this_paper['year']):
                    this_paper['journal'] = this_paper['journal'][:-len(', ' + this_paper['year'])]
                self.parsed_papers.append(this_paper)
            except IndexError:
                print('Warning: error parsing paper.')
            except AttributeError:
                print('Warning: error parsing paper.')
