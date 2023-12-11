from flask import jsonify, request
from auth import is_valid_token, authenticate_token, save_log
import cx_Oracle
import datetime
import json
import re
from log import save_log


# Thiết lập thông tin kết nối với cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('118.69.35.119', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

# Định nghĩa một endpoint để lấy dữ liệu từ bảng trong cơ sở dữ liệu Oracle dựa trên số công tơ và thời gian
def get_data():
    meter_asset_no = request.args.get('cong_to')
    thoi_gian = request.args.get('thoi_gian')
    token = request.headers.get('Authorization')
    
    # Lấy token từ request headers
    token = request.headers.get('Authorization')

    # Kiểm tra xem token có hợp lệ không
    if not is_valid_token(token):
        return jsonify(error='Token khong hop le hoac kiem tra lai thoi gian duoc cap Token'), 401

    if not meter_asset_no:
        return jsonify(error='Thiếu tham số cong_to')

    # Lưu log
    save_log(token, meter_asset_no, thoi_gian)

    # Truy vấn loại công tơ
    query_meter_model = "SELECT meter_model FROM a_equip_meter WHERE assetno = :meter_asset_no"
    cursor = conn.cursor()
    cursor.execute(query_meter_model, meter_asset_no=meter_asset_no)
    meter_model = cursor.fetchone()[0]

    # Truy vấn dữ liệu dựa trên loại công tơ
    if meter_model == "HHM11-V1":
        query = '''
            SElECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
            FROM
            (SELECT DISTINCT  e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto, e.TV thoigiandoc,
            e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3,
            g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
            FROM
            (SELECT DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, TV,
            FA dn_huucong_giao, FA_T1 dn_huucong_giao_bieu1, FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3,
            FR dn_huucong_nhan, FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
            FROM A_Data_catalogue d
            LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID WHERE d.METER_ASSET_NO = :meter_asset_no AND c.RECEIVE_TIME LIKE :thoi_gian) e
            LEFT JOIN BIZ_PUB_DATA_R_ENERGY_D g ON e.Data_ID = g.Data_ID)z
            LEFT join BIZ_PUB_DATA_OTHER_D y
            ON z.Data_ID = y.Data_ID and y.MR_TIME_FA LIKE :thoi_gian

        '''
    elif meter_model == "HHM31/38":
        query = '''
            SELECT DISTINCT z.Ma_DIEMDO, z.tenkhachhang, z.nocongto, y.MR_TIME_FA thoigiandoc, z.dn_huucong_giao, z.dn_huucong_giao_bieu1, z.dn_huucong_giao_bieu2, z.dn_huucong_giao_bieu3,
            z.dn_huucong_nhan, z.dn_huucong_nhan_bieu1, z.dn_huucong_nhan_bieu2, z.dn_huucong_nhan_bieu3, z.dn_vocong_giao, z.dn_vocong_giao_bieu1, z.dn_vocong_giao_bieu2, z.dn_vocong_giao_bieu3,
            z.dn_vocong_nhan, z.dn_vocong_nhan_bieu1, z.dn_vocong_nhan_bieu2, z.dn_vocong_nhan_bieu3
            FROM
            (SElECT DISTINCT  e.Data_ID, e.Ma_DIEMDO, e.tenkhachhang, e.METER_ASSET_NO nocongto,e.TV thoigiandoc, e.dn_huucong_giao, e.dn_huucong_giao_bieu1, e.dn_huucong_giao_bieu2, e.dn_huucong_giao_bieu3,
            e.dn_huucong_nhan, e.dn_huucong_nhan_bieu1, e.dn_huucong_nhan_bieu2, e.dn_huucong_nhan_bieu3, g.RA dn_vocong_giao, g.RA_T1 dn_vocong_giao_bieu1, g.RA_T2 dn_vocong_giao_bieu2, g.RA_T3 dn_vocong_giao_bieu3,
            g.RR dn_vocong_nhan, g.RR_T1 dn_vocong_nhan_bieu1, g.RR_T2 dn_vocong_nhan_bieu2, g.RR_T3 dn_vocong_nhan_bieu3
            FROM
            (SELECT  DISTINCT d.Data_ID, CONS_NO Ma_DIEMDO, CONS_NAME tenkhachhang, METER_ASSET_NO, c.TV, FA dn_huucong_giao,FA_T1 dn_huucong_giao_bieu1,
            FA_T2 dn_huucong_giao_bieu2, FA_T3 dn_huucong_giao_bieu3, FR dn_huucong_nhan,FR_T1 dn_huucong_nhan_bieu1, FR_T2 dn_huucong_nhan_bieu2, FR_T3 dn_huucong_nhan_bieu3
            FROM A_Data_catalogue d
            LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c 
            ON d.Data_ID = c.Data_ID  and d.METER_ASSET_NO = :meter_asset_no and c.RECEIVE_TIME LIKE :thoi_gian)e
            LEFT join BIZ_PUB_DATA_R_ENERGY_D g
            ON e.Data_ID = g.Data_ID where e.METER_ASSET_NO = :meter_asset_no and g.tv LIKE :thoi_gian)z
            LEFT join BIZ_PUB_DATA_OTHER_D y
            ON z.Data_ID = y.Data_ID and y.MR_TIME_FA LIKE :thoi_gian
        '''
    else:
        return "Loại công tơ không hợp lệ."

    if thoi_gian:
        try:
            thoi_gian = datetime.datetime.strptime(thoi_gian, '%d-%m-%y').strftime('%d-%b-%y').upper()
            # query += " AND TO_CHAR(RECEIVE_TIME, 'DD-MON-YY') LIKE :thoi_gian"
            thoi_gian = '%' + thoi_gian + '%'
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

    json_string = json.dumps(result, default=json_encoder, ensure_ascii=False)  # Chuyển đối tượng Python thành chuỗi JSON

    # Tìm và giải mã giá trị sau chuỗi "TENKHACHHANG"
    match = re.search(r'"TENKHACHHANG":"(.*?)"', json_string)
    if match:
        decoded_value = match.group(1).encode('latin-1').decode('utf-8')

        # Thay thế giá trị trong chuỗi JSON
        modified_json_string = re.sub(r'"TENKHACHHANG":".*?"', f'"TENKHACHHANG":"{decoded_value}"', json_string)

        json_string = json.loads(modified_json_string)
        return modified_json_string

    return json_string
