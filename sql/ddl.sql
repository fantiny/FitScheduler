-- 完整的数据库创建脚本 (最终版本)

-- 用户表 (统一用户和教练)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    profile_image VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'USER' COMMENT 'USER, COACH, ADMIN',
    -- 用户特有字段
    membership_rank VARCHAR(20) DEFAULT 'STANDARD',
    booking_count INT DEFAULT 0,
    -- 教练特有字段
    bio TEXT,
    specialization VARCHAR(100),
    hourly_rate DECIMAL(10,2),
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 支付方式表 (支持多种支付方式)
CREATE TABLE payment_methods (
    payment_method_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    payment_type ENUM('CREDIT_CARD', 'CASH', 'BANK_TRANSFER', 'ONLINE_PAYMENT') NOT NULL,
    -- 信用卡特有字段
    card_number VARCHAR(16),
    card_type VARCHAR(50),
    expiry_month INT,
    expiry_year INT,
    -- 通用字段
    payment_details VARCHAR(255),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 场地表
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    access_info VARCHAR(255),
    description TEXT,
    thumbnail_url VARCHAR(255),
    rating DECIMAL(3,2) DEFAULT 0,
    rating_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 场地设施标签表
CREATE TABLE venue_tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_id INT NOT NULL,
    tag_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE
);

-- 场地图片表
CREATE TABLE venue_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE
);

-- 教练所在场地关联表
CREATE TABLE coach_venues (
    coach_venue_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '教练用户ID',
    venue_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE,
    UNIQUE (user_id, venue_id)
);

-- 课程类型表
CREATE TABLE lesson_types (
    lesson_type_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    duration_minutes INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 教练提供的课程表
CREATE TABLE coach_lessons (
    coach_lesson_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '教练用户ID',
    lesson_type_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_type_id) REFERENCES lesson_types(lesson_type_id) ON DELETE CASCADE,
    UNIQUE (user_id, lesson_type_id)
);

-- 教练可用时间表
CREATE TABLE coach_availability (
    availability_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '教练用户ID',
    venue_id INT NOT NULL,
    day_of_week INT NOT NULL COMMENT '1=Monday, 7=Sunday',
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE
);

-- 预约表
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_reference VARCHAR(20) NOT NULL UNIQUE,
    user_id INT NOT NULL COMMENT '学员用户ID',
    coach_id INT NOT NULL COMMENT '教练用户ID',
    venue_id INT NOT NULL,
    lesson_type_id INT NOT NULL,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING, CONFIRMED, COMPLETED, CANCELLED, NO_SHOW',
    lesson_price DECIMAL(10,2) NOT NULL,
    facility_fee DECIMAL(10,2) DEFAULT 0,
    service_fee DECIMAL(10,2) DEFAULT 0,
    total_price DECIMAL(10,2) NOT NULL,
    payment_method_id INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_type_id) REFERENCES lesson_types(lesson_type_id) ON DELETE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id) ON DELETE SET NULL
);

-- 评价表
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    user_id INT NOT NULL COMMENT '学员用户ID',
    coach_id INT NOT NULL COMMENT '教练用户ID',
    score DECIMAL(3,2) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE (booking_id)
);

-- 收藏表
CREATE TABLE favorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    coach_id INT,
    venue_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE,
    CHECK (coach_id IS NOT NULL OR venue_id IS NOT NULL)
);

-- 通知表
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
); 