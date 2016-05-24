#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cuisine import package_ensure, dir_exists
from fabric.api import *
from fabric.context_managers import path

@task
def python():
    _system_pip()
    pyenv()
    pypackage()

@task
def js():
    node_js()
    frontend()

@task
def perl():
    if not dir_exists("~/.plenv"):
        run("git clone https://github.com/tokuhirom/plenv.git ~/.plenv/")
        run("git clone https://github.com/tokuhirom/Perl-Build.git ~/.plenv/plugins/perl-build/")
    with path("~/.plenv/bin:~/.plenv/shims"):
        run("eval '$(plenv init -)'")
        run("plenv install 5.18.1")
        run("plenv global 5.18.1")
        run("PLENV_INSTALL_CPANM='-v' plenv install-cpanm")
        run("cpanm --self-upgrade")


@task
def R():
    _install_R("3.2.5")
    _install_R("2.15.3")
    _rstudio_server()


def _install_R(version):
    prefix = "$HOME/bin/R-{}".format(version)
    if dir_exists(prefix):
        return
    major_version = version[0]
    url = "https://cran.ism.ac.jp/src/base/R-{}/R-{}.tar.gz".\
        format(major_version, version)
    with cd("/tmp"):
        run("wget {}".format(url))
        run("tar xzvf R-{}.tar.gz".format(version))
        with cd("R-{}".format(version)):
            run("./configure --prefix={} --with-x=no".format(prefix))
            run("make && make install")

def _rstudio_server():
    if run('which rstudio-server').return_code == 0:
        return
    run("wget http://download2.rstudio.org/rstudio-server-rhel-0.99.441-x86_64.rpm")
    sudo("yum -y install --nogpgcheck rstudio-server-rhel-0.99.441-x86_64.rpm")


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
