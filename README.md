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
    <a href="https://github.com/hershel/hershel/blob/master/LICENSE">
      <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

---

Sherlock is a project allowing to retrieve some Wikidot information (notably pages and their metadata, as well as the members of a wiki). Sherlock is built on the Scrapy framework.

# Installation

_This project has been coded with Python 3.8_

We strongly recommend that you use a [virtual environment]() system to use Sherlock in order to neglect the issue of version conflicts that you may be subject to.

```sh
python3.8 -m venv ./.venv --prompt sherlock
souce ./.venv/bin/activate
```

And only then, install the project's dependencies _inside_ the virtual env.

```
pip install -r requirements.txt
```

# Usage

If you are not familiar with Scrapy, I advise you to read the [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html).
The project currently contains two spiders. A spider is a classe which define how a certain site will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items).
The spiders only retrieve data for one wiki at a time. You have to provide them with the name of the target site as an argument (i.e `fondationscp`, `scp-wiki`, `scpko`...) with the following syntax `-a site=name`.

## `Members` spider

To start the member crawler.

```sh
scrapy crawl members -o output.json -a site=fondationscp
```

The collected objects will be of the following form

```json
{
  "site": "fondationscp",
  "username": "dr-edit",
  "id": "3303824",
  "pseudo": "Dr Edit",
  "member_since": "2017-08-22T15:22:55"
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
  "lang": "en",
  "title": "SCP-1220",
  "tag": ["language", "media", "recording", "safe", "scp"],
  "id": "13232511",
  "site": "scp-wiki",
  "slug": "scp-1220",
  "author": "1350914",
  "created_at": "2012-04-27T05:59:28",
  "updated_at": "2018-02-24T00:55:58",
  "rating": {
    "3378727": "+",
    "224440": "-",
    "356552": "+",
    "802114": "+",
    "1400601": "+",
    "1704681": "+",
    "2890310": "+",
    [...]
    "1204404": "+",
    "5162909": "+",
    "2037404": "+",
    "1765628": "+",
    "1707000": "+",
    "575954": "+",
    "2797341": "+",
    "1887293": "+"
  }
}
```

### License

MIT
