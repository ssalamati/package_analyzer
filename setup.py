from setuptools import setup, find_packages

setup(
    name='package_analyzer',
    version='0.1.0',
    author='Sami Salamati',
    author_email='salamati9819@gmail.com',
    description='A tool for analyzing Debian package statistics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ssalamati/package_analyzer',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'PyYAML', 
        'tenacity', 
        'tqdm'
    ],
    classifiers=[],
    package_dir={"package_analyzer": "package_analyzer"},
    include_package_data=True,
    scripts=[
        "bin/package_analyzer",
    ],
    data_files = [('.', ["etc/config.yml"])],
)
