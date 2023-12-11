from flask import jsonify, request
import hashlib
import datetime
import hashlib
from functools import wraps
import json
import cx_Oracle
from log import save_log


# Thiết lập thông tin kết nối với cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('118.69.35.119', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

# Định nghĩa một endpoint để login và sinh ra token mới
def login():
    user_name = request.args.get('user')
    password = request.args.get('password')

    # Kiểm tra xem thông tin đăng nhập có hợp lệ không
    if not is_valid_login(user_name, password):
        return jsonify(error='Đăng nhập không hợp lệ'), 401

    # Sinh ra token mới
    token = generate_token(user_name, password)

    # Lưu token vào cơ sở dữ liệu
    save_token(token, user_name, password)

    return jsonify(token=token)

# Hàm kiểm tra tính hợp lệ của thông tin đăng nhập (giả lập)
def is_valid_login(user_name, password):
    # TODO: Thực hiện kiểm tra tính hợp lệ của thông tin đăng nhập thực tế
    # Kiểm tra trong cơ sở dữ liệu, xác thực, v.v.
    if user_name == 'admin' and password == 'hhm@1997':
        return True
    elif user_name == 'HTXLH' and password == '123456':
        return True
    elif user_name == 'HTXTH' and password == '123456':
        return True
    return False

def generate_token(user_name, password):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = time.strftime('%H:%M:%S')
    token_string = f'hhm1997{user_name}{password}{current_date}{current_time}'
    hashed_token = hashlib.sha256(token_string.encode()).hexdigest()
    return hashed_token

# Hàm lưu token vào cơ sở dữ liệu
def save_token(token, user_name, password):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    expire_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    expire_date = expire_time.strftime('%Y-%m-%d')
    expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')

    select_query = "SELECT token FROM Tokens WHERE user_name = :user_name AND password = :password"
    cursor = conn.cursor()
    cursor.execute(select_query, user_name=user_name, password=password)
    existing_token = cursor.fetchone()

    if existing_token:
        update_query = "UPDATE Tokens SET token = :token, login_date = TO_DATE(:login_date, 'YYYY-MM-DD'), expire_date = TO_DATE(:expire_date, 'YYYY-MM-DD'), expire_time = TO_TIMESTAMP(:expire_time, 'YYYY-MM-DD HH24:MI:SS') WHERE user_name = :user_name AND password = :password"
        cursor.execute(update_query, token=token, login_date=current_date, expire_date=expire_date, expire_time=expire_time, user_name=user_name, password=password)
    else:
        insert_query = "INSERT INTO Tokens (user_name, password, token, login_date, expire_date, expire_time) VALUES (:user_name, :password, :token, TO_DATE(:login_date, 'YYYY-MM-DD'), TO_DATE(:expire_date, 'YYYY-MM-DD'), TO_TIMESTAMP(:expire_time, 'YYYY-MM-DD HH24:MI:SS'))"
        cursor.execute(insert_query, user_name=user_name, password=password, token=token, login_date=current_date, expire_date=expire_date, expire_time=expire_time)
    conn.commit()
    cursor.close()

# Hàm kiểm tra tính hợp lệ của token
def is_valid_token(token):
    expire_time = get_token_expire_time(token)
    if expire_time:
        current_time = datetime.datetime.now()
        if expire_time > current_time:
            return True
    return False

# Hàm decorator kiểm tra tính hợp lệ của token
def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not is_valid_token(token):
            return jsonify(error='Token không hợp lệ hoặc đã hết hạn'), 401

        return f(*args, **kwargs)

    return decorated_function

def get_token_expire_time(token):
    select_query = "SELECT expire_time FROM Tokens WHERE token = :token"
    cursor = conn.cursor()
    cursor.execute(select_query, token=token)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None
