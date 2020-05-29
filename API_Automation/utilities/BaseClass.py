import pymysql
import pytest

@pytest.mark.usefixtures('setup')
class BaseClass:
    def get_connection(self):
        if self.env_name == 'QA1':
            #print(' inside qa1 db')
            connection = pymysql.connect(host='127.0.0.1',
                                         port=2000,
                                         user='INTGZshopWU',
                                         password='Tfa25eAPSM2s5hqP',
                                         db='zshop_dropship')
            return connection

        if self.env_name == 'QA2':
            #print('inside  QA2 db')
            connection = pymysql.connect(host='127.0.0.1',
                                         port=2000,
                                         user='INTGZshopWU',
                                         password='Tfa25eAPSM2s5hqP',
                                         db='zshop_dropship')
            return connection
