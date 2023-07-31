from setuptools import setup, find_packages

install_requires = [
    'pandas', 
    'streamlit',
    'molmass',
    'ms-mint'
]

config = {
    'description': 'compute concentration by using standard curves',
    'author': 'luis-ponce and sorenwacker',
    'url': 'https://github.com/LewisResearchGroup/ms-conc',
    'download_url': 'https://github.com/LewisResearchGroup/ms-conc',
    'author_email': 'luisfponcinho@gmail.com',
    'version': '0.0.1',
    'install_requires': install_requires,
    'packages': find_packages(),
    'scripts': [],
    'name': 'ms_conc'
}

setup(**config)
