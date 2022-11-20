# :computer: 超星学习通自动完成任务点(控制台命令)

本项目最终目的开源消灭付费刷课平台

:star: 本人学业繁忙，尽力维护。

## :point_up: 更新通知

202212xx更新:

    # 1.修复音乐任务403

    # 2.添加题库支持

-格式(set.config):
    
    [{
        'name': 'xxx',
        'url': 'xxx',
        'type': 'get/post',
        'data': {'xxx': '{title}'}
    },
    xxx(如上)
    ]

    #{title}为题目提交参数，支持多个题库

20221118更新：

    1.修复章节问题

    2.支持aarch64架构运行

20221116公告：

    # 1.添加音频任务点支持

    # 代码近期准备重构（方便后期扩展维护/学业繁忙已推迟）

20220920 更新(1-Beta.2)：

    1.修复一个分页任务点错误

20220919 更新：

    3.更详细的bug输出，并尝试修复一个非固定的dict（class Exception未修复, 音频任务也会报错，后续修复)

    2.添加完成文档文件任务点功能（Beta）设置self.filebeta=0关闭此功能

    1.针对403无权限问题添加额外的信息输出，添加一次连接错误重试（或许有用）

20220918 更新：

    1.暂时修复获取视频403没有权限的状况

-------------------

## :books: 使用方法

### 源码运行(推荐)
1. 提前准备： Python版本>=3.8
2. `git clone https://github.com/cyear/chaoxing.git` 项目至本地
3. `cd chaoxing`
4. `pip3 install -r requirements.txt`
5. `python3 main.py` 运行程序
6. 可选参数 -debug 开启DEBUG模式 --no-log 不输出日志 --no-logo 隐藏开头项目LOGO --no-sec 关闭隐私保护

实时反馈群聊：

    QQ群：556766602

-------------------

### 使用Docker运行（本项目不支持，下面为原项目教程，具体查看下方github链接）
1. `git clone --depth=1 https://github.com/Samueli924/chaoxing` 获取项目源码
2. `docker-compose run --rm app`, 在交互式终端中运行容器

你可以在终端中使用`ctrl+p+q`来让容器退出交互式终端并在后台运行


原项目地址： https://github.com/Samueli924/chaoxing

## :warning: 免责声明  
- 本代码遵循 [GPL-3.0 License](https://github.com/cyear/chaoxing/blob/main/LICENSE)协议，允许**开源/免费使用和引用/修改/衍生代码的开源/免费使用**，不允许**修改和衍生的代码作为闭源的商业软件发布和销售**，禁止**使用本代码盈利**，以此代码为基础的程序**必须**同样遵守[GPL-3.0 License](https://github.com/cyear/chaoxing/blob/main/LICENSE)协议  
- 本代码仅用于**学习讨论**，禁止**用于盈利**  
- 他人或组织使用本代码进行的任何**违法行为**与本人无关
