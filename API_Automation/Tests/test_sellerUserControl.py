import json
from _csv import writer
from random import randint
from password_generator import PasswordGenerator
from selenium.webdriver.common.keys import Keys
from time import sleep
from API_Automation.utilities.BaseClass import BaseClass
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_SellerDetails_Onboard(BaseClass):

    def test_sellerDetails_WithoutToken(self):
        '''
        1) hit api without access token
        '''
        END_POINT = '/seller-app/v1/seller-details'
        URL = self.BASE_URl + END_POINT
        req = requests.get(url=URL).json()
        assert req['code'] == 4002
        assert req['message'] == 'Token is mandatory'

    def test_sellerDetails_withToken(self):
        '''
             1) hit api with access token
             '''
        END_POINT = '/seller-app/v1/seller-details'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token}
        req = requests.get(url=URL, headers=headers).json()
        assert req['code'] == 2000
        assert req['message'] == 'Request Successful'

    def test_sellerExist_withToken(self):
        '''
             1) hit api with access token
             '''
        END_POINT = '/seller-app/v1/seller-exists'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token}
        req = requests.get(url=URL, headers=headers).json()
        assert req['code'] == 2000
        assert req['message'] == 'Request Successful'

    def test_sellerExist_withoutToken(self):
        '''
             1) hit api without access token
             '''
        END_POINT = '/seller-app/v1/seller-exists'
        URL = self.BASE_URl + END_POINT
        req = requests.get(URL).json()
        assert req['code'] == 4002
        assert req['message'] == 'Token is mandatory'

    def test_logout(self):
        END_POINT = '/seller-app/v1/logout'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token}
        req = requests.delete(url=URL, headers=headers).json()
        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Logout Successfully'

    def test_logout_WithoutToken(self):
        END_POINT = '/seller-app/v1/logout'
        URL = self.BASE_URl + END_POINT
        req = requests.get(url=URL).json()
        assert req['code'] == 4002
        assert req['message'] == 'Token is mandatory'

    def test_logout_tokenExpire(self):
        END_POINT = '/seller-app/v1/logout'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token}
        req = requests.delete(url=URL, headers=headers).json()
        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Logout Successfully'
        req = requests.delete(url=URL, headers=headers).json()
        assert req['status'] == 'UNAUTHORIZED'
        assert req['code'] == 4003
        assert req['message'] == 'Invalid access token'

    def test_updatePassword_withToken(self):
        pwo = PasswordGenerator()
        new_pass = pwo.generate()
        data = {
            "password": new_pass
        }
        self.password = new_pass
        END_POINT = '/seller-app/v1/change-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token, "Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers,
                           data=json.dumps(data)).json()

        with open(self.login_filename, 'a') as file:
            csv_writer = writer(file)
            csv_writer.writerow([self.user, self.password])

        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Password change successfully'

    def test_updatePassword_invalid(self):

        data = {
            "password": ''
        }
        END_POINT = '/seller-app/v1/change-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Authorization": self.bearer_token, "Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers,
                           data=json.dumps(data)).json()
        assert req['message'] == 'password is mandatory'
        assert req['status'] == 'BAD_REQUEST'
        assert req['code'] == 4000

    def test_updatePassword_WithoutToken(self):
        pwo = PasswordGenerator()
        new_pass = pwo.generate()
        data = {
            "password": new_pass
        }
        self.password = new_pass
        END_POINT = '/seller-app/v1/change-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers,
                           data=json.dumps(data)).json()

        assert req['status'] == 'UNAUTHORIZED'
        assert req['code'] == 4002
        assert req['message'] == 'Token is mandatory'

    def test_forgotPassword(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000


    def test_forgotPassword_invalidSeller(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        user = 'randomInvalidUsertestdata'
        data = dict(sellerId=user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'NOT_FOUND'
        assert req['message'] == 'Seller not found for given seller id'
        assert req['code'] == 4031

    # forget-password -> validate OTP ->  resend-otp (optional) -> Change user pass

    def test_validate_OTP(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT `MOBILE_AUTHCODE` FROM `octubi` where UBILOGIN = %s"
                cursor.execute(sql, (self.user,))
                result = cursor.fetchone()
        finally:
            connection.close()
        END_POINT = '/seller-app/v2/forget-password-passcode'
        URL = self.BASE_URl + END_POINT
        data = dict(otp=result[0], sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Request Successful'

    def test_validate_OTP_From_email(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT `MOBILE_AUTHCODE` FROM `octubi` where UBILOGIN = %s"
                cursor.execute(sql, (self.user,))
                result = cursor.fetchone()
        finally:
            connection.close()

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://www.mailinator.com/')
        driver.maximize_window()
        driver.find_element_by_xpath("//input[@id='addOverlay']").send_keys(self.user)
        driver.find_element_by_xpath("//input[@id='addOverlay']").send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[1]//td[3]"))
        )
        driver.find_element_by_xpath('//tr[1]//td[3]').click()
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        sleep(3)
        otp_fromMail = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/p[4]/strong").text

        assert result[0] == otp_fromMail

        driver.close()

    def test_validateOTP_InvalidOtp(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000
        END_POINT = '/seller-app/v2/forget-password-passcode'
        URL = self.BASE_URl + END_POINT
        data = dict(otp=randint(500000, 999999), sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'BAD_REQUEST'
        assert req['code'] == 4010
        assert req['message'] == 'OTP incorrect. Please enter correct OTP code'

    def test_validateOTP_invalidSeller(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000
        connection = self.get_connection()
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT `MOBILE_AUTHCODE` FROM `octubi` where UBILOGIN = %s"
                cursor.execute(sql, (self.user,))
                result = cursor.fetchone()
        finally:
            connection.close()

        END_POINT = '/seller-app/v2/forget-password-passcode'
        URL = self.BASE_URl + END_POINT
        data = dict(otp=result[0], sellerId='randomUser')
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'NOT_FOUND'
        assert req['code'] == 4031
        assert req['message'] == 'Seller not found for given seller id'

    def test_resendOTP(self):
        END_POINT = '/seller-app/v2/resend-otp'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        requests.put(url=URL, headers=headers, data=json.dumps(data)).json()  # hit resend otp
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT `MOBILE_AUTHCODE` FROM `octubi` where UBILOGIN = %s"
                cursor.execute(sql, (self.user,))
                result = cursor.fetchone()
        finally:
            connection.close()
        END_POINT = '/seller-app/v2/forget-password-passcode'
        URL = self.BASE_URl + END_POINT
        data = dict(otp=result[0], sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Request Successful'

    def test_resendOTP_invalidSeller(self):
        END_POINT = '/seller-app/v2/forget-password'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId=self.user)
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'OK'
        assert req['message'] == 'Otp has been sent to registered emailId/mobile.'
        assert req['code'] == 2000
        END_POINT = '/seller-app/v2/resend-otp'
        URL = self.BASE_URl + END_POINT
        data = dict(sellerId='random-user')
        headers = {"Content-Type": 'application/json'}
        req = requests.put(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'NOT_FOUND'
        assert req['message'] == 'Seller not found for given seller id'
        assert req['code'] == 4031

    def test_changeUser_password(self):
        pwo = PasswordGenerator()
        new_pass = pwo.generate()
        END_POINT = '/seller-app/v2/create-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Content-Type": 'application/json'}
        data = {
            'password': new_pass,
            'sellerId': self.user
        }
        req = requests.post(url=URL, headers=headers, data=json.dumps(data)).json()
        self.password = new_pass

        assert req['status'] == 'OK'
        assert req['code'] == 2000
        assert req['message'] == 'Password change successfully'

        with open(self.login_filename, 'a') as file:
            csv_writer = writer(file)
            csv_writer.writerow([self.user, self.password])

    def test_changeUserPassword_invalidSeller(self):
        END_POINT = '/seller-app/v2/create-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Content-Type": 'application/json'}
        data = {
            'password': self.password,
            'sellerId': 'randomUser'
        }
        req = requests.post(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'NOT_FOUND'
        assert req['message'] == 'Seller not found for given seller id'
        assert req['code'] == 4031

    def test_changeUserPassword_emptyPass(self):
        END_POINT = '/seller-app/v2/create-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Content-Type": 'application/json'}
        data = {
            'password': ' ',
            'sellerId': self.user
        }
        req = requests.post(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'BAD_REQUEST'
        assert req['message'] == 'The field must be at least 6 characters'
        assert req['code'] == 4000

    def test_changeUserPassword_moreThan50Char(self):
        END_POINT = '/seller-app/v2/create-password'
        URL = self.BASE_URl + END_POINT
        headers = {"Content-Type": 'application/json'}
        data = {
            'password': '1234567801234@asasas56789012345678011223344556677889900qazwsxedcrfvtgbyhnujmikolp',
            'sellerId': self.user
        }
        req = requests.post(url=URL, headers=headers, data=json.dumps(data)).json()
        assert req['status'] == 'BAD_REQUEST'
        assert req['code'] == 4000
        assert req['message'] == 'The field must be less than 50 characters'
