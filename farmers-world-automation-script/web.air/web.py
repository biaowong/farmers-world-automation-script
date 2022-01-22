# -*- encoding=utf8 -*-
"""基于 Chrome 浏览器的自动化操作脚本"""

from airtest.core.api import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from airtest_selenium.proxy import WebChrome

using("log.air")
from log import logger


# 连接已存在的 Chrome 浏览器
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = WebChrome(chrome_options=chrome_options)
driver.implicitly_wait(20)

auto_setup(__file__)

# 登录网页
# driver.get(r'https://play.farmersworld.io/')
# driver.implicitly_wait(20)


def login_wax_wallet():
    """登录钱包"""
    # 存储原始窗口的 ID
    original_window = driver.current_window_handle

    driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div/button").click()
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/button/p").click()
    driver.switch_to_new_tab()
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id=\"root\"]/div/section/div[2]/div/div/button/div").click()
    driver.switch_to_new_tab()
    driver.implicitly_wait(20)
    driver.find_element_by_name("userName").send_keys("xxxxxx@xxx.xxx")
    driver.implicitly_wait(20)
    driver.find_element_by_name("password").send_keys("xxxxxx")
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div/div[5]/div/div/div/div[4]/button").click()
    driver.implicitly_wait(20)
    sleep(60)
    # 回到最初窗口
    driver.switch_to_window(original_window)

def enter_map(map_name):
    """进入地图"""
    map_imgs = {
        'mining': 'home-map-bg.jpg',
        'chicken': 'chicken-map.jpg',
        'plant': 'crop-map.jpg',
        'cow': 'cow-map.jpg'
    }

    try:
        driver.find_element_by_xpath("//img[@src='/Map.png']").click()
        driver.implicitly_wait(20)
        driver.find_element_by_xpath("//span[@style='background-image: url(\"./img/" + map_imgs[map_name] + "\"); filter: grayscale(0);']").click()
        driver.implicitly_wait(20)
    except NoSuchElementException as nsee:
        logger.debug(nsee)
        return False

# 进入 Mining
def mining_water():
    """采矿浇水"""
    logger.debug("mining_water")

# 进入 Chicken
def chicken_water():
    """小鸡浇水"""
    logger.debug("chicken_water")

# Plant 相关
def get_energy():
    """获取能量"""
    return int(driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[1]/section[1]/div[5]/div[2]/div").get_attribute("innerHTML"))

def loop_plant_water():
    """给种子循环浇水"""
    for i in range(1, 9):
        logger.debug(i)
        try:
            energy = get_energy() # 获取能量
            logger.debug(energy)
            # 能量大于 200 且浇水间隔时间为 0 时才能浇水
            if energy > 200:
                driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div/div/section/div/section/img[" + str(i) + "]").click()
                driver.implicitly_wait(20)
                # 获取浇水时间
                water_time = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[1]/div[1]/section/div/div/div[2]/div[2]/div").get_attribute("innerHTML")
                logger.debug(water_time)
                if water_time == "00:00:00":
                    driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div/div/section/div/div/div[2]/div[3]/div/button/div").click()
                    driver.implicitly_wait(20)
                    sleep(10)
        except NoSuchElementException as nsee:
            logger.debug(nsee)

    energy = get_energy() # 再次获取能量
    if energy > 200 and energy != 500: # 如果能量大于200 说明点击有问题或遗漏，需要重新点击一次
        sleep(60)
        loop_plant_water()

# 循环执行浇水任务
def plant_water():
    """植物浇水"""
    # 进入 Plant
    enter_map("plant")
    # 给种子循环浇水
    loop_plant_water()

    # 补充能量
    try:
        # 能量等于 200 时充值
        energy = get_energy()
        if energy == 200:
            driver.find_element_by_xpath("//img[@src='./img/plus.png']").click()
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("//input[@type='number']").send_keys("300")
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/button/div").click()
            driver.implicitly_wait(20)
    except NoSuchElementException as nsee:
        logger.debug(nsee)
        return False

# 进入 Cow
def cow_water():
    """奶牛浇水"""
    logger.debug("cow_water")

def loop_action():
    """循环执行任务"""
    while True:
        plant_water()
        cow_water();
        sleep(30)

loop_action()

