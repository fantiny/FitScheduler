#!/usr/bin/env python
"""
数据库查询工具：显示测试过程中创建的数据
"""
import pymysql
import pandas as pd
from tabulate import tabulate
import sys
from datetime import datetime
import traceback

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
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        return connection
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        sys.exit(1)

def execute_query(connection, query, params=None):
    """执行查询"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ 查询执行失败: {str(e)}")
        return []

def show_table_data(connection, table_name, limit=10, where_clause=None):
    """显示表数据"""
    query = f"SELECT * FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += f" LIMIT {limit}"
    
    results = execute_query(connection, query)
    
    if not results:
        print(f"\n== {table_name.upper()} 表中没有数据 ==\n")
        return
    
    # 将结果转换为Pandas DataFrame以便于展示
    df = pd.DataFrame(results)
    print(f"\n== {table_name.upper()} 表数据 ==")
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    print(f"总记录数: {len(results)}\n")
    return df

def show_users(connection):
    """显示用户数据"""
    return show_table_data(connection, "users")

def show_lesson_types(connection):
    """显示课程类型数据"""
    return show_table_data(connection, "lesson_types")

def show_coaches(connection):
    """显示教练数据"""
    return show_table_data(connection, "coaches")

def show_venues(connection):
    """显示场地数据"""
    return show_table_data(connection, "venues")

def show_bookings(connection):
    """显示预约数据"""
    bookings = show_table_data(connection, "bookings")
    if bookings is not None and not bookings.empty:
        # 查询预约相关的用户和教练信息
        for _, booking in bookings.iterrows():
            user_id = booking.get('user_id')
            coach_id = booking.get('coach_id')
            venue_id = booking.get('venue_id')
            lesson_type_id = booking.get('lesson_type_id')
            booking_id = booking.get('booking_id')
            
            print(f"\n== 预约 #{booking_id} 详细信息 ==")
            
            # 查询用户信息
            user_data = execute_query(connection, "SELECT username, email FROM users WHERE user_id = %s", (user_id,))
            if user_data:
                user = user_data[0]
                print(f"用户: {user['username']} ({user['email']})")
            
            # 查询教练信息
            coach_data = execute_query(connection, "SELECT name, email FROM coaches WHERE coach_id = %s", (coach_id,))
            if coach_data:
                coach = coach_data[0]
                print(f"教练: {coach['name']} ({coach['email']})")
            
            # 查询场地信息
            venue_data = execute_query(connection, "SELECT venue_name, address FROM venues WHERE venue_id = %s", (venue_id,))
            if venue_data:
                venue = venue_data[0]
                print(f"场地: {venue['venue_name']} ({venue['address']})")
            
            # 查询课程类型信息
            lesson_type_data = execute_query(connection, "SELECT name, description, base_price FROM lesson_types WHERE lesson_type_id = %s", (lesson_type_id,))
            if lesson_type_data:
                lesson_type = lesson_type_data[0]
                print(f"课程类型: {lesson_type['name']} (基础价格: {lesson_type['base_price']})")
            
            # 显示预约详情
            print(f"预约日期: {booking.get('booking_date')}")
            print(f"时间: {booking.get('start_time')} - {booking.get('end_time')}")
            print(f"价格: {booking.get('total_price')} (课程: {booking.get('lesson_price')}, 场地: {booking.get('facility_fee')}, 服务费: {booking.get('service_fee')})")
            print(f"状态: {booking.get('status')}")
            print(f"预约号: {booking.get('booking_reference')}")
            print(f"备注: {booking.get('notes')}")
            print(f"创建时间: {booking.get('created_at')}")

def show_test_users(connection):
    """显示测试用户数据"""
    return show_table_data(connection, "users", where_clause="username LIKE 'testuser_%'")

def show_integration_test_data(connection):
    """专门查询集成测试创建的数据"""
    print("\n" + "=" * 40)
    print("== 集成测试创建的数据 ==")
    print("=" * 40)
    
    # 查询集成测试创建的用户
    test_users = execute_query(connection, "SELECT * FROM users WHERE username LIKE 'testuser_%' ORDER BY user_id")
    if test_users:
        df_users = pd.DataFrame(test_users)
        print("\n集成测试用户:")
        print(tabulate(df_users[['user_id', 'username', 'email', 'created_at']], headers='keys', tablefmt='pretty', showindex=False))
        
        # 检查这些用户是否有预约
        for user in test_users:
            user_id = user['user_id']
            bookings = execute_query(connection, "SELECT * FROM bookings WHERE user_id = %s", (user_id,))
            if bookings:
                print(f"\n用户 {user['username']} (ID: {user_id}) 的预约:")
                
                # 显示预约详情
                for booking in bookings:
                    booking_id = booking['booking_id']
                    coach_id = booking['coach_id']
                    venue_id = booking['venue_id']
                    lesson_type_id = booking['lesson_type_id']
                    
                    # 查询教练信息
                    coach_data = execute_query(connection, "SELECT name FROM coaches WHERE coach_id = %s", (coach_id,))
                    coach_name = coach_data[0]['name'] if coach_data else "未知"
                    
                    # 查询场地信息
                    venue_data = execute_query(connection, "SELECT venue_name FROM venues WHERE venue_id = %s", (venue_id,))
                    venue_name = venue_data[0]['venue_name'] if venue_data else "未知"
                    
                    # 查询课程类型信息
                    lesson_type_data = execute_query(connection, "SELECT name FROM lesson_types WHERE lesson_type_id = %s", (lesson_type_id,))
                    lesson_type_name = lesson_type_data[0]['name'] if lesson_type_data else "未知"
                    
                    print(f"\n预约 #{booking_id} 详细信息:")
                    print(f"  预约号: {booking['booking_reference']}")
                    print(f"  用户: {user['username']}")
                    print(f"  教练: {coach_name}")
                    print(f"  场地: {venue_name}")
                    print(f"  课程类型: {lesson_type_name}")
                    print(f"  日期: {booking['booking_date']}")
                    print(f"  时间: {booking['start_time']} - {booking['end_time']}")
                    print(f"  价格: {booking['total_price']} (课程: {booking['lesson_price']}, 场地: {booking['facility_fee']}, 服务费: {booking['service_fee']})")
                    print(f"  状态: {booking['status']}")
                    print(f"  备注: {booking['notes']}")
                    print(f"  创建时间: {booking['created_at']}")
            else:
                print(f"\n用户 {user['username']} (ID: {user_id}) 没有预约记录")
    else:
        print("没有找到集成测试创建的用户")
    
    # 查询集成测试创建的课程类型
    test_lesson_types = execute_query(connection, "SELECT * FROM lesson_types WHERE name LIKE '测试课程类型%'")
    if test_lesson_types:
        df_lesson_types = pd.DataFrame(test_lesson_types)
        print("\n集成测试课程类型:")
        print(tabulate(df_lesson_types[['lesson_type_id', 'name', 'description', 'base_price', 'duration_minutes']], headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("\n没有找到集成测试创建的课程类型")

def check_booking_results(connection):
    """分析预约创建是否成功"""
    print("\n== 预约创建分析 ==")
    
    # 检查lesson_types表
    lesson_types = execute_query(connection, "SELECT COUNT(*) as count FROM lesson_types")
    lesson_type_count = lesson_types[0]['count'] if lesson_types else 0
    
    if lesson_type_count == 0:
        print("❌ 没有课程类型记录，预约创建将会失败")
        reason = "数据库中没有lesson_types记录，由于外键约束，创建预约时会失败"
    else:
        print(f"✅ 发现 {lesson_type_count} 个课程类型记录")
        
    # 检查测试用户的预约
    test_users = execute_query(connection, "SELECT user_id FROM users WHERE username LIKE 'testuser_%'")
    if test_users:
        user_ids = [user['user_id'] for user in test_users]
        placeholders = ', '.join(['%s'] * len(user_ids))
        bookings = execute_query(connection, f"SELECT COUNT(*) as count FROM bookings WHERE user_id IN ({placeholders})", tuple(user_ids))
        booking_count = bookings[0]['count'] if bookings else 0
        
        if booking_count > 0:
            print(f"✅ 测试用户成功创建了 {booking_count} 个预约")
        else:
            print("❌ 测试用户没有创建任何预约")
            # 查找失败原因
            if lesson_type_count == 0:
                reason = "由于没有课程类型记录，预约创建失败"
            else:
                reason = "虽然有课程类型记录，但预约创建仍然失败，可能是其他约束或验证问题"
            print(f"   原因: {reason}")
    else:
        print("❓ 没有找到测试用户记录")

def show_table_counts(connection):
    """显示数据库中的表和行数"""
    tables = execute_query(connection, "SHOW TABLES")
    print("数据库中的表:")
    for table in tables:
        table_name = list(table.values())[0]
        count = execute_query(connection, f"SELECT COUNT(*) as count FROM {table_name}")
        row_count = count[0]['count'] if count else 0
        print(f"- {table_name}: {row_count} 行")

def main():
    """主函数"""
    print("=== 数据库查询工具 ===")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    try:
        connection = connect_to_db()
        if connection:
            print("✅ 数据库连接成功\n")
            
            # 显示数据库中的表和行数
            show_table_counts(connection)
            
            # 显示集成测试创建的数据
            show_integration_test_data(connection)
            
            # 关闭连接
            connection.close()
    except Exception as e:
        print(f"❌ 执行过程中出错: {e}")
        traceback.print_exc()
    
    print("\n" + "-" * 40)
    print(f"查询完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 