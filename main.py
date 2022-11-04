import os,sys
from time import sleep
import re

import configparser

import joe_def_v2 as sw



# Init PythonConfigParser via Config.ini
try:
    config = configparser.ConfigParser()
    config.read('AtenConfig.ini')
    aten_account = config['Auth']['Account']
    aten_password = config['Auth']['Password']
    aten_local_version = config['Firmware']['FirmwareFileName']
    aten_target_version = config['Firmware']['FinalVersion']
except (NameError, KeyError):
    print("AtenConfig.ini Args Error. Try the following example below : " + sw.col_yellow() + '''
[Auth]
Account = admin
Password = P@ssw0rd

[Firmware]
FirmwareFileName = SN01_SN91xx_V1.7.167.003.fw
FinalVersion = 1.7.167''' + sw.col_def())
    sw.pause_exit0()
except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    raise

# Import os, get Dir and filename.
local_dir = (os.path.abspath(os.getcwd()))
upload_path = local_dir + "/" + aten_local_version


# Init IP List and Loop it.

# Init Driver and Login.
try:
    guw = sw.GetUniWebdriver()
    driver = guw.windows()
    sw.login(driver, "https://192.168.92.101/")

    Hostname = sw.gettext(driver, "xpath", "//*[@id='contentlayer']/div/form/table/tbody/tr/td/div[2]")
    print("Connection Successful, Hostname = "+ sw.col_yellow() + Hostname + sw.col_def(), end=', ')

    sw.input(driver, "name", "login_username", aten_account)
    sw.input(driver, "name", "login_password", aten_password)
    sw.click(driver, "id", "B_LOGIN")

    # Click Diag Box.
    try:
        sw.click(driver, "id", "DialogCmdCancel")
    finally:
        pass


    # Check Firmware Version.
    try:
        # Get source Alert Message.
        sw.click(driver, "id", "IM_ABOUT")
        alert = driver.switch_to.alert.text

        # Split it.
        alert_split = driver.switch_to.alert.text.split(' ', 4)
        sed = alert_split[2].split('\n', 1)
        version = sed[0]
        driver.switch_to.alert.accept()
        print("Version = " + sw.col_yellow() + version + sw.col_def())


    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    # Firmware Version less then Target , Upgrade it !
    if aten_target_version == version:
        print("version ==")
        driver.quit()
    elif aten_target_version != version:
        print(sw.col_pu() + "Detected Version Not Match " + version + " != " + aten_target_version + sw.col_def())

        # Switch to Firmware Page
        sw.click(driver, "id", "LM_MAINTENANCE")
        sw.click(driver, "id", "LMS_UPGRADE")
        sw.click(driver, "name", "CheckVersion")
        sw.input(driver, "name", "FirmwareFile", upload_path)
        sw.click(driver, "xpath", "//div[@id='CMD_UPGRADE']/input")
        #print("Summit Pressed")

    try:
        upload_progress = 0
        print("Upload Progress : ", end='')
        while upload_progress < 100:
            sleep(3)
            upload_progress_raw = sw.gettext(driver, "id", "uploadMessage")
            upload_progress_with_pre = upload_progress_raw.split(' ', 5)
            upload_progress = upload_progress_with_pre[0]
            upload_progress = int(re.sub("%", '', upload_progress))
            print(str(upload_progress) + "%  ", end='')
            #if upload_progress == 'P': upload_progress = 0
            #sleep(3)
        print("Done ...")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])

    try:
        sleep(5)
        upload_upgradeMessage = sw.gettext(driver, "id", "upgradeMessage")
        if 'upgrade' in upload_upgradeMessage:
            print("Detected Upgrade Progressing Bar, Terminate the WebDriver.")
            driver.quit()
            pass
        else:
            print(sw.col_red() + "Not Detected Progressing Bar !! Keep going, We check it later." + sw.col_def())
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        driver.quit()



except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    driver.quit()
    raise

# Loop IP List Again for Checking version is match.
