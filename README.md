**amigonnadie** is a simple CLI to one of the datasets of the NYC Open Data, specifically *DOHMH New York City Restaurant Inspection Results.*

It's an easy way to check if a place is OK (or not...) in terms of vermins, food safety, etc.

# Installation
Clone it from GitHub, and then run `python setup.py install`.

# Usage
`amigonnadie check "La Colombe"`

Actually it uses full text search, so you can specify a street and a building:
`amigonnadie check "La Colombe Lafayette 400"`

Please use double quotes to enclose the query.
