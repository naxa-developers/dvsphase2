Pipeline Test status of master branch : [![CircleCI](https://circleci.com/gh/naxadeve/dvsphase2/tree/master.svg?style=svg)](https://circleci.com/gh/naxadeve/dvsphase2/tree/master)

Pipeline Test status of test server setup branch : [![CircleCI](https://circleci.com/gh/naxadeve/dvsphase2/tree/test-server-setup.svg?style=svg)](https://circleci.com/gh/naxadeve/dvsphase2/tree/test-server-setup)

Pipeline Test status of develop branch : [![CircleCI](https://circleci.com/gh/naxadeve/dvsphase2/tree/develop.svg?style=svg)](https://circleci.com/gh/naxadeve/dvsphase2/tree/develop)

Clone this repository Install docker and docker-compose

Create a symlink with name docker-compose.yml to docker-compose.local.yml

Rename .env_sample to .env and change it settings accordingly for the project

Inside dvs folder rename local_settings_sample.py to local_settings.py and change it settings accordingly for the project

Run external services docker-compose -f external_services.yml up -d

Run the server docker-compose up -d

Note: for logs run docker-compose logs -f --tail 100
