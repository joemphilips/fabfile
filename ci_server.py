#!usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import (run, cd, task, sudo, env)
from fabric.context_managers import shell_env, settings
from cuisine import package_ensure
from utils import _update_git
import cuisine
cuisine.select_package("yum")
env.password = "miya0511"


@task
def jenkins():
    _update_git()
    _openjdk()
    _get_repo()
    package_ensure("jenkins")
    nginx()
    with shell_env():
        sudo("/etc/init.d/jenkins start")
        sudo("chkconfig jenkins on")


def _openjdk():
    packages = ["java-1.7.0-openjdk",
                "java-1.7.0-openjdk-devel"]
    for package in packages:
        package_ensure(package)

def _get_repo():
    with cd("/etc/yum.repos.d/"):
        sudo("curl -OL http://pkg.jenkins-ci.org/redhat/jenkins.repo")
        sudo("rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key")

@task
def nginx():
    with settings(warn_only=True):
        sudo("rpm -ivh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm")
        sudo("yum -y install nginx")
