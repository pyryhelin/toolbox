import setuptools

setuptools.setup(
    name='clickup',
    version='0.1.11',
    author='Pyry Helin',
    author_email='pyr.hel@gmail.com',
    description='clickup api wrapper',
    url='https://github.com/pyryhelin/toolbox',
    project_urls = {
        "Bug Tracker": "https://github.com/pyryhelin/toolbox/issues"
    },
    license='MIT',
    packages=['clickup'],
    install_requires=['requests', 'datetime'],
)