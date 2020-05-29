import inspect
import logging
from _csv import reader

import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        "--ENV_NAME", action="store", default="QA1"
    )


@pytest.fixture()
def setup(request):
    request.cls.env_name = request.config.getoption("ENV_NAME")

    if request.cls.env_name == 'QA1':
        #print('inside qa1 setup')
        request.cls.BASE_URl = 'http://qa1.ezmall.com:20001'
        request.cls.login_filename = '..\TestData\login.txt'

    elif request.cls.env_name == 'QA2':
        #print('inside qa2 setup')
        request.cls.BASE_URl = 'http://qa1.ezmall.com:20001'
        request.cls.login_filename = '..\TestData\qa2_login.txt'


    with open(request.cls.login_filename) as file:
        csv_Reader = list(reader(file))[::-1]
        user = csv_Reader[1][0]
        password = csv_Reader[1][1]

    #print(f'user: {user}, Password: {password}')
    try:
        URL = 'http://qa1.ezmall.com:20009/oauth/token'
        data = dict(grant_type='password', username=user, password=password)
        req = requests.post(url=URL, auth=('client', 'secret'), data=data).json()
        access_token = req['access_token']
        request.cls.bearer_token = "Bearer "+ access_token
    except:
        pass
    request.cls.user = user
    request.cls.password = password

    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    fileHandler = logging.FileHandler('logfile.log')
    formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
    fileHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)  # filehandler object

    logger.setLevel(logging.DEBUG)
    request.cls.logger = logger



