## Updates

![example](https://cdn.hashnode.com/res/hashnode/image/upload/v1666314008938/eGSgVKEnB.png?auto=compress,format&format=webp)

1. a well rendered interactive html templete with TailwindCSS
2. a github action script to get `html` file and push to `result` branch every day.
3. a [blog](https://murez.cloud/how-to-show-your-google-scholar-on-hashnode) to show how to use in hashnode.

--------------------------
Old README

<p align="center">
    <img src="https://twrogers.github.io/assets/images/scholar-exporter.png" width=400" title="Google Scholar Profile exporter for static html pbulication lists.">
</p>

# google-scholar-export
**google-scholar-export** is a Python library for scraping Google scholar profiles to generate a HTML publication lists.

Currently, the profile can be scraped from either the Scholar user id, or the Scholar profile URL, resulting in a list
of the following:

1. Publication title
2. Publication authors
3. Journal information (name, issue no., vol.)
4. Date
5. Url to the Scholar publication
6. The number of citations according to Scholar

The resulting html is formatted like:
```html
<p>Publications (<b>20</b>) last scraped for <a href="https://scholar.google.co.uk/citations?user=JicYPdAAAAAJ&hl=en">Geoffrey Hinton</a> on <b>2019-08-11</b> 
using <a href="https://github.com/TWRogers/google-scholar-export">google-scholar-export</a>.</p>
<div class="card">
    <div class="card-publication">
        <div class="card-body card-body-left">
            <h4><a href="https://scholar.google.co.uk/citations?user=JicYPdAAAAAJ&hl=en#d=gs_md_cita-d&u=%2Fcitations%3Fview_op%3Dview_citation%26hl%3Den%26oe%3DASCII%26user%3DJicYPdAAAAAJ%26citation_for_view%3DJicYPdAAAAAJ%3AGFxP56DSvIMC">Learning internal representations by error-propagation</a></h4>
            <p style="font-style: italic;">by DE Rumelhart, GE Hinton, RJ Williams</p>
            <p><b>Parallel Distributed Processing: Explorations in the Microstructure of …</b></p>
        </div>
    </div>
    <div class="card-footer">
        <small class="text-muted">Published in <b>1986</b> | 
        <a href="https://scholar.google.co.uk/scholar?oi=bibs&hl=en&oe=ASCII&cites=1374659557399191249,4574189560556662535,10453698013284960354,12541410141153091507,7476519782727404507,1722523513356915749,6822548856209813074,4464353390709992638,15344233312479649775">Citations: <b>62260</b></a></small>
    </div>
</div>
...
```
And is primarily aimed at people using Bootstrap.

It is possible to modify the html for each publication by modifying `PAPER_TEMPLATE` in `./exporter/exporter.py`

## Rationale
Generating lists of publications for static websites is a pain. Google Scholar, popular amongst academics, is great at
tracking publications and citations. However, it does not have an API.

There are some other libraries:
* [dschreij/scholar_parser](https://github.com/dschreij/scholar_parser)
* [bborrel/google-scholar-profile-parser](https://github.com/bborrel/google-scholar-profile-parser)

However, both of these are php based, and not useful for static sites.

The purpose of this repository is to allow generation of static html code directly from your Google Scholar profile.
This code can be run manually, or at website build time to update the publications list.

Here is an example that utilises this library:
[twrogers.github.io/projects.html](https://twrogers.github.io/projects.html#publications)

The aim is eventually to develop a _JS_ version of this library.

## Requirements
Install the relevant requirements as usual from the root of this repository:

```bash
pip install -r ./requirements.txt
```
This code was written and tested in **Python 3.5.2**.

## Usage
To export to html from a Google Scholar user id, do the following:

```python
from exporter import ScholarExporter
# Example from user id:
s = ScholarExporter.from_user('JicYPdAAAAAJ')  # Geoffrey Hinton user
s.export('index.html')
```

To export to html from a Google Scholar profile url, do the following:

```python
from exporter import ScholarExporter
# Example from url:
s = ScholarExporter('https://scholar.google.co.uk/citations?user=JicYPdAAAAAJ&hl=en')  # Geoffrey Hinton url
s.export('index.html')
```
## TODO
* Add example CSS style sheet
* Fix `IndexError` and `AttributeErrors` that sometimes occur.
* Add other export options


## License

Copyright 2019 Thomas W. Rogers. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================
