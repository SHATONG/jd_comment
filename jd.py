# 爬取京东商品评论并存储到数据库
# shatong
# 2020-01-10
import time
from mysql.sql import Sql
from selenium import webdriver
import configparser
from log.logger import log

# 从配置文件中读取相关参数
conf = configparser.ConfigParser()
conf.read('config/conf.ini', encoding='utf-8')
HostUrl = conf.get('conf', 'host')
comment_type = conf.get('conf', 'comment_type')
print(HostUrl)
log.debug("------已取得url，准备爬取评论------")
driver = webdriver.Chrome()
driver.maximize_window()


# 打开京东详情页
def py_jd_product_detail():
    try:

        driver.get(HostUrl)
        time.sleep(10)
        gun()
        closeAD()
    except Exception as e:
        log.error("-------详情页面打开失败，准备重试------")
        driver.close()
        py_jd_product_detail()


# 打开京东评论页面
def py_jd_comment():
    try:
        btn_comment = driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[5]')
        btn_comment.click()
        time.sleep(3)
        gun()
        # 首次打开，保存首页内容
        save_comment()
          try:
            # 打开下一页内容
            btn_last_nums = driver.find_elements_by_xpath('//a[@class="ui-pager-next"]/preceding-sibling::a')
            btn_last_num = btn_last_nums[-1].text
            last_num = int(btn_last_num)
            print('最后一页的页码为：', last_num)
            for i in range(1, 1000):
                print("当前页码为", i)
                btn_next_page = driver.find_element_by_xpath('//a[@class="ui-pager-next"]')
                btn_next_page.click()
                time.sleep(5)
                save_comment()
        except Exception as e:
            log.error("-------爬到最后一页了------")
            log.error(e)
    except Exception as e:
        log.error("-------爬取失败，系统挂了，无力回天(-.-!!)------")


def save_comment():
    comments = driver.find_elements_by_class_name("comment-con")
    for comment in comments:
        commentContent = comment.text
        log.debug(commentContent)
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Sql.insert_new_comment(comment_type, commentContent,create_time)


def gun():
    # 将滚动条移动到页面的底部
    js = "var q=document.documentElement.scrollTop=2000"
    driver.execute_script(js)
    time.sleep(3)


def closeAD():
    btn_clsoe_ad = driver.find_element_by_xpath('//*[@id="toolbar-qrcode"]/span')
    btn_clsoe_ad.click()


# 清空数据表
Sql.delete_all_comment()
py_jd_product_detail()
py_jd_comment()
driver.close()