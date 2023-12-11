import cx_Oracle
from flask import Flask, jsonify, request
import json
import re
import datetime

app = Flask(__name__)

# Thiết lập thông tin kết nối với cơ sở dữ liệu Oracle
dsn_tns = cx_Oracle.makedsn('118.69.35.119', '1521', service_name='hhm')
conn = cx_Oracle.connect(user='MiniMDM10', password='MiniMDM10', dsn=dsn_tns)

# Định nghĩa một endpoint để lấy dữ liệu từ bảng trong cơ sở dữ liệu Oracle dựa trên số công tơ và thời gian
@app.route('/data', methods=['GET'])
def get_data():
    meter_asset_no = request.args.get('cong_to')
    thoi_gian = request.args.get('thoi_gian')

    if not meter_asset_no:
        return jsonify(error='Thiếu tham số cong_to')

    query = '''
        SELECT CONS_NO madiemdo, CONS_NAME tenkhachhang, METER_ASSET_NO nocongto, RECEIVE_TIME thoigianDCUtradulieu, FA dienhuucongchieugiao,FA_T1 dienhuucongchieugiao_bieu1, FA_T2 dienhuucongchieugiao_bieu2, FA_T3 dienhuucongchieugiao_bieu3, FR dienhuucongchieunhan,FR_T1 dienhuucongchieunhan_bieu1, FR_T2 dienhuucongchieunhan_bieu2, FR_T3 dienhuucongchieunhan_bieu3
        FROM A_Data_catalogue d
        LEFT JOIN BIZ_PUB_DATA_F_ENERGY_D c ON d.Data_ID = c.Data_ID
        WHERE METER_ASSET_NO = :meter_asset_no
    '''

    if thoi_gian:
        query += " AND RECEIVE_TIME LIKE :thoi_gian"
        thoi_gian = '%' + thoi_gian + '%'

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

# Chạy ứng dụng trên địa chỉ IP 192.168.30.252 và cổng 5000
if __name__ == '__main__':
    app.run( port=5050)
