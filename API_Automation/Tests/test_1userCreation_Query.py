import random
from _csv import writer

from API_Automation.utilities.BaseClass import BaseClass
import requests


class Test_createUser_Query(BaseClass):
    def test_BulkUserCreation_Query(self):
        mobile = self.random_mobile()
        email = str(mobile) + '@mailinator.com'

        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                sql = "(select max(`UBIRFNUM`)+1 from octubi);"   #get max UBIRFNUM
                cursor.execute(sql)
                next_ubiRfNum = cursor.fetchone()
                #print('\n ubirf ', next_ubiRfNum[0])
                sql = '''
                 INSERT INTO octubi
(`UBIRFNUM`, `UBILOGIN`, `UBIPASS`, `UBIFNAME`, `UBIMNAME`, `UBILNAME`, `MOBILE`, `ALTERNATE_MOBILE_NO`,
`COMMUNICATION_EMAIL`, `UBIASAADMINACTIVE`, `UBIASAWEBACTIVE`, `UBIISGUESTUSER`, `UBIISACTIVE`, `UBIUSERTYPE`,
`UBIWEBADMINUSERTYPE`, `UBINETWORKID`, `UBIISPRIORITYCUSTOMER`, `UBIORDERCOUNT`, `UBI_COD_OPTION`, `UBICODCOUNT`,
`INACTIVE_TO_ACTIVE_COUNTER`, `RESET_PASSWORD`, `MOBILE_AUTHCODE`, `MOBILE_AUTHENTICATED`, `MOBILE_AUTHCODE_START`,
`MOBILE_AUTHCODE_EXPIRY`, `EMAIL_AUTHCODE`, `EMAIL_AUTHENTICATED`, `EMAIL_AUTHCODE_EXPIRY`, `UBI_OLD_MOBILE`,
`RESET_PASSWORD_DATE`, `UBILASTLOGINDATE`, `CREATEDATE`, `MODIDATE`, `CREATEDBY`, `MODIFIEDBY`, `DELETED`,
`IS_INVITED`, `REFERER_LOGINID`, `REFERER_NAME`, `REFERER_REG_DATE`, `UBIINVITATIONNAME`, `REDEMPTION_MADE_BY_REFERRER`,
`IS_FREEGIFT_MADE_ON_FIRST_PURCHASE`, `UBIWISHLISTURL`, `UBIISWISHLISTPUBLIC`, `UBIPROFILEURL`, `UBIISPROFILEPUBLIC`,
`UBIISNEWSLETTER`, `UBILOYALTYPOINTS`, `UBIGENDER`, `UBIDOB`, `UBICNDOCCUPATION`, `UBICNDHOUSEINCM`, `UBICOMPANYNAME`,
`UBIADDRESS1`, `UBIADDRESS2`, `UBILANDMARK`, `UBI_STD_CODE`, `UBI_PHONE_NO`, `UBI_PHONE_EXT`, `UBIPINCODE`, `UBICITYCODE`,
`UBISTATECODE`, `UBICOUNTRYCODE`, `ORGID`, `UBIACCCODE`, `UBIDTHTYPE`, user_hashcode, `UBIISBLOCKED`, publickey, privatekey)
VALUES(%s , %s, 'efuApbwH1JtkQyM3WGgUgg==', 'Guest', NULL, NULL, NULL, NULL, %s,
'N', 'Y', NULL, 'Y', 'W', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '979936', NULL, SYSDATE(),
SYSDATE(), '979936', NULL, SYSDATE(), NULL, SYSDATE(),
SYSDATE(), SYSDATE(), SYSDATE(), 0, 0, 'N', NULL, NULL,
NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'N', NULL, NULL, NULL, NULL, NULL, NULL, NULL,
NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, '69619cb137f1db52609f16c4e0b75669a684435a6d5f13a69a2b32440e20d504', NULL, NULL, NULL);
                 '''
                cursor.execute(sql, (str(next_ubiRfNum[0]), str(mobile), str(email)))
                connection.commit()
                sql = "(select max(`SSIRFNUM`)+1 from octassi);"   #get max ssirfnum
                cursor.execute(sql)
                next_ssiRfNum = cursor.fetchone()
                #print('\n ssirf ', next_ssiRfNum[0])

                sql = '''
                INSERT INTO octassi
(`SSIRFNUM`, `SSIVMTRFNUM`, `SSICNDTITLE`, `SSICNDVENDORTYPE`, `SSICNDSTORETYPE`, `SSIFNAME`, `SSILNAME`,
`SSIBNAME`, `SSIPHONE`, `SSIPHONE2`, `SSIMOBILE`, `SSIEMAILID`, `SSIOTHERPHONE`, `SSIEMAIL`, `SSIISORDERMAIL`,
`SSISHOPNO`, `SSIAGCODE`, `SSIPOSSTATUS`, `SSIRDCCODE`, `SSIISSELLER`, `SSIISWEB`, `ISDELIVERSTORE`, `ISORDERSTORE`,
`ISWAREHOUSE`, `SSISHIPPINGINFO`, `ISDEFAULTSTORE`, `ISACTIVE`, `ISONLINE`, `SSICNDANNUALTO`, `SSICNDSTAFFSTRGNTH`,
`COMPNYFOUND`, `SSIMJRCLIENT`, `SSISALESEXPRNCE`, `SSISALEEXPRNIFYES`, `SSIPRCNTGCOMITION`, `ISSTORSHIPPER`, `ISASP`,
`SSICATEGORY`, `SSISTOREBRAND`, `SSISTORENATURE`, `SSIVATNO`, `SSILSTNO`, `SSIMCTTNO`, `SSICURRENCY`, `SSIOPENDATE`,
`SSICLOSEDATE`, `SSIBLOCKREASON`, `SSIBLOCKFROM`, `SSIBLOCKTO`, `SSICSTTAXNO`, `SSILEGACYSTORECODE`, `SSIREFRENCENO`,
`SSICONTACTNO`, `DELETED`, `CREATEDATE`, `CREATEDBY`, `MODIDATE`, `MODIFIEDBY`, `ORGID`, `SSICOUNTRYRFNUM`, `SSICITYRFNUM`,
`COMMISSION_TYPE`, `COMMISSION`, `SSIGSTNO`, `SSIPANNO`, `SSITAXZONE`, ssitinno, location_code, end_eff_date, `isEzWarehouse`,
location_name, preference)
VALUES(%s, 571, NULL, NULL, NULL, 'Wega Lifestyle Pvt. Ltd.  ', 'Wega Lifestyle Pvt. Ltd.  ',
NULL, %s, NULL, NULL, NULL, NULL, %s, 'Y', 'TR0000131', NULL, NULL, NULL,
'Y', 'Y', 'N', 'Y', 'Y', NULL, 'Y', 'Y', 'Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'N', '2018-01-12 16:31:56.000',
0, SYSDATE(), 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'ZSH', NULL, 'Y', 'DTDC Warehouse', 98);                '''
                cursor.execute(sql, (next_ssiRfNum[0],mobile, email))
                connection.commit()
                sql = '''
                INSERT INTO zshop_dropship.octausa
                (`USAUBI`, `USASSI`, `CREATEDATE`, `MODIDATE`, `DELETED`, `CREATEDBY`, `MODIFIEDBY`, `ORGID`)
                VALUES (%s, %s, SYSDATE(), SYSDATE(), 'N', 0, 0, 0);
                '''
                cursor.execute(sql, (next_ubiRfNum[0], next_ssiRfNum[0]))
                connection.commit()

                with open(r'..\TestData\user_creation.csv', 'a') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow([mobile, 'AkashGKrishnan'])

                with open(self.login_filename, 'a') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow([self.user, self.password])

        finally:
            connection.close()


    def random_mobile(self):
        return random.randint(1111111111,5555555555)