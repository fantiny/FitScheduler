# 集成测试结果

测试时间: 2025-03-17 13:18:48

## 总结

* 总步骤数: 13
* 成功步骤: 12
* 失败步骤: 1

* 服务器状态: ✅ 运行中

## 详细步骤

### 步骤 1: 用户注册 - ✅ 成功

详情:
```
成功创建用户 testuser_89dc2b_20250317131825，用户ID: 10
```


```json
{
  "email": "user_89dc2b_20250317131825@example.com",
  "username": "testuser_89dc2b_20250317131825",
  "phone": "1234567890",
  "is_active": true,
  "membership_rank": "STANDARD",
  "user_id": 10,
  "profile_image": null,
  "booking_count": 0,
  "created_at": "2025-03-17T13:18:29",
  "updated_at": "2025-03-17T13:18:29"
}
```

### 步骤 2: 用户登录 - ✅ 成功

详情:
```
成功获取访问令牌
```


```json
{
  "token_type": "bearer"
}
```

### 步骤 3: 获取用户信息 - ✅ 成功

详情:
```
成功获取用户 testuser_89dc2b_20250317131825 的信息
```


```json
{
  "email": "user_89dc2b_20250317131825@example.com",
  "username": "testuser_89dc2b_20250317131825",
  "phone": "1234567890",
  "is_active": true,
  "membership_rank": "STANDARD",
  "user_id": 10,
  "profile_image": null,
  "booking_count": 0,
  "created_at": "2025-03-17T13:18:29",
  "updated_at": "2025-03-17T13:18:29"
}
```

### 步骤 4: 获取场地列表 - ✅ 成功

详情:
```
成功获取 8 个场地
```


```json
{
  "count": 8
}
```

### 步骤 5: 选择场地 - ✅ 成功

详情:
```
选择场地ID: 1, 名称: Test Venue
```


```json
{
  "venue_name": "Test Venue",
  "address": "123 Test Street",
  "access_info": "Parking available",
  "description": "A test venue for API testing",
  "thumbnail_url": "https://example.com/venue.jpg",
  "venue_id": 1,
  "rating": "0.00",
  "rating_count": 0,
  "created_at": "2025-03-17T01:56:56",
  "updated_at": "2025-03-17T01:56:56",
  "tags": [],
  "images": []
}
```

### 步骤 6: 获取教练列表 - ✅ 成功

详情:
```
成功获取 8 个教练
```


```json
{
  "count": 8
}
```

### 步骤 7: 选择教练 - ✅ 成功

详情:
```
选择教练ID: 1, 名称: Test Coach
```


```json
{
  "name": "Test Coach",
  "email": "coach@example.com",
  "phone": "9876543210",
  "bio": "Experienced coach for testing",
  "specialization": "Tennis",
  "hourly_rate": "50.00",
  "is_active": true,
  "coach_id": 1,
  "profile_image": null,
  "rating": 0.0,
  "review_count": 0,
  "created_at": "2025-03-17T01:57:01",
  "updated_at": "2025-03-17T01:57:01",
  "venues": [],
  "lessons": [],
  "availabilities": []
}
```

### 步骤 8: 获取课程类型列表 - ❌ 失败

详情:
```
请求异常: Expecting value: line 1 column 1 (char 0)
```

### 步骤 9: 选择课程类型 - ✅ 成功

详情:
```
请求异常，但数据库中存在ID=1的课程类型，将使用该课程类型
```


```json
{
  "lesson_type_id": 1,
  "type_name": "测试课程类型"
}
```

### 步骤 10: 创建预约 - ✅ 成功

详情:
```
成功创建预约，预约ID: 7
```


```json
{
  "coach_id": 1,
  "venue_id": 1,
  "lesson_type_id": 1,
  "booking_date": "2025-03-18",
  "start_time": "14:00:00",
  "end_time": "15:00:00",
  "lesson_price": "50.00",
  "facility_fee": "10.00",
  "service_fee": "5.00",
  "total_price": "65.00",
  "notes": "集成测试预约 89dc2b",
  "booking_id": 7,
  "booking_reference": "BK20250317A3B7C1",
  "status": "PENDING",
  "payment_method_id": null,
  "created_at": "2025-03-17T13:18:42",
  "updated_at": "2025-03-17T13:18:42"
}
```

### 步骤 11: 验证预约详情 - ✅ 成功

详情:
```
成功获取预约详情，确认预约已创建
```


```json
{
  "coach_id": 1,
  "venue_id": 1,
  "lesson_type_id": 1,
  "booking_date": "2025-03-18",
  "start_time": "14:00:00",
  "end_time": "15:00:00",
  "lesson_price": "50.00",
  "facility_fee": "10.00",
  "service_fee": "5.00",
  "total_price": "65.00",
  "notes": "集成测试预约 89dc2b",
  "booking_id": 7,
  "booking_reference": "BK20250317A3B7C1",
  "status": "PENDING",
  "payment_method_id": null,
  "created_at": "2025-03-17T13:18:42",
  "updated_at": "2025-03-17T13:18:42"
}
```

### 步骤 12: 验证预约列表 - ✅ 成功

详情:
```
预约ID: 7 在用户预约列表中找到
```


```json
{
  "coach_id": 1,
  "venue_id": 1,
  "lesson_type_id": 1,
  "booking_date": "2025-03-18",
  "start_time": "14:00:00",
  "end_time": "15:00:00",
  "lesson_price": "50.00",
  "facility_fee": "10.00",
  "service_fee": "5.00",
  "total_price": "65.00",
  "notes": "集成测试预约 89dc2b",
  "booking_id": 7,
  "booking_reference": "BK20250317A3B7C1",
  "status": "PENDING",
  "payment_method_id": null,
  "created_at": "2025-03-17T13:18:42",
  "updated_at": "2025-03-17T13:18:42"
}
```

### 步骤 13: 获取预约详情 - ✅ 成功

详情:
```
成功获取预约ID: 7 的详细信息
```


```json
{
  "coach_id": 1,
  "venue_id": 1,
  "lesson_type_id": 1,
  "booking_date": "2025-03-18",
  "start_time": "14:00:00",
  "end_time": "15:00:00",
  "lesson_price": "50.00",
  "facility_fee": "10.00",
  "service_fee": "5.00",
  "total_price": "65.00",
  "notes": "集成测试预约 89dc2b",
  "booking_id": 7,
  "booking_reference": "BK20250317A3B7C1",
  "status": "PENDING",
  "payment_method_id": null,
  "created_at": "2025-03-17T13:18:42",
  "updated_at": "2025-03-17T13:18:42"
}
```

