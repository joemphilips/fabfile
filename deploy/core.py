#!usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import *
from cuisine import package_ensure, package_remove

CENTOS_GIT_DEPENDENCIES = ["curl-devel",
                           "expat-devel",
                           "gettext-devel",
                           "openssl-devel",
                           "zlib-devel",
                           "perl-ExtUtils-MakeMaker"]
CENTOS=False
GIT_VERSION="2.8.2"

@task
def update_git():
    current_version=run('git --version | cut -d" " -f3')
    if current_version == GIT_VERSION:
        return
    package_remove("git")
    if CENTOS=True:
        for git_dependency in git_dependencies:
            package_ensure(CENTOS_GIT_DEPENDENCIES)
    run("wget https://www.kernel.org/pub/software/scm/git/git-%s.tar.gz" % GIT_VERSION)
    run("tar -zxf git-%s.tar.gz" % GIT_VERSION)
    with cd("git-%s" % GIT_VERSION):
        sudo("make prefix=/usr/local all")
        sudo("make prefix=/usr/local install")
    _install_git_subtree()


def _install_git_subtree():
    with cd("/tmp"):
        run("curl http://git.kernel.org/cgit/git/git.git/plain/contrib/subtree/git-subtree.sh > git-subtree")
        sudo("mv git-subtree /usr/local/bin")
        sudo("chmod a+x /usr/local/bin/git-subtree")

