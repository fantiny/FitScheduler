#!/usr/bin/env python
"""
直接向数据库插入课程类型的脚本
"""
import pymysql
import sys
import traceback
from datetime import datetime
from decimal import Decimal

# 数据库连接信息
DB_CONFIG = {
    'host': 'localhost',
    'user': 'fantiny',
    'password': 'MySqL_R00t!2023#S3cur1ty',
    'database': 'yoyaku',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def connect_to_db():
    """连接到数据库"""
    try:
        print("尝试连接到数据库...")
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        return connection
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def create_lesson_type(connection):
    """创建课程类型"""
    try:
        print("尝试创建课程类型...")
        with connection.cursor() as cursor:
            # 检查是否已存在
            print("检查课程类型是否已存在...")
            cursor.execute("SELECT COUNT(*) as count FROM lesson_types WHERE name = %s", ("测试课程类型",))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                print("✅ 课程类型'测试课程类型'已存在，无需创建")
                
                # 获取已存在的课程类型ID
                cursor.execute("SELECT lesson_type_id FROM lesson_types WHERE name = %s", ("测试课程类型",))
                lesson_type = cursor.fetchone()
                return lesson_type['lesson_type_id'] if lesson_type else None
            
            # 创建课程类型
            print("创建新的课程类型...")
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = """
            INSERT INTO lesson_types 
            (name, description, base_price, duration_minutes, is_active, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                "测试课程类型",
                "用于测试的课程类型",
                Decimal('50.00'),
                60,
                True,
                now,
                now
            ))
            connection.commit()
            print("SQL执行成功，已提交事务")
            
            # 获取插入的ID
            print("获取插入的课程类型ID...")
            cursor.execute("SELECT lesson_type_id FROM lesson_types WHERE name = %s", ("测试课程类型",))
            lesson_type = cursor.fetchone()
            lesson_type_id = lesson_type['lesson_type_id'] if lesson_type else None
            
            print(f"✅ 成功创建课程类型，ID: {lesson_type_id}")
            return lesson_type_id
    except Exception as e:
        print(f"❌ 创建课程类型失败: {str(e)}")
        traceback.print_exc()
        connection.rollback()
        return None

def main():
    """主函数"""
    print(f"=== 课程类型创建工具 ===")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    # 连接数据库
    connection = connect_to_db()
    
    try:
        # 创建课程类型
        lesson_type_id = create_lesson_type(connection)
        
        if lesson_type_id:
            print(f"课程类型创建成功，可以在集成测试中使用lesson_type_id={lesson_type_id}")
        else:
            print("课程类型创建失败，请检查错误信息")
    
    except Exception as e:
        print(f"执行过程中出错: {str(e)}")
        traceback.print_exc()
    finally:
        connection.close()
        print("-" * 40)
        print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 