"""
环境配置项管理
"""

from pathlib import Path
from dynaconf import Dynaconf


# 根目录
ROOT_DIR = Path(__file__).parent

# 加载配置
settings = Dynaconf(
    # 设置环境变量前缀
    # 比如：settings.FOO = "bar" 在环境变量中就是 DEMO_FOO="bar"
    envvar_prefix="DYNACONF",
    # 指定根目录
    base_dir=ROOT_DIR,
    # 通过列表方式加载多个配置文件
    settings_files=["settings.toml", ".secrets.toml"],
    # 加载 .env 文件
    load_dotenv=True,
)


LOGO_STR = """

 ▄▄▄       ▄▄▄▄    ▄▄▄       ███▄    █ ▓█████▄  ▒█████   ███▄    █ 
▒████▄    ▓█████▄ ▒████▄     ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒ ██ ▀█   █ 
▒██  ▀█▄  ▒██▒ ▄██▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▌▒██░  ██▒▓██  ▀█ ██▒
░██▄▄▄▄██ ▒██░█▀  ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░▓██▒  ▐▌██▒
 ▓█   ▓██▒░▓█  ▀█▓ ▓█   ▓██▒▒██░   ▓██░░▒████▓ ░ ████▓▒░▒██░   ▓██░
 ▒▒   ▓▒█░░▒▓███▀▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
  ▒   ▒▒ ░▒░▒   ░   ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░ ░ ░░   ░ ▒░
  ░   ▒    ░    ░   ░   ▒      ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒     ░   ░ ░ 
      ░  ░ ░            ░  ░         ░    ░        ░ ░           ░ 
                ░                       ░                          
"""


if __name__ == '__main__':
    assert settings.MYSQL.HOST == "127.0.0.1"
    assert settings.MYSQL.USERNAME == "root"
    assert settings.MYSQL.DATABASE == "abandon"
