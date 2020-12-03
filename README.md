# Installing and Development Environment

## Requirements

1. Docker
    - **NOTE:** currently running on [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) + Ubuntu 18.04 for dev env and Ubuntu 20.04 on production build
2. Docker-compose
    - [`docker-compose`](https://phoenixnap.com/kb/install-docker-compose-ubuntu) for ubuntu 18.04

## Dev environment
1. after cloning the repo, cd to the root
2. installing and running: `docker-compose -f docker-compose.dev.yml --build up`
    - **NOTE:** as of the current build, migrations are run which means that every time parameters are changed in certain dockerfiles/docker-compose files/non-application files require a down -> up to avoid the admin migrations application from failing
3. quitting `docker-compose -f docker-compose.dev.yml down`
