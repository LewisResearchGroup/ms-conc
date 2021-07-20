from setuptools import setup, find_packages

install_requires = [
    'pandas', 
    'streamlit',
    'molmass',
    'ms-mint'
]

config = {
    'description': 'compute concentration by using standard curves',
    'author': 'luis-ponce and soren-wacker',
    'url': 'https://github.com/luis-ponce',
    'download_url': 'https://github.com/luis-ponce/ms_mint_conc',
    'author_email': 'luisfponcinho@gmail.com',
    'version': '0.0.1',
    'install_requires': install_requires,
    'packages': find_packages(),
    'scripts': [],
    'name': 'ms_mint_conc'
}

setup(**config)
