# Halo Infinite Career Rank Extractor

[**▶️ See output**](https://den.dev/blog/halo-infinite-career-ranks/)

This sample tool is designed to read the career rank data from the Halo Infinite game CMS API and store it locally.

## Prerequisites

- [Python 3](https://www.python.org/downloads/)

## Installing requirements

```bash
pip install -r requirements.txt
```

## Running the tool

```bash
python -m career YOUR_SPARTAN_TOKEN
```

As I [mentioned in my blog post](https://den.dev/blog/halo-infinite-career-ranks/), I intentionally didn't bake in the authentication logic here because I wanted a quick and dirty solution to my problem, but if you want to do it _the right way_, you can read [my other blog post](https://den.dev/blog/halo-api-authentication/) on how to authenticate against the Halo Infinite API. For the time being, however, you can grab a token from [Halo Waypoint](https://halowaypoint.com) after you log in (look for the `X-343-Authorization-Spartan` header).

## Feedback

If you have feedback or comments, [open an issue](https://github.com/OpenSpartan/career/issues).
