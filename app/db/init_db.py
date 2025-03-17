import pymysql
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 导入项目配置
from src.core.config import settings

# 数据库连接配置
DB_CONFIG = {
    'host': settings.DB_HOST,
    'port': settings.DB_PORT,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'charset': 'utf8mb4'
}

def init_database():
    """初始化数据库，执行DDL脚本"""
    # 连接到MySQL服务器（不指定数据库）
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        charset=DB_CONFIG['charset']
    )
    
    try:
        with conn.cursor() as cursor:
            # 删除已存在的数据库
            print('删除旧数据库...')
            cursor.execute(f'DROP DATABASE IF EXISTS {settings.DB_NAME};')
            
            # 创建新数据库
            print('创建新数据库...')
            cursor.execute(f'CREATE DATABASE {settings.DB_NAME};')
            
            # 切换到新数据库
            cursor.execute(f'USE {settings.DB_NAME};')
            
            # 读取DDL文件
            print('执行DDL脚本...')
            ddl_path = os.path.join(os.path.dirname(__file__), 'new_ddl.sql')
            with open(ddl_path, 'r', encoding='utf-8') as f:
                ddl_script = f.read()
            
            # 分割SQL语句并执行
            statements = ddl_script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:  # 跳过空语句
                    cursor.execute(statement)
            
            conn.commit()
            print('数据库初始化完成！')
    except Exception as e:
        print(f'初始化数据库时出错: {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    init_database() 