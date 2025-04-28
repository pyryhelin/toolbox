import setuptools

setuptools.setup(
    name='vercelKV',
    version='0.1.11',
    author='Pyry Helin',
    author_email='pyr.hel@gmail.com',
    description='rest api for vercel kv',
    url='https://github.com/pyryhelin/toolbox',
    project_urls = {
        "Bug Tracker": "https://github.com/pyryhelin/toolbox/issues"
    },
    license='MIT',
    packages=['vercelKV'],
    install_requires=['requests'],
)