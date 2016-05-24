#!usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import sudo, run, cd, task, settings
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
CENTOS_VERSION="6"

@task
def prepare():
    _setup_yum()
    _update_git()

def _setup_yum(version=CENTOS_VERSION):
    sudo("yum install -y --skip-broken epel-release")
    sudo("yum install -y --skip-broken http://rpms.famillecollet.com/enterprise/remi-release-{}.rpm".\
         format(version))
    sudo("yum install -y --skip-broken http://pkgs.repoforge.org/rpmforge-release/"
         "rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm")
    sudo("yum install -y --skip-broken https://mirror.webtatic.com/yum/el7/webtatic-release.rpm")
    sudo("curl -s https://setup.ius.io/ | sh")
    sudo("yum install -y --skip-broken centos-release-SCL")
    sudo("yum install -y --skip-broken http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm")


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


