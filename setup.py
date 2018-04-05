from setuptools import setup

setup(name='crimeX',
      version='1.0',
      description='makentu2018 project',
      url='http://github.com/reggiehsu111/crimeX',
      author='reggiehsu111',
      author_email='reggiehsu111@gmail.com',
      license='MIT',
      packages=['crimeX'],
      install_requires=[
          'speech_recognition', 'textblob', 'numpy', 'cv2', 're'
      ],
      zip_safe=False)