# kind

Query Korea Investor's Network for Disclosure(KIND) for Korean companies' published documents.

## Instructions

The package requires that you have Mozilla Firefox, Internet browser, installed.

1. Install:

```
pip install kind-wycliffwasonga
```

## Usage

1. CLI

```sh
$ kind search --company 241560
```

```sh
$ kind search --company 241560 --start 2021-01-01 --end 2021-03-31
```

2 Library

```python
from datetime import datetime
import kind

start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 3, 31)
results = kind.search("241560", start_date, end_date)
```
