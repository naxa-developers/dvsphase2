![Imgur](https://i.imgur.com/ZtIe5vn.png)
# Dvs

[![Requirements Status](https://requires.io/github/dfid-dvs/server/requirements.svg?branch=master)](https://requires.io/github/dfid-dvs/server/requirements/?branch=master)     [![Maintainability](https://api.codeclimate.com/v1/badges/53490fd15b757a876b6a/maintainability)](https://codeclimate.com/github/naxadeve/dvsphase2/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/53490fd15b757a876b6a/test_coverage)](https://codeclimate.com/github/naxadeve/dvsphase2/test_coverage) ![version](https://img.shields.io/badge/python-v3.6-blue)

### Pipeline Test Status :

| Stages | Status |
| ------ | ------ |
|  Production | [![CircleCI](https://circleci.com/gh/dfid-dvs/server/tree/master.svg?style=svg)](https://circleci.com/gh/dfid-dvs/server/tree/master) |
| Staging  | [![CircleCI](https://circleci.com/gh/naxadeve/dvsphase2/tree/master.svg?style=svg)](https://circleci.com/gh/naxadeve/dvsphase2/tree/master) |
| Development | [![CircleCI](https://circleci.com/gh/naxadeve/dvsphase2/tree/test-server-setup.svg?style=svg)](https://circleci.com/gh/naxadeve/dvsphase2/tree/test-server-setup)

### Steps To Follow

- Clone this repository

- Install docker and docker-compose in your system.
 Docker Refrence [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

- Create a symlink with name docker-compose.yml to docker-compose.local.yml
```sh
   ln -s docker-compose.yml  docker-compose.local.yml
 ```


- Rename .env_sample to .env and change it settings accordingly for the project

- Inside dvs folder rename local_settings_sample.py to local_settings.py and change it settings accordingly for the project

- Bulid docker image
```sh
   docker-compose build
 ```

- Run external services
```sh
   docker-compose -f external_services.yml up -d
 ```

- Run the project in docker
```sh
   docker-compose up -d
 ```

>Note:
> for logs run docker-compose logs -f --tail 100
>check docker container status docker ps / docker ps -a
