#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
import os
import urllib2
import tarfile
import shutil


class NfcpyPackage:
    'Nfcpy package manipulation.'

    TARFILE = 'nfcpy-%s.tar.gz'
    SRC_URL = 'https://launchpad.net/nfcpy/%s/%s/+download/%s'

    def __init__(self, version, dist_dir, cache_dir):
        self.version = version
        self.version_to_minor = '.'.join(version.split('.')[0:2])
        self.src_tarball = NfcpyPackage.TARFILE % version
        self.src_url = NfcpyPackage.SRC_URL \
            % (self.version_to_minor,
               self.version,
               self.src_tarball)
        self.dist_dir = dist_dir
        self.src_true_dirname = self.src_tarball[:-len('.tar.gz')]
        self.src_dirname = 'nfcpy'
        self.src_true_path = os.path.join(dist_dir, self.src_true_dirname)
        self.lib_true_path = os.path.join(self.src_true_path, 'nfc')
        self.lib_path = os.path.join(dist_dir, 'nfc')
        self._cache_dir = cache_dir
        self.cache_file = os.path.join(self.cache_dir, self.src_tarball)

    @property
    def cache_dir(self):
        'Get cache directory for project making it if not exists.'
        d = self._cache_dir
        if not os.path.exists(d):
            os.makedirs(d)
        return d

    @property
    def tarball(self):
        f = self.cache_file
        if not os.path.exists(f):
            self.download(self.src_url, f)
        return f

    def download(self, src_url, dist_path):
        'Get nfcpy source tarball.'
        response = urllib2.urlopen(src_url)
        blob = response.read()
        file = open(dist_path, 'w')
        file.write(blob)
        file.close

    def extract_src(self, tarball_path, dist_path):
        'Extract nfcpy source.'
        tar = tarfile.open(tarball_path)
        tar.extractall(dist_path)
        tar.close()

    def clean(self):
        shutil.rmtree(self.cache_file)

    def install(self):
        'Install nfcpy.'
        self.extract_src(self.tarball, self.dist_dir)
        os.symlink(self.lib_true_path, self.lib_path)


class CustomInstallCommand(install):
    'Customized setuptools install command.'

    ROOT = os.path.dirname(os.path.abspath(__file__))
    TMP_DIR = os.path.join(ROOT, 'tmp')
    SRC_DIR = os.path.join(ROOT, 'src')

    def run(self):
        nfcpy = NfcpyPackage(
            version='0.9.1',
            dist_dir=CustomInstallCommand.SRC_DIR,
            cache_dir=CustomInstallCommand.TMP_DIR
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
