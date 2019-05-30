## Language & tooling

* Language: Python | 3.6.7
* Unit testing: pytest | 3.3.2 | https://docs.pytest.org/en/latest/
* Code formatting: Black | 19.3b0 | https://github.com/python/black

## Usage

```
python3 main.py
```

## Initial state of Stocks in the Index

See the list in main.py on line 9.

## Areas for improvement

I have made a number of design decisions with the goal of keeping the solution simple that would need
to be revisited in the real world.

Some example usages:

* Utilise the command pattern to keep an audit log of operations.
* Use a statistics library to calculate the geometric mean.
* Check balance of shares owned before selling.


## Why Python 3?

Python 3 felt like a safe bet given this role is to build the next generation of credit
systems and Python 2 is getting close to end of life.

## Author's Python knowledge

Apologies if the code is not Pythonic/idomatic in areas.

I have limited hands-on development experience with Python from 10 years ago.

My recent hands-on development experience is mostly in PHP and JavaScript, though I have been managing
teams who use Python everyday and writing throwaway scripts myself.
