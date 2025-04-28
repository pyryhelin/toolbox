import setuptools

setuptools.setup(
    name='logflare',
    version='0.1.11',
    author='Pyry Helin',
    author_email='pyr.hel@gmail.com',
    description='A small logging library for sending logs to Logflare',
    url='https://github.com/pyryhelin/toolbox',
    project_urls = {
        "Bug Tracker": "https://github.com/pyryhelin/toolbox/issues"
    },
    license='MIT',
    packages=['logflare'],
    install_requires=['requests'],
)