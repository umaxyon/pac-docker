# -*- coding: utf-8 -*-
import os
import platform
from fabric.api import local
from fabric.api import task
from fabric.api import lcd
from fabric.api import path
from fabric.contrib.console import confirm

from fabric_aws_lambda import SetupTask as BaseSetupTask
from fabric_aws_lambda import InvokeTask
from fabric_aws_lambda import MakeZipTask


BASE_PATH = os.path.dirname(__file__)
DICT_PATH = os.path.join(os.path.dirname(BASE_PATH), 'dict')

LIB_PATH = os.path.join(BASE_PATH, 'lib')
INSTALL_PREFIX = os.path.join(BASE_PATH, 'local')

REQUIREMENTS_TXT = os.path.join(BASE_PATH, 'requirements.txt')

LAMBDA_FUNCTION_NAME = os.path.basename(BASE_PATH)
LAMBDA_HANDLER = 'lambda_handler'
LAMBDA_FILE = os.path.join(BASE_PATH, 'lambda_function.py')

EVENT_FILE = os.path.join(BASE_PATH, 'event.json')

ZIP_FILE = os.path.join(BASE_PATH, 'lambda_function.zip')
ZIP_EXCLUDE_FILE = os.path.join(BASE_PATH, 'exclude.lst')


MECAB_PKG = 'mecab-0.996'
MECAB_IPADIC_PKG = 'mecab-ipadic-2.7.0-20070801'
MECAB_NEOLOGD_PKG = 'mecab-ipadic-neologd'

class SetupTask(BaseSetupTask):
    def install_python_modules(self):
        if platform.system() == 'Linux':
            local('echo -e "[install]\ninstall-purelib=\$base/lib64/python" > setup.cfg')

        options = dict(requirements=self.requirements, lib_path=self.lib_path)
        with lcd(BASE_PATH), path(os.path.join(self.install_prefix, 'bin'), behavior='prepend'):
            local('pip install --upgrade -r {requirements} -t {lib_path}'.format(**options))

    def pre_task(self):
        with lcd(self.tempdir):
            local('rm -rf *')
            self.install_mecab(pkg_name=MECAB_PKG)
            self.install_mecab_ipadic(pkg_name=MECAB_IPADIC_PKG)


    def install_mecab(self, pkg_name):
        local('mv {} {}'.format(os.path.join('/root', pkg_name), self.tempdir))
        with lcd(pkg_name):
            local('./configure --prefix={} --enable-utf8-only'.format(self.install_prefix))
            local('make && make install')

    def install_mecab_ipadic(self, pkg_name):
        local('mv {} {}'.format(os.path.join('/root', pkg_name), self.tempdir))
        local('nkf --overwrite -Ew {}/*'.format(pkg_name))
        with lcd(pkg_name), path(os.path.join(self.install_prefix, 'bin'), behavior='prepend'):
            local('{}/libexec/mecab/mecab-dict-index -f utf-8 -t utf-8'.format(self.install_prefix))
            local('./configure')
            local('make install')


        with lcd(DICT_PATH), path(os.path.join(self.install_prefix, 'bin'), behavior='prepend'):
            local('cp -r {} {}'.format(os.path.join(self.tempdir,pkg_name), DICT_PATH))
            local('{}/libexec/mecab/mecab-dict-index -m {} -d {} -u {} -f utf8 -t utf8 -a {}'.format(self.install_prefix, 'mecab-ipadic-2.7.0-20070801.model', os.path.join(DICT_PATH, pkg_name), 'PacPacDev.csv', 'PacPac.csv'), capture=False)
            local('mv PacPac.csv {}'.format(os.path.join(self.tempdir, pkg_name)))

        with lcd(pkg_name), path(os.path.join(self.install_prefix, 'bin'), behavior='prepend'):
            local('{}/libexec/mecab/mecab-dict-index -f utf-8 -t utf-8'.format(self.install_prefix))
            local('make install')


@task
def clean():
    for target in [ZIP_FILE, LIB_PATH, INSTALL_PREFIX]:
        local('rm -rf {}'.format(target))

task_setup = SetupTask(
    requirements=REQUIREMENTS_TXT,
    lib_path=LIB_PATH,
    install_prefix=INSTALL_PREFIX
)

task_makezip = MakeZipTask(
    zip_file=ZIP_FILE,
    exclude_file=ZIP_EXCLUDE_FILE,
    lib_path=LIB_PATH
)

