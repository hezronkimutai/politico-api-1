# Politico-API

# Questioner

[![Build Status](https://travis-ci.com/nevooronni/Politico-API.svg?branch=develop)](https://travis-ci.com/nevooronni/Politico-API)
[![Coverage Status](https://coveralls.io/repos/github/nevooronni/Politico-API/badge.svg?branch=develop)](https://coveralls.io/github/nevooronni/Politico-API?branch=develop)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  [![PEP8](https://img.shields.io/badge/code%20style-pep8A-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


## Summary 
-------------------------
Question is a politics voting app, it allows the admin to create political parties and office for candidate to run for, the candidates can run for a particular office allowing users to vote for them.

This project is managed by pivotal tracker board. [view the board here](https://www.pivotaltracker.com/n/projects/2244344)

The site is hosted [here]()

The following are API endpoints enabling one to:
-------------------------
* Create account and log in
* Create a political party
* Fetch a specific political party
* Fetch all political parties
* Edit a specific political party
* Delete a specific political party
* Create a political office
* Fetch all political offices
* Create candidate for a specific office election
* Vote for a candidate for a specific office election

Pre-requisites
--------------------------
- Postman
- Git
- Python3

Testing
-------------------------- 
- Clone this repository to your computer:
```
git clone: https://github.com/nevooronni/Politico-API.git
```
- cd into this folder:
```
Politico-API
```
Installation
-------------------------- 
1. Create a virtual environment
```
virtaulenv -p python3 ve```
source venv/bin/activate
```nv
```

2. Activate the virtual environment
```
source venv/bin/activate
```

3. Install git
```
sudo apt-get install git-all
```

4. Switch to 'develop' branch
```
git checkout develop
```
5. Install requirements
```
pip install -r requirements.txt
```
6. Set environment variables
```
mv .env.run .env 

source .env 
```

7. Run app 
```
flask run
```
8. Run tests
```
py.test --cov=app --cov-config .coveragerc
```

Use Postman to test following working Endpoinsts
-------------------------

| Endpoint | Functionality |
----------|---------------
POST/parties | Create a politcal party record
GET/parties/&lt;party-id&gt; | Fetch a specific politcal party record
GET /parties | Fetch all political party records
PATCH /parties/&lt;party-id&gt;/name | Edit a politcal party
DELETE /parties/&lt;party-id&gt; | Delete a politcal party
POST/offices | Create a political office
GET/offices/&lt;office-id&gt; | Fetch a specific politcal office record
GET /offices | Fetch all political offices records

Authors
-------------------------
**Neville Oronni** - _Github_ - [nevooronni](https://github.com/nevooronni)

License
----------
This project is licensed under the MIT license. See [LICENSE](https://github.com/nevooronni/Politico-API/blob/master/LICENSE) for details.

Contribution
---------------
Fork this repository, contribute, and create a pull request to this repo's gh-pages branch.

Acknowledgements
-----------------
1. Andela workshops
2. Andela Bootcamp Team1 members

