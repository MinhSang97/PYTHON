import cx_Oracle
from flask import Flask, jsonify, request
import hashlib
import datetime
import hashlib
from functools import wraps
import json
import re
import time
import logging
import os
import signal
import sys


app = Flask(__name__)

# Thiết lập thông tin kết nối với cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('192.168.30.252', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

# Định nghĩa một endpoint để login và sinh ra token mới
@app.route('/login', methods=['GET'])
def login():
    user_name = request.args.get('user')
    password = request.args.get('password')
    
    # Lấy địa chỉ IP
    ip_address = request.remote_addr

    if not is_valid_login(user_name, password):
        return jsonify(error='Đăng nhập không hợp lệ'), 401

    token = generate_token(user_name, password)
    save_token(token, user_name, password, ip_address)
    
    return jsonify(token=token)

# Hàm kiểm tra tính hợp lệ của thông tin đăng nhập (giả lập)
def is_valid_login(user_name, password):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Tokens WHERE user_name = :user_name AND password = :password", user_name=user_name, password=password)
    result = cursor.fetchone()[0]
    cursor.close()

    return result > 0

def generate_token(user_name, password):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = time.strftime('%H')
    token_string = f'hhm1997{user_name}{password}{current_date}{current_time}'
    hashed_token = hashlib.sha256(token_string.encode()).hexdigest()
    return hashed_token

# Hàm lưu token vào cơ sở dữ liệu
def save_token(token, user_name, password, ip_address):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    expire_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    expire_date = expire_time.strftime('%Y-%m-%d')
    expire_time = expire_time.strftime('%Y-%m-%d %H:%M:%S')

    select_query = "SELECT token FROM Tokens WHERE user_name = :user_name AND password = :password"
    cursor = conn.cursor()
    cursor.execute(select_query, user_name=user_name, password=password)
    existing_token = cursor.fetchone()

    if existing_token:
        update_query = "UPDATE Tokens SET token = :token, login_date = TO_DATE(:login_date, 'YYYY-MM-DD'), expire_date = TO_DATE(:expire_date, 'YYYY-MM-DD'), expire_time = TO_TIMESTAMP(:expire_time, 'YYYY-MM-DD HH24:MI:SS'), ip_address = :ip_address WHERE user_name = :user_name AND password = :password"
        cursor.execute(update_query, token=token, login_date=current_date, expire_date=expire_date, expire_time=expire_time, user_name=user_name, password=password, ip_address=ip_address)
    else:
        insert_query = "INSERT INTO Tokens (user_name, password, token, login_date, expire_date, expire_time, ip_address) VALUES (:user_name, :password, :token, TO_DATE(:login_date, 'YYYY-MM-DD'), TO_DATE(:expire_date, 'YYYY-MM-DD'), TO_TIMESTAMP(:expire_time, 'YYYY-MM-DD HH24:MI:SS'), :ip_address)"
        cursor.execute(insert_query, user_name=user_name, password=password, token=token, login_date=current_date, expire_date=expire_date, expire_time=expire_time, ip_address=ip_address)   
    conn.commit()
    cursor.close()

def save_log(token, cong_to, thoi_gian, ip_address):
    current_time = datetime.datetime.now()
    
    insert_query = "INSERT INTO Logs (token, cong_to, thoi_gian, thoi_gian_hien_tai, ip_address) VALUES (:token, :cong_to, :thoi_gian, :thoi_gian_hien_tai, :ip_address)"
    cursor = conn.cursor()
    cursor.execute(insert_query, token=token, cong_to=cong_to, thoi_gian=thoi_gian, thoi_gian_hien_tai=current_time, ip_address=ip_address)
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

#getdata theo to day
def get_data_by_date_range(meter_asset_no, start_date, end_date):
    # meter_asset_no = request.args.get('cong_to')
    # start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')
    # Thực hiện kiểm tra tính hợp lệ của meter_asset_no, start_date và end_date

    # Chuyển đổi định dạng của start_date và end_date (nếu cần)
    start_date = datetime.datetime.strptime(start_date, '%d-%m-%y').strftime('%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%d-%m-%y').strftime('%Y-%m-%d')

    # Truy vấn loại công tơ
    query_meter_model = "SELECT meter_model FROM a_equip_meter WHERE assetno = :meter_asset_no"
    cursor = conn.cursor()
    cursor.execute(query_meter_model, meter_asset_no=meter_asset_no)
    meter_model = cursor.fetchone()

    if meter_model is None:
        return jsonify(error='No công tơ không hợp lệ.'), 404

    meter_model1 = meter_model[0]

    # Xây dựng truy vấn dựa trên meter_model và khoảng thời gian
    if meter_model1 == "HHM11-V1":
        query = '''
                     SElECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
            FROM
            (SELECT DISTINCT  e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto, e.TV,
            e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3,
            g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
            FROM
            (SELECT DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, c.TV,
            FA dn_huucong_giao, FA_T1 dn_huucong_giao_bieu1, FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3,
            FR dn_huucong_nhan, FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
            FROM A_Data_catalogue d
            LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID 
            WHERE d.METER_ASSET_NO = :meter_asset_no
            AND TRUNC(c.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
            AND TRUNC(c.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')) e
            LEFT JOIN BIZ_PUB_DATA_R_ENERGY_D g ON e.Data_ID = g.Data_ID)z
            LEFT join BIZ_PUB_DATA_OTHER_D y
            ON z.Data_ID = y.Data_ID
            and z.nocongto = :meter_asset_no and z.tv = y.tv
            AND TRUNC(y.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
    AND TRUNC(y.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
    
        AND TRUNC(z.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
    AND TRUNC(z.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
        '''
    elif meter_model1 == "HHM31/38":
        query = '''
                        SELECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, 
                            z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
                            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, 
                            z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
                            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
                FROM
                    (SELECT DISTINCT e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto, e.tv, 
                            e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
                            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3, 
                            g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
                            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
                    FROM
                        (SELECT DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, c.tv, 
                                FA dn_huucong_giao, FA_T1 dn_huucong_giao_bieu1, FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3, 
                                FR dn_huucong_nhan, FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
                        FROM A_Data_catalogue d
                        LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID 
                        WHERE d.METER_ASSET_NO = :meter_asset_no
                AND TRUNC(c.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                            AND TRUNC(c.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        ) e
                    LEFT JOIN BIZ_PUB_DATA_R_ENERGY_D g ON e.Data_ID = g.Data_ID 
                    WHERE e.METER_ASSET_NO = :meter_asset_no
                        AND g.TV > TO_DATE(:start_date, 'yyyy-mm-dd') 
                        AND g.TV < TO_DATE(:end_date, 'yyyy-mm-dd')
                    ) z
                LEFT JOIN BIZ_PUB_DATA_OTHER_D y
                    ON z.Data_ID = y.Data_ID and z.tv = y.tv
                    WHERE z.nocongto = :meter_asset_no
                    AND TRUNC(y.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(y.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        AND TRUNC(z.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(z.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
        '''
    elif meter_model1 == "HHM31":
        query = '''
                        SELECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, 
                            z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
                            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, 
                            z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
                            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
                FROM
                    (SELECT DISTINCT e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto, e.tv, 
                            e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
                            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3, 
                            g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
                            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
                    FROM
                        (SELECT DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, c.tv, 
                                FA dn_huucong_giao, FA_T1 dn_huucong_giao_bieu1, FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3, 
                                FR dn_huucong_nhan, FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
                        FROM A_Data_catalogue d
                        LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID 
                        WHERE d.METER_ASSET_NO = :meter_asset_no
                AND TRUNC(c.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                            AND TRUNC(c.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        ) e
                    LEFT JOIN BIZ_PUB_DATA_R_ENERGY_D g ON e.Data_ID = g.Data_ID 
                    WHERE e.METER_ASSET_NO = :meter_asset_no
                        AND g.TV > TO_DATE(:start_date, 'yyyy-mm-dd') 
                        AND g.TV < TO_DATE(:end_date, 'yyyy-mm-dd')
                    ) z
                LEFT JOIN BIZ_PUB_DATA_OTHER_D y
                    ON z.Data_ID = y.Data_ID and z.tv = y.tv
                    WHERE z.nocongto = :meter_asset_no
                    AND TRUNC(y.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(y.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        AND TRUNC(z.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(z.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
        '''
    elif meter_model1 == "HHM38":
        query = '''
                        SELECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, 
                            z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
                            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, 
                            z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
                            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
                FROM
                    (SELECT DISTINCT e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto, e.tv, 
                            e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
                            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3, 
                            g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
                            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
                    FROM
                        (SELECT DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, c.tv, 
                                FA dn_huucong_giao, FA_T1 dn_huucong_giao_bieu1, FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3, 
                                FR dn_huucong_nhan, FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
                        FROM A_Data_catalogue d
                        LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID 
                        WHERE d.METER_ASSET_NO = :meter_asset_no
                AND TRUNC(c.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                            AND TRUNC(c.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        ) e
                    LEFT JOIN BIZ_PUB_DATA_R_ENERGY_D g ON e.Data_ID = g.Data_ID 
                    WHERE e.METER_ASSET_NO = :meter_asset_no
                        AND g.TV > TO_DATE(:start_date, 'yyyy-mm-dd') 
                        AND g.TV < TO_DATE(:end_date, 'yyyy-mm-dd')
                    ) z
                LEFT JOIN BIZ_PUB_DATA_OTHER_D y
                    ON z.Data_ID = y.Data_ID and z.tv = y.tv
                    WHERE z.nocongto = :meter_asset_no
                    AND TRUNC(y.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(y.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
                        AND TRUNC(z.tv) >= TO_DATE(:start_date, 'yyyy-mm-dd')
                    AND TRUNC(z.tv) <= TO_DATE(:end_date, 'yyyy-mm-dd')
        '''
    elif meter_model1 == "":
        return "Loại công tơ không hợp lệ."
    else:
        return "Loại công tơ không hợp lệ."

    cursor = conn.cursor()
    cursor.execute(query, meter_asset_no=meter_asset_no, start_date=start_date, end_date=end_date)
    data = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    result = []
    for row in data:
        row_dict = {}
        for i, column in enumerate(columns):
            row_dict[column] = row[i]
        result.append(row_dict)

    cursor.close()

    def json_encoder(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    json_string = json.dumps(result, default=json_encoder, ensure_ascii=False)  # Chuyển đổi đối tượng Python thành chuỗi JSON

    # Tìm và giải mã giá trị sau chuỗi "TENKHACHHANG"
    match = re.search(r'"TENKHACHHANG":"(.*?)"', json_string)
    if match:
        decoded_value = match.group(1).encode('latin-1').decode('utf-8')

        # Thay thế giá trị trong chuỗi JSON
        modified_json_string = re.sub(r'"TENKHACHHANG":".*?"', f'"TENKHACHHANG":"{decoded_value}"', json_string)

        json_string = json.loads(modified_json_string)
        return modified_json_string

    return json_string

def check_api_status(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if not is_api_active:
            return jsonify({'error': 'API is currently shut down'}), 503
        return f(*args, **kwargs)
    return decorated_function


# Định nghĩa một endpoint để lấy dữ liệu từ bảng trong cơ sở dữ liệu Oracle dựa trên số công tơ và thời gian
@app.route('/data', methods=['GET'])
@authenticate_token
def get_data():
    meter_asset_no = request.args.get('cong_to')
    thoi_gian = request.args.get('thoi_gian')
    token = request.headers.get('Authorization')

    # Lấy địa chỉ IP
    ip_address = request.remote_addr
    
    # Lấy token từ request headers
    token = request.headers.get('Authorization')

    # Kiểm tra xem token có hợp lệ không
    if not is_valid_token(token):
        return jsonify(error='Token khong hop le hoac kiem tra lai thoi gian duoc cap Token'), 401

    if not meter_asset_no:
        return jsonify(error='Thiếu tham số cong_to')

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date and end_date:
        return get_data_by_date_range(meter_asset_no, start_date, end_date)
    else:
        # Lưu log
        save_log(token, meter_asset_no, thoi_gian, ip_address)

        # Truy vấn loại công tơ
        query_meter_model = "SELECT meter_model FROM a_equip_meter WHERE assetno = :meter_asset_no"
        cursor = conn.cursor()
        cursor.execute(query_meter_model, meter_asset_no=meter_asset_no)
        meter_model = cursor.fetchone()

        if meter_model is None:
            return jsonify(error='No công tơ không hợp lệ.'), 404

        meter_model1 = meter_model[0]

    # Truy vấn dữ liệu dựa trên loại công tơ
    if meter_model1 == "HHM11-V1":
                query = '''
select A.CONS_NO MA_DDO, A.CONS_NAME TEN_KHANG,A.METER_ASSET_NO METER_ID,D.MR_TIME_FA THOIGIANDOC,  
B.FA DN_HUUCONG_GIAO,B.FA_T1 DN_HUUCONG_GIAO_BIEU1,B.FA_T2 DN_HUUCONG_GIAO_BIEU2,B.FA_T3 DN_HUUCONG_GIAO_BIEU3, 
B.FR DN_VOCONG_GIAO,B.FR_T1 DN_VOCONG_GIAO_BIEU1,B.FR_T2 DN_VOCONG_GIAO_BIEU2,B.FR_T2 DN_VOCONG_GIAO_BIEU3,  
 C.RA DN_HUUCONG_NHAN,C.RA_T1 DN_HUUCONG_NHAN_BIEU1,C.RA_T2 DN_HUUCONG_NHAN_BIEU2,C.RA_T3 DN_HUUCONG_NHAN_BIEU3, 
 C.RR DN_VOCONG_NHAN,C.RR_T1 DN_VOCONG_NHAN_BIEU1,C.RR_T2 DN_VOCONG_NHAN_BIEU2,C.RR_T2 DN_VOCONG_NHAN_BIEU3  
 from (select DATA_ID,CONS_NO,CONS_NAME,METER_ASSET_NO  
from A_DATA_CATALOGUE where METER_ASSET_NO= :meter_asset_no) A inner join  
BIZ_PUB_DATA_F_ENERGY_D B on A.DATA_ID=B.DATA_ID and trunc(B.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_R_ENERGY_D C on C.DATA_ID=A.DATA_ID and trunc(C.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_OTHER_D D on A.DATA_ID=D.DATA_ID AND TRUNC(D.TV)=to_date(:thoi_gian,'yyyy-mm-dd')
            
        '''
    elif meter_model1 == "HHM31/38":
        query = '''
select A.CONS_NO MA_DDO, A.CONS_NAME TEN_KHANG,A.METER_ASSET_NO METER_ID,D.MR_TIME_FA THOIGIANDOC,  
B.FA DN_HUUCONG_GIAO,B.FA_T1 DN_HUUCONG_GIAO_BIEU1,B.FA_T2 DN_HUUCONG_GIAO_BIEU2,B.FA_T3 DN_HUUCONG_GIAO_BIEU3, 
B.FR DN_VOCONG_GIAO,B.FR_T1 DN_VOCONG_GIAO_BIEU1,B.FR_T2 DN_VOCONG_GIAO_BIEU2,B.FR_T2 DN_VOCONG_GIAO_BIEU3,  
 C.RA DN_HUUCONG_NHAN,C.RA_T1 DN_HUUCONG_NHAN_BIEU1,C.RA_T2 DN_HUUCONG_NHAN_BIEU2,C.RA_T3 DN_HUUCONG_NHAN_BIEU3, 
 C.RR DN_VOCONG_NHAN,C.RR_T1 DN_VOCONG_NHAN_BIEU1,C.RR_T2 DN_VOCONG_NHAN_BIEU2,C.RR_T2 DN_VOCONG_NHAN_BIEU3  
 from (select DATA_ID,CONS_NO,CONS_NAME,METER_ASSET_NO  
from A_DATA_CATALOGUE where METER_ASSET_NO= :meter_asset_no) A inner join  
BIZ_PUB_DATA_F_ENERGY_D B on A.DATA_ID=B.DATA_ID and trunc(B.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_R_ENERGY_D C on C.DATA_ID=A.DATA_ID and trunc(C.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_OTHER_D D on A.DATA_ID=D.DATA_ID AND TRUNC(D.TV)=to_date(:thoi_gian,'yyyy-mm-dd')
        '''
    elif meter_model1 == "HHM31":
        query = '''
select A.CONS_NO MA_DDO, A.CONS_NAME TEN_KHANG,A.METER_ASSET_NO METER_ID,D.MR_TIME_FA THOIGIANDOC,  
B.FA DN_HUUCONG_GIAO,B.FA_T1 DN_HUUCONG_GIAO_BIEU1,B.FA_T2 DN_HUUCONG_GIAO_BIEU2,B.FA_T3 DN_HUUCONG_GIAO_BIEU3, 
B.FR DN_VOCONG_GIAO,B.FR_T1 DN_VOCONG_GIAO_BIEU1,B.FR_T2 DN_VOCONG_GIAO_BIEU2,B.FR_T2 DN_VOCONG_GIAO_BIEU3,  
 C.RA DN_HUUCONG_NHAN,C.RA_T1 DN_HUUCONG_NHAN_BIEU1,C.RA_T2 DN_HUUCONG_NHAN_BIEU2,C.RA_T3 DN_HUUCONG_NHAN_BIEU3, 
 C.RR DN_VOCONG_NHAN,C.RR_T1 DN_VOCONG_NHAN_BIEU1,C.RR_T2 DN_VOCONG_NHAN_BIEU2,C.RR_T2 DN_VOCONG_NHAN_BIEU3  
 from (select DATA_ID,CONS_NO,CONS_NAME,METER_ASSET_NO  
from A_DATA_CATALOGUE where METER_ASSET_NO= :meter_asset_no) A inner join  
BIZ_PUB_DATA_F_ENERGY_D B on A.DATA_ID=B.DATA_ID and trunc(B.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_R_ENERGY_D C on C.DATA_ID=A.DATA_ID and trunc(C.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_OTHER_D D on A.DATA_ID=D.DATA_ID AND TRUNC(D.TV)=to_date(:thoi_gian,'yyyy-mm-dd')
        '''
    elif meter_model1 == "HHM38":
        query = '''
SELECT  z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
select A.CONS_NO MA_DDO, A.CONS_NAME TEN_KHANG,A.METER_ASSET_NO METER_ID,D.MR_TIME_FA THOIGIANDOC,  
B.FA DN_HUUCONG_GIAO,B.FA_T1 DN_HUUCONG_GIAO_BIEU1,B.FA_T2 DN_HUUCONG_GIAO_BIEU2,B.FA_T3 DN_HUUCONG_GIAO_BIEU3, 
B.FR DN_VOCONG_GIAO,B.FR_T1 DN_VOCONG_GIAO_BIEU1,B.FR_T2 DN_VOCONG_GIAO_BIEU2,B.FR_T2 DN_VOCONG_GIAO_BIEU3,  
 C.RA DN_HUUCONG_NHAN,C.RA_T1 DN_HUUCONG_NHAN_BIEU1,C.RA_T2 DN_HUUCONG_NHAN_BIEU2,C.RA_T3 DN_HUUCONG_NHAN_BIEU3, 
 C.RR DN_VOCONG_NHAN,C.RR_T1 DN_VOCONG_NHAN_BIEU1,C.RR_T2 DN_VOCONG_NHAN_BIEU2,C.RR_T2 DN_VOCONG_NHAN_BIEU3  
 from (select DATA_ID,CONS_NO,CONS_NAME,METER_ASSET_NO  
from A_DATA_CATALOGUE where METER_ASSET_NO= :meter_asset_no) A inner join  
BIZ_PUB_DATA_F_ENERGY_D B on A.DATA_ID=B.DATA_ID and trunc(B.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_R_ENERGY_D C on C.DATA_ID=A.DATA_ID and trunc(C.TV)=to_date(:thoi_gian,'yyyy-mm-dd')  
left join BIZ_PUB_DATA_OTHER_D D on A.DATA_ID=D.DATA_ID AND TRUNC(D.TV)=to_date(:thoi_gian,'yyyy-mm-dd')
        '''
    
    else:
        print(meter_model)
        return jsonify(error='Loại công tơ không hợp lệ.')

    if thoi_gian:
        try:
            thoi_gian = datetime.datetime.strptime(thoi_gian, '%d-%m-%y').strftime('%Y-%m-%d')
            print(thoi_gian)
            # thoi_gian = datetime.datetime.strptime(thoi_gian, '%d-%m-%y').strftime('%d-%b-%y').upper()
            # thoi_gian = '%' + thoi_gian + '%'
        except ValueError:
            return jsonify(error='Định dạng thời gian không hợp lệ')

    cursor = conn.cursor()
    cursor.execute(query, meter_asset_no=meter_asset_no, thoi_gian=thoi_gian)
    data = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    result = []
    for row in data:
        row_dict = {}
        for i, column in enumerate(columns):
            row_dict[column] = row[i]
        result.append(row_dict)

    cursor.close()


    def json_encoder(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    json_string = json.dumps(result, default=json_encoder, ensure_ascii=False)

    # Tìm và giải mã giá trị sau chuỗi "TENKHACHHANG"
    match = re.search(r'"TENKHACHHANG":"(.*?)"', json_string)
    if match:
        decoded_value = match.group(1).encode('latin-1').decode('utf-8')
        # Thay thế giá trị trong chuỗi JSON
        json_string = re.sub(r'"TENKHACHHANG":".*?"', f'"TENKHACHHANG":"{decoded_value}"', json_string)

    return jsonify(json.loads(json_string))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Endpoint to shut down the Flask application.
    """
    token = request.headers.get('Authorization')

    # Check if the token is valid for security reasons
    if not is_valid_token(token):
        return jsonify(error='Token không hợp lệ'), 401

    print("Shutting down gracefully...")
    
    # Perform any cleanup tasks if needed
    
    os.kill(os.getpid(), signal.SIGINT)  # Send a signal to gracefully shut down the Flask app
    
    return jsonify(message='Shutting down...')

@app.route('/start', methods=['POST'])  
def start_api():
    global is_api_active
    is_api_active = True
    return 'API has been started'


# Endpoint bảo mật yêu cầu token hợp lệ
@app.route('/protected', methods=['GET'])
@authenticate_token
def protected():
    return jsonify(message='Truy cập thành công vào endpoint bảo mật!')

# Endpoint không yêu cầu xác thực token
@app.route('/unprotected', methods=['GET'])
def unprotected():
    return jsonify(message='Truy cập thành công vào endpoint không yêu cầu xác thực token!')


logging.basicConfig(level=logging.DEBUG)



if __name__ == '__main__':
    app.run(debug=True,port=1009)
    # app.run(host="192.168.30.252",port=1009)