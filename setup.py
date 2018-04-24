from setuptools import setup

setup(name='snitch',
      version='0.1',
      description='Anonymous product comments',
      url='http://github.com/enot_yoyo/snitch',
      author='a.zotikov,a.lemets,e.homenko,v.shmatov',
      author_email='a.lemets@gmail.com',
      license='MIT',
      packages=['snitch'],
      zip_safe=False,
      install_requires=[
            'flask',
            'flask-sqlalchemy',
            'flask-restful',
            'psycopg2'
      ])
