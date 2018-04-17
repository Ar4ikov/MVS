# | Created by Ar4ikov
# | Время: 17.04.2018 - 09:06

import setuptools as setUp
import mvs_client

setUp.setup(
    name='mvs_client',
    version=mvs_client.__version__,
    requires=['requests'],
    install_requires=['requests'],
    packages=['mvs_client'],
    url='https://github.com/Ar4ikov/MVS',
    license='MIT License',
    author='Nikita Archikov',
    author_email='bizy18588@gmail.com',
    description='MVS API Client',
    keywords='MAV MVS MVS_Client mvs mvs_client'

)