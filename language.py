#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cuisine import package_ensure
from fabric.api import *

@task
def python():
    _system_pip()
    pyenv()
    pypackage()

@task
def js():
    node_js()
    frontend()

def _system_pip():
    package_ensure("epel-release")
    package_ensure("python-pip")
    sudo("pip install pip --upgrade")


# install pyenv andd virtualenv
def pyenv():
    if exists("~/.pyenv"):
        return
        # run("rm -rf ~/.pyenv")
    run('git clone https://github.com/yyuu/pyenv.git ~/.pyenv')
    run('git clone https://github.com/yyuu/pyenv-virtualenv.git \
        ~/.pyenv/plugins/pyenv-virtualenv')
    with cd("~/.pyenv"):
        run("git pull")
    with shell_env(PATH="$PATH:~/.pyenv/bin"):
        run('pyenv install miniconda3-latest')
        run('pyenv rehash')
        run('pyenv global miniconda3-latest')


def pypackage():
    packages = ['flake8',
                'ipython',
                'jupyter'
                ]
    for package in packages:
        with settings(warn_only=True):
            sudo("pip install {}".format(package))


@task
def node_js():
    run("git clone git://github.com/creationix/nvm.git ~/.nvm")


@task
def frontend():
    pass
