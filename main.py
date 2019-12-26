# -*- coding: utf-8 -*-
import time, os
import logging, random
import itchat, config, data
from config import option
from crawler.zhidexiang import ZhiDeXiangCrawler
from mail import Mail


def main_handler():
    last_result = set()
    result = set()
    try:
        # 创建临时目录
        if not os.path.exists(config.BASE_TMP_DIR):
            os.makedirs(config.BASE_TMP_DIR)
        zhidexiang_crawler = ZhiDeXiangCrawler()
        last_result = data.get_tmp_result()
        for post_detail in zhidexiang_crawler.crawl():
            result.add(post_detail.id)
            if post_detail.id in last_result:
                continue
            send_msg(post_detail, config.MSG_PUSH_CONFIG)
    except Exception as ex:
        logging.exception('任务错误: %s' % str(ex))
    finally:
        data.save_tmp_result(result, last_result)

'''
itchat发送消息
'''
def send_msg(post_detail, msg_push_config):
    #msg_push_config为非实例配置
    files = []
    msg = post_detail.format_msg(config.ENABLE_POST_URL, config.ENABLE_SHOW_SOURCE)
    logging.info('PostDetail -> %s' % str(post_detail))
    if not config.ENABLE_PUSH_MSG:
        logging.info('推送开关已关闭，消息未推送 -> \n')
    else:
        for chatroom in msg_push_config:
            if not chatroom.enable_chatroom_push(post_detail.source):
                logging.info(chatroom.nick_name + '：已关闭【' + post_detail.source + '】推送消息！')
                continue
            if not chatroom.enable_push(post_detail):
                logging.info('当前【%s】不推送此消息！' % (chatroom.nick_name))
                continue
            if chatroom.user_name == '':
                logging.info('【%s】无法推送，找不到标志符，请保存群聊到通讯录后重新登录！' % (chatroom.nick_name))
                continue
        itchat.send_msg(msg, toUserName=chatroom.user_name)
        # 发送图片
        if chatroom.pic_enable and len(post_detail.images) != 0:
            # 保证图片只下载一次
            if len(files) == 0:
                if len(post_detail.images) > config.ALLOW_MAX_IMAGE_COUNT:
                    files.append(post_detail.merge_image(config.BASE_TMP_DIR))
                else:
                    files = post_detail.download_image(config.BASE_TMP_DIR)
            for path in files:
                itchat.send_image(path, toUserName=chatroom.user_name)
                time.sleep(2)
        time.sleep(random.randint(2, 5))
    if not config.ENABLE_MAIL:
        logging.info('邮箱开关已关闭，消息未推送 -> \n')
        return
    logging.info('准备推送 -> \n%s' % msg)
    sender = Mail(config.MSG_MAIL_CONFIG[0].mail_host,config.MSG_MAIL_CONFIG[0].mail_username,config.MSG_MAIL_CONFIG[0].mail_password)
    sender.send(msg,'rootphantomy@hotmail.com')
    
    # 删除临时文件
    for path in files:
        if os.path.exists(path):
            os.remove(path)

def select():
    pass

if __name__ == '__main__':
    # 日志格式设定
    logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s: %(message)s')
    logging.info('加载应用配置信息')
    option.auto_app_config()
    # 定时循环
    while True:
        main_handler()
        logging.info('等待时间/s：%s' % config.TASK_INTERVAL)
        time.sleep(config.TASK_INTERVAL)
        # 重新加载配置
        option.auto_app_config()
    # 退出登录
    itchat.logout()
