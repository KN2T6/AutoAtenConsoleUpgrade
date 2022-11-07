import os, sys
from time import sleep
import re
import csv
import configparser
import joe_def_v2 as sw

from selenium.common.exceptions import TimeoutException
import selenium.common.exceptions as EC

# Init PythonConfigParser via Config.ini
try:
    config = configparser.ConfigParser()
    config.read('AtenConfig.ini')
    aten_account = config['Auth']['Account']
    aten_password = config['Auth']['Password']
    aten_IP_List = config['Auth']['IP_List']
    aten_local_version = config['Firmware']['FirmwareFileName']
    aten_target_version = config['Firmware']['FinalVersion']
except (NameError, KeyError):
    print("AtenConfig.ini Args Error. Try the following example below : " + sw.col_yellow() + '''
[Auth]
Account = admin
Password = P@ssw0rd
IP_List = IP_List.csv

[Firmware]
FirmwareFileName = SN01_SN91xx_V1.7.167.003.fw
FinalVersion = 1.7.167''' + sw.col_def())
    sw.pause_exit0()
except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    raise

# Print Some Junk.
print(sw.col_pu() + "Aten Firmware Auto Upgrader by Kinmax KN2T6" + sw.col_def())
print("")


# Drag and Drop.
if len(sys.argv) > 1:
    dropped_arg = sys.argv
    dropped_file = dropped_arg[1]
    print(sw.col_red() + "Detected Drop File : " + dropped_file + sw.col_def())
    aten_IP_List = dropped_file
else:
    print(sw.col_yellow() + "Not Detected Drag and Drop File, Using Default Parser ./" + aten_IP_List + sw.col_def())

# Import os, get Dir and filename.
local_dir = (os.path.abspath(os.getcwd()))
upload_path = local_dir + "/" + aten_local_version

# Counting IP List.
with open(aten_IP_List, newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    for i, row in enumerate(rows):
        i += 1
    print("Import IP : " + sw.col_yellow() + str(i) + sw.col_def())
    input(sw.col_blue() + "IP Import Correct ? , Press Enter Key to Continue..." + sw.col_def())

# Init IP List and Loop it.
with open(aten_IP_List, newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    for row in rows:
        print("Connecting to " + sw.col_yellow() + row[0] + sw.col_def())

        # Init Driver and Login.
        try:
            guw = sw.GetUniWebdriver()
            driver = guw.windows()
            sw.login(driver, "https://" + row[0] + "/")

            Hostname = sw.gettext(driver, "xpath", "//*[@id='contentlayer']/div/form/table/tbody/tr/td/div[2]")
            print("Connection Successful, Hostname = " + sw.col_yellow() + Hostname + sw.col_def(), end=', ')

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
                print("Unexpected error : @ Check Firmware Version.", sys.exc_info()[0])
                raise

            # Firmware Version less then Target , Upgrade it !
            try:
                if aten_target_version == version:
                    print(sw.col_green() + "Version Matched." + sw.col_def())
                    print("")
                    driver.quit()
                    continue

                elif aten_target_version != version:
                    print(
                        sw.col_pu() + "Detected Version Not Match " + version + " != " + aten_target_version + sw.col_def())

                    # Switch to Firmware Page
                    sw.click(driver, "id", "LM_MAINTENANCE")
                    sw.click(driver, "id", "LMS_UPGRADE")
                    sw.click(driver, "name", "CheckVersion")
                    sw.input(driver, "name", "FirmwareFile", upload_path)
                    sw.click(driver, "xpath", "//div[@id='CMD_UPGRADE']/input")
                    # print("Summit Pressed")

                    upload_progress = 0
                    print("Upload Progress : ", end='')
                    while upload_progress < 100:
                        sleep(3)
                        upload_progress_raw = sw.gettext(driver, "id", "uploadMessage")
                        upload_progress_with_pre = upload_progress_raw.split(' ', 5)
                        upload_progress = upload_progress_with_pre[0]
                        upload_progress = int(re.sub("%", '', upload_progress))
                        print(str(upload_progress) + "%  ", end='')
                        # if upload_progress == 'P': upload_progress = 0
                        # sleep(3)
                    print("Done ...")

                    # sleep(5)
                    upload_upgradeMessage = sw.wait_until(driver, "id", "upgradeMessage")
                    if 'upgrade' in upload_upgradeMessage:
                        print("Detected Upgrade Progressing Bar, Terminate the WebDriver.")
                        print("")
                        driver.quit()
                        pass
                    else:
                        print(
                            sw.col_red() + "Not Detected Progressing Bar !! Keep going, We check it later." + sw.col_def())

            except EC.InvalidArgumentException:
                print("InvalidArgumentException : No Firmware File Detected, Make Sure It Locate in Same Directory.")
                print("InvalidArgumentException : No Firmware File Detected, Make Sure Your AtenConfig.ini is Correct.")
            except Exception:
                print("Unexpected error : @Firmware Version less then Target", sys.exc_info()[0])
                driver.quit()
                raise

        except EC.WebDriverException as err:
            print("CONNECTION ERROR ? ...", end='')
            if 'ERR_CONNECTION_REFUSED' in err.msg:
                print("ERR_CONNECTION_REFUSED")
                driver.quit()
                pass
            print("")
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            driver.quit()
            raise


# Loop IP List Again for Checking version is match.
