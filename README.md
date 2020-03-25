<p align="center">
   <img src="https://raw.githubusercontent.com/foundation-int-tech-team/sherlock/master/media/search.png" />
</p>

<h2 align="center">Sherlock</h2>

<p align="center">
    <em>A web crawler to retrieve Wikidot information</em>
</p>

<p align="center">
    <a href="https://www.python.org/">
      <img alt="Python 3.8" src="https://img.shields.io/badge/Made%20with-Python%203.8-1f425f.svg">
    </a>
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
</p>

---

Sherlock is a project allowing to retrieve some Wikidot information (notably pages and their metadata, as well as the members of a wiki). Sherlock is built on the Scrapy framework.

# Installation

_This project has been coded with Python 3.8_

We strongly recommend that you use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) system to use Sherlock in order to neglect the issue of version conflicts that you may be subject to.

```sh
python3.8 -m venv .venv --prompt sherlock
source ./.venv/bin/activate
```

And only then, install the project's dependencies _inside_ the virtual env.

```
pip install -r requirements.txt
```

# Usage

If you are not familiar with Scrapy, I advise you to read the [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html).
The project currently contains two spiders. A spider is a classe which define how a certain site will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items).
The spiders only retrieve data for one wiki at a time. You have to provide them with the name of the target site as an argument (i.e `fondationscp`, `scp-wiki`, `scpko`...) with the following syntax `-a site=name`.

> The branches and their associated metadata are located in the `config.json` file.

## `Members` spider

To start the member crawler.

```sh
scrapy crawl members -o output.json -a site=fondationscp
```

The collected objects will be of the following form

```json
{
  "branch_id": "464696",
  "member_since": "2016-11-03T20:36:04",
  "slug": "jama-sky",
  "user_id": "2880235",
  "username": "jama sky"
}
```

## `Pages` spider

To start the member crawler.

```sh
scrapy crawl pages -o output.json -a site=scp-wiki
```

The collected objects will be of the following form

```json
{
  "title": "SCP-1078",
  "tag": [
    "auditory",
    "electromagnetic",
    "euclid",
    "glass",
    "ocular",
    "scp",
    "sensory",
    "sphere",
    "teleportation",
    "visual"
  ],
  "preview": "Description: SCP-1078 is a small spherical glass eye of a form consistent with late 19th-century German glassblowing techniques. Shavings have confirmed the material to be high-quality blown glass, although no sample has been retrieved from a depth of greater than █.██mm.",
  "id": "13250018",
  "branch_id": "66711",
  "slug": "scp-1078",
  "created_by": "1352778",
  "created_at": "2012-04-30T22:32:53",
  "updated_at": "2018-12-30T17:06:13",
  "rating": {
    "2739004": "+",
    "224440": "-",
    "802114": "-",
    "1750255": "-",
    "1520693": "+",
    "538399": "+",
    "2953586": "+",
    "1449722": "-",
    "2112862": "+",
    "4017872": "-",
    "1340953": "-",
    "1373546": "-",
    [...]
    "1267588": "-",
    "1734870": "+",
    "202258": "+",
    "1204404": "+",
    "575954": "+",
    "2797341": "+"
  }
}
```

## `Titles` spider

To start the title crawler.

```sh
scrapy crawl titles -o output.json -a site=scp-wiki
```

The collected objects will be of the following form

```json
{
  "branch_id": 464696,
  "subtitle": "C'EST UN MONSTRE QUI VEUT TOUS NOUS TUER AAAAAAAAH",
  "slug": "scp-es-4991-j"
}
```

# `config.json`

This file is responsible for directing the crawler to the relevant information of the branch concerned. This file looks like this:

```json
{
  [...]
  "scp-wiki": { /* as it is hosted at scp-wiki.wikidot.com */
    "id": 66711, /* ID that wikidot gave to the branch site */
    "index": [ /* list of paths where the crawler can find the titles of the different SCP */
      "scp-series",
      "scp-series-2",
      [...]
    ],
    "language": "english" /* language is used to generate a preview of the page */
  },
  [...]
}
```

> Note: `language` must be supported by [nltk](https://github.com/nltk/nltk) and its [`punkt`](https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml) dataset

**If you notice that some configuration elements are missing for a branch, don't hesitate to propose a pull request.**

### License

MIT

<p align="center">🎩</p>
