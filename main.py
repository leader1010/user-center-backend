import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from common.settings.default import DefaultConfig

# 日志
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')  # 生成Formatter
# 文件日志
file_handler = TimedRotatingFileHandler(
    filename='logs/user-center_debug.log', when='midnight',
    backupCount=30)  # 生成handle
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
# 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他的地方
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)


def create_app(config):
    """
    创建Flask应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(config)
    from common.models import db
    db.init_app(app)
    return app


app = create_app(DefaultConfig)

# 注册用户蓝图
from resources.user import user_bp

app.register_blueprint(user_bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
