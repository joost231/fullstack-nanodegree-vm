# Tournament results

A database schema to store the game matches between players. Combined with a Python module to rank the players and pair them up in matches in a tournament.


## Table of contents

* [Quick start](#quick-start)
* [What's included](#Whats-included)
* [Creator](#creator)


## Quick start

Follow these steps to run the code:
* Clone the repo.
* Download and install Vagrant.
* Boot the vagrant box with the command `vagrant up`.
* Ssh into the vagrant box with the command `vagrant ssh`.
* Go to the tournament folder with `cd /vagrant/tournament`.
* Test the code with the command `tournament_test.py`.


## What's included
Within the download you'll find the following directories and files:

```
vagrant/
├── pg_config.sh
├── Vagrantfile
└── tournament/
    ├── tournament_test.py
    ├── tournament.py
    └── tournament.sql
```


## Creator

**Joost van Schie** (<https://github.com/joost231>)