from setuptools import setup

with open('requirements.txt') as file:
    requirements = [line.strip() for line in file.readlines()]

setup(
    name='yandex_disk_api',
    version='0.1',
    description='Super minimal Python interface for using Yandex.Disk API.',
    url='https://github.com/ylytkin/yandex-disk-api',
    author='Yura Lytkin',
    author_email='jurasicus@gmail.com',
    license='MIT',
    packages=['yandex_disk_api'],
    install_requires=requirements,
    zip_safe=False,
)
