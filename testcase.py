from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
import warnings
warnings.filterwarnings('ignore')

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '11'
desired_caps['deviceName'] = 'Pixel 2 API 30'
desired_caps['appPackage'] = 'com.dnielfe.manager'
desired_caps['appActivity'] = 'com.dnielfe.manager.BrowserActivity'
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

time.sleep(2)

def createFile(filename):
    createBtn = driver.find_elements_by_id("com.dnielfe.manager:id/fabbutton")
    if createBtn:
        createBtn[0].click()
    time.sleep(1)
    createOpts = driver.find_elements_by_id("android:id/title")
    if createOpts:
        createOpts[0].click()
    else:
        print("newfile failed")

    time.sleep(1)

    for item in filename:
        driver.press_keycode(ord(item)-97+29)

    time.sleep(1)
    FinalCreate = driver.find_elements_by_id("android:id/button1")#click ok 
    if FinalCreate:
        FinalCreate[0].click()
    time.sleep(1)
    
def createDir(dirname):
    createBtn = driver.find_elements_by_id("com.dnielfe.manager:id/fabbutton")
    if createBtn:
        createBtn[0].click()
        
    time.sleep(1)

    #class:android.widget.TextView
    createOpts = driver.find_elements_by_id("android:id/title")
    for item in createOpts:
        if item.text == "Create new folder":
            item.click()
            break;

    time.sleep(1)

    for item in dirname:
        driver.press_keycode(ord(item)-97+29)

    time.sleep(1)
    FinalCreate = driver.find_elements_by_id("android:id/button1")#click ok 
    if FinalCreate:
        FinalCreate[0].click()
    time.sleep(1)

def deleteFile(filename):
    FileList = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in FileList:
        if item.text == filename:
            TouchAction(driver).long_press(item,duration=3000).release().perform()#长按
            options = driver.find_elements_by_id("com.dnielfe.manager:id/search")[0]
            options.click()
            time.sleep(2)
            delete_button = driver.find_elements_by_class_name("android.widget.LinearLayout")[1]
            delete_button.click()
            time.sleep(2)
            driver.find_elements_by_id("android:id/button1")[0].click()
            break
        
def copyFile(filename):
    FileList = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in FileList:
        if item.text == filename:
            TouchAction(driver).long_press(item,duration=3000).release().perform()#长按
            options = driver.find_elements_by_id("com.dnielfe.manager:id/folderinfo")[0]
            options.click()
            time.sleep(2)
            break
        
def cutfile(filename):
    FileList = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in FileList:
        if item.text == filename:
            TouchAction(driver).long_press(item,duration=3000).release().perform()#长按
            options = driver.find_elements_by_id("com.dnielfe.manager:id/actionmove")[0]
            options.click()
            time.sleep(2)
            break

def testfile(filename):
    TestNewFile = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in TestNewFile:
        if item.text == filename:
            #print(filename,"test successed")
            return True
    return False
    
def testNofile(filename):
    TestNewFile = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in TestNewFile:
        if item.text == filename:
            return False
    return True

def clickFile(filename):
    TestNewFile = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    for item in TestNewFile:
        if item.text == filename:
            item.click()
            break
    time.sleep(3)

def rename_firstfile(newname):
    FirstFile = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
    TouchAction(driver).long_press(FirstFile[0],duration=3000).release().perform()#长按

    time.sleep(2)
    driver.find_elements_by_id("com.dnielfe.manager:id/search")[0].click() #options

    time.sleep(2)
    rename = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]#click rename button
    rename.click()

    time.sleep(2)
    for item in newname:
        driver.press_keycode(ord(item)-97+29)

    time.sleep(2)
    driver.find_elements_by_id("android:id/button1")[0].click()
    time.sleep(2)
    
#点击allow
allow = driver.find_elements_by_id("com.android.permissioncontroller:id/permission_allow_button")
allow[0].click()
time.sleep(2)

#新建testdir文件夹
createDir("atestdir")

clickFile("atestdir")

#测试新建文件功能
createDir("aa")
createFile("bb")
createDir("acopysrc")
createDir("acutsrc")
if testfile("aa"):
    print("create dir successed")
if testfile("bb"):
    print("create file successed")

#测试重命名功能
Filelist = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
OriginalFirstFilename = Filelist[0].text
rename_firstfile("aa")
if testfile("aa"+ OriginalFirstFilename):
    print("test rename successed")

#测试删除功能
deleteFile("aa"+ OriginalFirstFilename)

time.sleep(2)
NewFileList = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")

if testNofile("aa"+ OriginalFirstFilename):
    print("delete test successed")
else:
    print("delete failed")

#返回上一级
driver.back()


#测试排序功能，以alpha排序为例，此处验证升序
FileList = driver.find_elements_by_id("com.dnielfe.manager:id/top_view")
FilenameList = [item.text for item in FileList]
print(FilenameList)

flag = 1
for i in range(0,len(FilenameList)-1):
    if(FilenameList[i].lower() > FilenameList[i+1].lower()):
        flag = 0
        break
    
if not flag:
    print("sort failed")
else:
    print("sort successed")

#测试复制功能
#id:com.dnielfe.manager:id/folderinfo id2:com.dnielfe.manager:id/paste
clickFile("atestdir")
copyFile("acopysrc")
driver.back()
paste = driver.find_elements_by_id("com.dnielfe.manager:id/paste")[0]
paste.click()
time.sleep(1)
driver.swipe(540,1000,540,1550)
if testfile("acopysrc"):
    print("copy successed")
else:
    print("copy failed")

#测试剪切功能 com.dnielfe.manager:id/actionmove
clickFile("atestdir")
cutfile("acutsrc")
driver.back()
paste = driver.find_elements_by_id("com.dnielfe.manager:id/paste")[0]
paste.click()
time.sleep(1)
driver.swipe(540,1000,540,1550)
flag1 = testfile("acutsrc")
clickFile("atestdir")
flag2 = testNofile("acutsrc")
if flag1 and flag2:
    print("cut test successed")
else:
    print("cut test failed")
driver.back()

#删除atestdir、acopysrc、acutsrc
driver.swipe(540,1000,540,1550)
deleteFile("atestdir")
deleteFile("acopysrc")
deleteFile("acutsrc")

time.sleep(2)

if testNofile("atestdir") and testNofile("acoptsrc") and testNofile("acutsrc"):
    print("delete 3dirs successed")
else:
    print("delete 3dirs failed")

time.sleep(2)
driver.quit()
