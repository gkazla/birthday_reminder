from setuptools import setup, find_packages

with open('VERSION') as file:
    VERSION = file.read()

with open('README.md') as file:
    README = file.read()

setup(
    name='CommunityBirthdayReminder',
    version=VERSION,
    packages=find_packages(exclude=['.venv', 'venv']),
    description='Sending email remainders to a community members.',
    long_description=README,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'jinja2>=3.1.2,<4.0.0'
    ]
)
