#!usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import sudo, run, cd, task, settings
from cuisine import package_ensure
from config import NCC_proxy
import cuisine
cuisine.select_package("yum")
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


