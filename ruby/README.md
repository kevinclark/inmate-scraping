# Inmate Scraping (Ruby)

## Installation
Assuming functional Ruby v2.7+ environment:

```sh
bundle install
```

## New Hampshire Usage

```sh
# First step
bundle exec rake nh:download

# Generate TSV (see: `nh/data/inmates.tsv`)
bundle exec rake nh:tsv
```
