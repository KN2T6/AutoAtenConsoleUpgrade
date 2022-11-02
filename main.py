
import joe_def_v2 as sw
from time import sleep

# Init PythonConfigParser via Config.ini

# Init IP List and Loop it.

# Init Driver and Login.
try:
    guw = sw.GetUniWebdriver()
    driver = guw.windows()
    sw.login(driver, "https://192.168.92.101/")

    sw.input(driver, "name", "login_username", "admin")
    sw.input(driver, "name", "login_password", "P@ssw0rd")
    sw.click(driver, "id", "B_LOGIN")

# Click Diag Box.
    try:
        sw.click(driver, "id", "DialogCmdOK")
        sleep(5)
    except:
        print("error")

# Check Firmware Version.

# Firmware Version less then Target , Upgrade it !

# Switch to Firmware Page
    sw.click(driver, "id", "LM_MAINTENANCE")
    sw.click(driver, "id", "LMS_UPGRADE")
    sw.click(driver, "name", "CheckVersion")
    #sw.click(driver, "name", "FirmwareFile")

    #chooseFile = sw.find_ele(driver, "name", "FirmwareFile")
    #chooseFile = sw.find_ele(driver, "xpath", "/html/body/div[3]/div[3]/div[1]/div[36]/div/form/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/input")
    #chooseFile.click()
    #chooseFile.send_keys("SN01_SN91xx_V1.7.167.003.fw")
    sw.input(driver, "name", "FirmwareFile", "N:\Firmware\ATEN\SN01_SN91xx_V1.7.167.003.fw")
    sw.click(driver, "xpath", "//div[@id='CMD_UPGRADE']/input")



    sleep(10)
    driver.quit()
except:
    sleep(10)
    driver.quit()
    raise

# Loop IP List Again for Checking version is match.