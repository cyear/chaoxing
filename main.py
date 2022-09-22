import random, time, sys
import argparse
import utils.functions as ft
from api.chaoxing import Chaoxing

work(chaoxingAPI):
    #print(chaoxingAPI.selected_course)
    re_login_try = 0
    # done = list(ft.load_finished(chaoxingAPI.usernm))
    logger.info("已选课程："+str(chaoxingAPI.selected_course['content']['course']['data'][0]['name']))
    logger.info("开始获取所有章节")
    chaoxingAPI.get_selected_course_data()  # 读取所有章节
    mission_num = len(chaoxingAPI.missions)
    mission_index = 0
    while mission_index < mission_num:
        mission = chaoxingAPI.missions[mission_index]
        mission_index += 1
        logger.debug("开始读取章节信息")
        knowledge_raw = chaoxingAPI.get_mission(mission['id'], chaoxingAPI.selected_course['key'])  # 读取章节信息
        if "data" not in knowledge_raw and "error" in knowledge_raw:
            logger.debug("---knowledge_raw info begin---")
            logger.debug(knowledge_raw)
            logger.debug("---knowledge_raw info end---")
            if re_login_try < 2:
                logger.warn("章节数据错误,可能是课程存在验证码,正在尝试重新登录")
                chaoxingAPI.re_init_login()
                mission_index -= 1
                re_login_try += 1
                continue
            else:
                logger.error("章节数据错误,可能是课程存在验证码,重新登录尝试无效")
                input("请截图并携带日志提交Issue反馈")
        re_login_try = 0
        tabs = len(knowledge_raw['data'][0]['card']['data'])
        for tab_index in range(tabs):
            #print("开始读取标签信息")
            knowledge_card_text = chaoxingAPI.get_knowledge(
                chaoxingAPI.selected_course['key'],
                chaoxingAPI.selected_course['content']['course']['data'][0]['id'],
                mission["id"],
                tab_index
            )
            attachments: dict = chaoxingAPI.get_attachments(knowledge_card_text)
            if not attachments:
                continue
            if not attachments.get('attachments'):
                continue
            print(f'\n当前章节：{mission["label"]}:{mission["name"]}')
            for attachment in attachments['attachments']:
                if attachment.get('type') != 'video': # 非视频任务跳过
                    #print(attachment)
                    if attachment.get('type') != 'document':
                        print("pass video and document")
                        continue
                    if not chaoxingAPI.filebeta:
                        continue
                    # document (.pptx...)支持
                    jobid = None
                    if "jobid" in attachments:
                        jobid = attachments["jobid"]
                    else: 
                        if "jobid" in attachment:
                            jobid = attachment["jobid"]
                        else:
                            if "jobid" in attachment['property']:
                                jobid = attachment['property']['jobid']
                            else:
                                if "'_jobid'" in attachment['property']:
                                    jobid = attachment['property']['_jobid']
                    if not jobid:
                        print("not jobid pass")
                        continue
                    video_info = chaoxingAPI.get_d_token(
                        attachment['property']['objectid'],
                        attachments['defaults']['fid']
                    )
                    #print(video_info)
                    print(f"\n当前文件：{attachment['property']['name']}")
                    #print(mission)
                    #print(attachment)
                    #if mission['id'] == 390379027:
                    chaoxingAPI.document(
                        chaoxingAPI.uid,
                        chaoxingAPI.selected_course['key'],
                        attachment['jtoken'],
                        chaoxingAPI.selected_course['content']['course']['data'][0]['id'],
                        mission["id"],
                        jobid
                    )
                    continue
                print(f"\n当前视频：{attachment['property']['name']}")
                if attachment.get('isPassed'):
                    print("当前视频任务已完成")
                    ft.show_progress(attachment['property']['name'], 1, 1)
                    time.sleep(1)
                    continue
                try:
                    video_info = chaoxingAPI.get_d_token(
                        attachment['objectid'],
                        attachments['defaults']['fid']
                    )
                except:
                    #print(attachment)
                    logger.warn("出现了一个可修复问题")
                    try:
                        video_info = chaoxingAPI.get_d_token(
                            attachment['property']['objectid'],
                            attachments['defaults']['fid']
                        )
                    except:
                        logger.error(attachments)
                        logger.error("致命问题: code 112-107")
                if not video_info:
                    continue
                jobid = None
                if "jobid" in attachments:
                    jobid = attachments["jobid"]
                else: 
                    if "jobid" in attachment:
                        jobid = attachment["jobid"]
                    else:
                        if "jobid" in attachment['property']:
                            jobid = attachment['property']['jobid']
                        else:
                            if "'_jobid'" in attachment['property']:
                                jobid = attachment['property']['_jobid']
                if not jobid:
                    print("未找到jobid，已跳过当前任务点")
                    continue
                chaoxingAPI.pass_video(
                    video_info['duration'],
                    attachments['defaults']['cpi'],
                    video_info['dtoken'],
                    attachment['otherInfo'],
                    chaoxingAPI.selected_course['key'],
                    attachment['jobid'],
                    video_info['objectid'],
                    chaoxingAPI.uid,
                    attachment['property']['name'],
                    chaoxingAPI.speed,
                    chaoxingAPI.get_current_ms
                )
                ft.pause(8, 13)
                # chaoxing.speed = set_speed  # 预防ERR


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cyear-chaoxing')  # 命令行传参
    parser.add_argument('-debug','--debug', action='store_true', help='Enable debug output in console')
    parser.add_argument('--no-log', action='store_false', help='Disable Console log')
    parser.add_argument('--no-logo', action='store_false', help='Disable Boot logo')
    parser.add_argument('--no-sec', action='store_false', help='Disable all security feature')
    parser.add_argument('-v','--version', action='store_true', help='version')
    args = parser.parse_args()  # 定义专用参数变量
    debug = args.debug  # debug输出  Default:False
    show = args.no_log # 显示控制台log Default:True
    logo = args.no_logo # 展示启动LOGO Default:True
    hideinfo = args.no_sec  # 启用隐私保护 Default:True
    v = args.version
    if v:
        print("\n------v0.1.2209.1.Beta.2------\n")
        input("Enter to exit the program> > > ")
        sys.exit()
    try:
        #if 1:
        ft.init_all_path(["saves", "logs"])  # 检查文件夹
        logger = ft.Logger("main",debug,show)  # 初始化日志类
        if debug:
            logger.debug("已启用debug输出")
        if not show:
            logger.debug("已关闭控制台日志")
        ft.title_show(logo)     # 显示头
        if not logo:
            logger.debug("已关闭启动LOGO")
        logger.info("正在读取本地用户数据...")
        usernm, secname, passwd = ft.load_users(hideinfo)    # 获取账号密码
        chaoxing = Chaoxing(usernm, passwd, debug, show)     # 实例化超星API
        chaoxing.init_explorer()    # 实例化浏览Explorer
        logger.info("登陆中")
        if chaoxing.login():    # 登录
            logger.info("已登录账户：" +secname)
            logger.info("正在读取所有课程")
            if chaoxing.get_all_courses():  # 读取所有的课程
                logger.info("进行选课")
                if chaoxing.select_course():    # 选择要学习的课程
                    if chaoxing.filebeta:
                        logger.warn("您已打开 Beta 版本功能（具体查看README.md）")
                    speed_input = input("默认倍速： 1 倍速 \n——因使用不合理的多倍速造成的一切风险与开发者无关——\n请输入学习倍速(倍数为整数,默认1倍速)：")
                    if speed_input:
                        chaoxing.speed = int(speed_input)
                    else:
                        chaoxing.speed = 1
                    logger.debug("当前设置速率："+str(chaoxing.speed)+"倍速")
                    logger.info("开始学习")
                    do_work(chaoxing)   # 开始学习
        input("任务已结束，请点击回车键退出程序")
    except Exception as e:
        print(f"出现报错{e.__class__}")
        print(f"错误文件名：{e.__traceback__.tb_frame.f_globals['__file__']}")
        print(f"错误行数：{e.__traceback__.tb_lineno}")
        print(f"错误原因:{e}")
        input("请截图提交至Github或QQ供作者修改代码\n点击回车键退出程序")