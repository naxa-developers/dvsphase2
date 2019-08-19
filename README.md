

Test status of master branch :
[![CircleCI](https://circleci.com/gh/dfid-dvs/server/tree/master.svg?style=svg)](https://circleci.com/gh/dfid-dvs/server/tree/master)


Clone this repository
Install docker and docker-compose

Create a symlink with name docker-compose.yml to docker-compose.local.yml

Run external services docker-compose -f external_services.yml up -d

Run the server docker-compose up -d


Note: for logs run docker-compose logs -f --tail 100
