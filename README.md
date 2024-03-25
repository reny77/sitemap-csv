# sitemap-csv

This script allows you to download all the URLs from a sitemap in CSV format. It also works for nested sitemaps. 

In the first column, it puts the URL of the sitemap, and in the second, the URL of the page.

## Prepare your environment

```bash
git clone git@github.com:reny77/sitemap-csv.git
cd sitemap-csv
python3 -m venv venv
source venv/bin/activate
python3 sitemap-dumper.py https://${URL}/sitemap.xml
```

## Usage

```bash
python3 sitemap-dumper.py https://${URL}/sitemap.xml
```
