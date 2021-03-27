from setuptools import setup, find_packages

setup(
        name='Flask-Template',
        version='1.0',
        long_description=__doc__,
        python_requires='>= 3.8',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Werkzeug==1.0.1',
            'Wheel==0.36.2',
            'Pytest==6.2.2',
            'Cryptography==3.4.6',
            'Python-Dotenv==0.13.0',
            'Flask==1.1.2',
            'Flask-Blueprint==1.3.0',
            'Flask-Migrate==2.5.3',
            'Flask-Cors==3.0.9',
            'Flask-Assets==2.0',
            'Flask-login==0.5.0',
            'Flask-mail==0.9.1',
            'SQLAlchemy==1.3.22',
            'Flask-SQLAlchemy==2.4.4',
            'Sqlalchemy-utils==0.36.8',
            'PyMySQL==0.9.3',
            'Jinja2==2.11.1',
            'Jsmin==2.2.2',
            'Cssmin==0.2.0',
            ],

    )
