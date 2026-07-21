# MySQL 连接信息（兰园项目）

| 项目 | 值 |
|------|------|
| 主机 | localhost (127.0.0.1) |
| 端口 | 3306 |
| 数据库 | lanyuan |
| 用户名 | lanyuan |
| 密码 | 123456 |

## 命令行连接

```bash
# 方式一：lanyuan 用户
mysql -u lanyuan -p
# 密码: 123456

# 方式二：root 免密
sudo mysql
```

## 常用 SQL

```sql
USE lanyuan;
SHOW TABLES;           -- 查看所有表
SELECT * FROM users;   -- 查用户
SELECT * FROM posts;   -- 查帖子（含 images JSON）
SELECT * FROM comments;
SELECT * FROM likes;

DESCRIBE users;        -- 查看表结构
```

## 后端连接

配置在 `backend/.env`：

```
DATABASE_URL=mysql+aiomysql://lanyuan:lanyuan_dev_pw@localhost/lanyuan?charset=utf8mb4
```

## 切换回 SQLite（开发用）

删掉 `backend/.env` 即可回到 SQLite。
