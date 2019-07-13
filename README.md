# rankrecommend

![gandalf's symbol](static/images/logo.png)

A rooted-pagerank based link recommendation system for directed graphs. Specific app which scrapes github and recommends people to follow. 

## Implementation:

* Flask-based web server, and Bootstrap as frontend.
* Uses *Personalised* or *Rooted* Pagerank to find rank prospective \*folowees\*
* The rank of *kth* node is obtained based on the *kth* element of the eigen probability vector for the *random walk with teleport to root* matrix.
* networkx used for graph operations, and numpy for solving for the eigenvalues.

## Setup
Needs python3 and venv submodule. Run setup.sh

## Running:
Run start.sh. Visit 127.0.0.1:5000

## Issues:
* Scraping data from github takes time for slow connections. So program caches user's networks in the data/ folder. If such a file exists, it does not scrape data. *This means that the recommendations will not change even if changes occur in the github network.* Delete the data file for updation.

* The app is **NOT** secure, and does not handle all possible paths well. Misuse is not supported.

