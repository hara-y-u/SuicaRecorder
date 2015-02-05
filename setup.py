#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
import os
import shutil
from subprocess import call


class NfcpyPackage:
    'Nfcpy package manipulation.'

    BRANCH_URL = 'lp:nfcpy'

    def __init__(self, dist_dir):
        self.dist_dir = dist_dir
        self.src_true_path = os.path.join(dist_dir, 'nfcpy')
        self.lib_true_path = os.path.join(self.src_true_path, 'nfc')
        self.lib_path = os.path.join(dist_dir, 'nfc')

    def branch_repo(self, dist_dir):
        pwd = os.getcwd()
        os.chdir(dist_dir)
        call(['bzr', 'branch', NfcpyPackage.BRANCH_URL])
        os.chdir(pwd)

    def clean(self):
        shutil.rmtree(self.src_true_path)

    def install(self):
        'Install nfcpy.'
        self.branch_repo(self.dist_dir)
        os.unlink(self.lib_path)
        os.symlink(self.lib_true_path, self.lib_path)


class CustomInstallCommand(install):
    'Customized setuptools install command.'

    ROOT = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.join(ROOT, 'src')

    def run(self):
        nfcpy = NfcpyPackage(
            dist_dir=CustomInstallCommand.SRC_DIR
        )
        nfcpy.install()
        install.run(self)


setup(
    name='suicarecorder',
    version='0.0.1',
    description='Suica Log Record Utility.',
    author='yukihiro hara',
    author_email='yukihr@gmail.com',
    install_requires=['pyusb', 'cement',
                      'scrapelib', 'lxml'],
    url='http://github.com/SuicaLogRecorder',
    cmdclass={
        'install': CustomInstallCommand,
    }
)
