#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
import os
import urllib2
import tarfile
import shutil


class CustomInstallCommand(install):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    TMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
    SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
    NFCPY_VERSION = '0.9.2'
    NFCPY_VERSION_TO_MINOR = '.'.join(NFCPY_VERSION.split('.')[0:2])
    NFCPY_SRC_TARBALL = 'nfcpy-%s.tar.gz' % NFCPY_VERSION
    NFCPY_SRC_URL = 'https://launchpad.net/nfcpy/%s/%s/+download/%s' \
                    % (NFCPY_VERSION_TO_MINOR,
                       NFCPY_VERSION,
                       NFCPY_SRC_TARBALL)
    TMP_NFCPY_SRC_TARBALL_PATH = os.path.join(TMP_DIR, NFCPY_SRC_TARBALL)
    NFCPY_SRC_DIST = os.path.join(SRC_DIR, 'nfcpy')

    'Get tmp directory for project making it if not exists.'
    def get_create_tmp_dir(self):
        tmp_dir = CustomInstallCommand.TMP_DIR
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        return tmp_dir

    'Get nfcpy source tarball.'
    def download_nfcpy(self, src_url, dist_path):
        response = urllib2.urlopen(src_url)
        blob = response.read()
        file = open(dist_path, 'w')
        file.write(blob)
        file.close

    'Extract nfcpy source.'
    def extract_nfcpy_src(self, tarball_path, dist_path):
        tar = tarfile.open(tarball_path)
        tar.extractall(dist_path)
        tar.close()

    'Install nfcpy.'
    def install_nfcpy(self):
        src_url = CustomInstallCommand.NFCPY_SRC_URL
        tarball = CustomInstallCommand.NFCPY_SRC_TARBALL
        tmp_dir = self.get_create_tmp_dir()
        tar_dist_path = os.path.join(tmp_dir, tarball)
        src_dist_path = CustomInstallCommand.NFCPY_SRC_DIST
        if not os.path.exists(tar_dist_path):
            self.download_nfcpy(src_url, tar_dist_path)
        if os.path.exists(src_dist_path):
            shutil.rmtree(src_dist_path)
        self.extract_nfcpy_src(tar_dist_path, src_dist_path)

    'Customized setuptools install command - install nfcpy.'
    def run(self):
        self.install_nfcpy()
        install.run(self)


setup(
    name='suicarecorder',
    version='0.0.1',
    description='Suica Log Record Utility.',
    author='yukihiro hara',
    author_email='yukihr@gmail.com',
    install_requires=['pyusb', 'cement'],
    url='http://github.com/SuicaLogRecorder',
    cmdclass={
        'install': CustomInstallCommand,
    }
)
