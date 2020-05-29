import json


from API_Automation.utilities.BaseClass import BaseClass
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())




class Test_LoadTest_logout(BaseClass):
    def test_load_logout(self):
        END_POINT = '/seller-app/v1/logout'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token}
        req = requests.delete(url=URL, headers=headers).json()
        print(req)
        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Logout Successfully'
