# 项目名称: BookShop

## 项目描述
这是一个在线图书商店的项目，旨在为用户提供方便快捷的图书购买体验。

## 功能特点
- 用户注册和登录
- 图书浏览和搜索
- 图书详情展示
- 购物车管理
- 订单生成和支付
- 用户个人信息管理

## 技术栈
- 前端: HTML, CSS, JavaScript
- 后端: Django (5.0.6)
- 数据库: SQLite3

## 运行
1. 克隆项目到本地
2. 进入项目目录
3. 进行数据库迁移: 
    1. `python3.12 manage.py makemigrations`
    2. `python3.12 manage.py migrate`
4. 创建超级用户: `python3.12 manage.py createsuperuser`
5. 启动开发服务器: `python manage.py runserver`

## 注意事项
* 在 `settings.py` 和 `.env` 文件中设置相应的用于密码重置的邮箱。以下是具体步骤：

1. 在项目根目录下创建一个 `.env` 文件。
2. 在 `.env` 文件中添加以下内容，替换为你的实际邮箱配置：
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password    # 授权码
   DEFAULT_FROM_EMAIL=your-email@example.com
   ```
3. 在 `settings.py` 文件中，添加以下配置以读取 `.env` 文件中的邮箱设置：
    ```python
    from decouple import config

    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = config('EMAIL_HOST', default='')
    EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')
    ```

* 在项目根目录下创建一个 media 文件夹用于保存上传的书本图片和用户图片，文件夹目录为：
  ```
  media
    -book_images
    -user_images
  ```

* 在 `shop/static` 下建立images文件夹存放默认头像 `default.jpg`