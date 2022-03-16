from setuptools import setup

setup(
    name='MTG Card Generator',
    packages=['mtg_card_generator'],
    description='Machine learning tool to automatically generate Magic: The Gathering cards',
    version='0.1',
    url='',
    author='Benjamin M. Syiek',
    author_email='',
    keywords=['machine learning', 'magic: the gathering', 'markov model'],
    entry_points={
        'console_scripts': [
            "make_mtg_card = mtg_card_generator.scripts.make_mtg_card:main"
        ]
    }
)
