#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil
from subprocess import call

ROOT = os.path.dirname(os.path.abspath(__file__))


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
        if os.path.exists(self.lib_path):
            os.unlink(self.lib_path)
        os.symlink(self.lib_true_path, self.lib_path)


class CustomInstallCommand(install):
    'Customized setuptools install command.'

    def run(self):
        nfcpy = NfcpyPackage(dist_dir=ROOT)
        nfcpy.install()
        install.run(self)


setup(
    name='suicarecorder',
    version='0.0.1',
    packages='suicarecorder',
    description='Suica Log Record Utility.',
    author='yukihiro hara',
    author_email='yukihr@gmail.com',
    license='MIT',
    keywords='nfc suica finance',
    install_requires=['pyusb>=1.0.0b2', 'cement',
                      'scrapelib', 'lxml'],
    tests_require=['nose'],
    package_data={
        '': ['*.json']
    },
    url='http://github.com/yukihr/SuicaRecorder',
    cmdclass={
        'install': CustomInstallCommand,
    }
)
