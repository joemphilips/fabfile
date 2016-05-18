#!usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import sudo, run, cd, task
from cuisine import package_ensure
from config import NCC_proxy
import cuisine
cuisine.select_package("yum")
git_dependencies = ["curl-devel",
                    "expat-devel",
                    "gettext-devel",
                    "openssl-devel",
                    "zlib-devel",
                    "perl-ExtUtils-MakeMaker"]
GIT_VERSION="2.8.2"

@task
def _update_git():
    current_version=run('git --version | cut -d" " -f3')
    if current_version == GIT_VERSION:
        return
    sudo("yum -y remove git")
    for git_dependency in git_dependencies:
        package_ensure(git_dependency)
    run("wget https://www.kernel.org/pub/software/scm/git/git-%s.tar.gz" % GIT_VERSION)
    run("tar -zxf git-%s.tar.gz" % GIT_VERSION)
    with cd("git-%s" % GIT_VERSION):
        sudo("make prefix=/usr/local all")
        sudo("make prefix=/usr/local install")


