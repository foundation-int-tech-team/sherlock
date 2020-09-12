<p align="center">
   <img src="https://raw.githubusercontent.com/foundation-int-tech-team/sherlock/master/media/search.png" />
</p>

<h2 align="center">Sherlock</h2>

<p align="center">
    <em>A web crawler to retrieve Wikidot informations</em>
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
The project currently contains 4 spiders (the functionality allowing to collect the votes is not yet present). A spider is a classe which define how a certain site will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items).
The spiders only retrieve data for one wiki at a time. You have to provide them with the name of the target site as an argument (i.e `fondationscp`, `scp-wiki`, `scpko`...) with the following syntax `-a site=<name>`.

> The branches and their associated metadata are located in the `data.json` file.

If you want to store the recovered data in a Postgresql database, please decrement line 69 in `settings.py`.

## `members` spider

To start the member crawler.

```sh
scrapy crawl members -o output.json -a site=fondationscp
```

The collected objects will be of the following form

```json
{
  "branch_id": 464696,
  "user_id": "1511818",
  "slug": "dr-hideous",
  "username": "Dr Hideous",
  "member_since": "2012-12-16T20:06:48"
}
```

## `pages` spider

To start the page crawler.

```sh
scrapy crawl pages -o output.json -a site=scp-wiki
```

The collected objects will be of the following form

```json
{
  "page_id": "2417704",
  "branch_id": 66711,
  "title": "SCP-547-D",
  "preview": "Description: SCP-547 appears to be a young, muscular Caucasian male in his late teenage years. Subject is 2m (6'3\") and weighs 85kg (190 lbs.). Since original encounter with SCP-547 in Austria near the small village of in 17██, subject appears to have not aged at all. MRI and X-Ray reveal SCP-547's body to be completely human with the exception of where subject's heart would be.",
  "slug": "decomm:scp-547-d",
  "tags": ["decommissioned", "euclid", "humanoid", "neutralized", "scp"],
  "created_by": "172464",
  "created_at": "2008-11-08T17:44:50",
  "updated_at": "2014-09-04T06:56:00"
}
```

## `titles` spider

To start the title crawler.

```sh
scrapy crawl titles -o output.json -a site=scp-wiki
```

The collected objects will be of the following form

```json
{
  "subtitle": "The 12 Rusty Keys and the Door",
  "slug": "scp-004",
  "branch_id": 66711
}
```

# `data.json`

This file is responsible for directing the crawler to the relevant information of the branch concerned. This file looks like this:

```python
{
  [...]
  "scp-wiki": { # as it is hosted at scp-wiki.wikidot.com
    "id": 66711, # ID that wikidot gave to the branch site
    "index": [ # list of paths where the crawler can find the titles of the different SCP
      "scp-series",
      "scp-series-2",
      [...]
    ],
    "language": "english" # language is used to generate a preview of the page
  },
  [...]
}
```

When you give `-a site=<name>`, name is searched as the key from this file and the corresponding value is loaded as the current configuration.

> Note: `language` must be supported by [nltk](https://github.com/nltk/nltk) and by the [`punkt`](https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml) dataset

**If you notice that some configuration elements are missing for a branch, don't hesitate to propose a pull request.**

### License

MIT

<p align="center">🎩</p>
