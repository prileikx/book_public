import datetime
SQLALCHEMY_TRACK_MODIFICATIONS=True

#json字符串设置,若为true则无法正常显示中文
JSON_AS_ASCII=False
#数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'book'
USERNAME = 'root'
PASSWORD = 'password'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
#邮件发送设置
MAIL_SERVER='smtp.163.com'
MAIL_PORT=25
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEBUG=True
MAIL_USERNAME='abc@example.com'
MAIL_PASSWORD='password'
MAIL_DEFAULT_SENDER='abc@example.com'
#session
PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=30)
SECRET_KEY='password'
#图片生成设置
font_path='D:/project_developer/book_manage/static/SourceHanSansSC-Normal-2.otf'
img_path='D:/project_developer/book_manage/static/upload/books/img/'