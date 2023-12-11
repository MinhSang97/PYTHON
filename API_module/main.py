from flask import Flask, jsonify, request
from auth import is_valid_login, generate_token, save_token
from data import get_data
from log import save_log
from auth import authenticate_token

app = Flask(__name__)

# Định nghĩa một endpoint để login và sinh ra token mới
@app.route('/login', methods=['GET'])
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

# Định nghĩa một endpoint để lấy dữ liệu từ bảng trong cơ sở dữ liệu Oracle dựa trên số công tơ và thời gian
@app.route('/data', methods=['GET'])
@authenticate_token
def get_data():
    meter_asset_no = request.args.get('cong_to')
    thoi_gian = request.args.get('thoi_gian')
    token = request.headers.get('Authorization')
    
    # Lấy dữ liệu từ cơ sở dữ liệu
    data = fetch_data_from_db(meter_asset_no, thoi_gian)

    return jsonify(data=data)

# Hàm lấy dữ liệu từ cơ sở dữ liệu
def fetch_data_from_db(meter_asset_no, thoi_gian):
    # TODO: Lấy dữ liệu từ cơ sở dữ liệu dựa trên số công tơ và thời gian
    # Trả về dữ liệu dưới dạng danh sách hoặc từ điển
    
    data = [...]  # Dữ liệu từ cơ sở dữ liệu

    return data

# Hàm decorator kiểm tra tính hợp lệ của token
def authenticate_token(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        # TODO: Kiểm tra tính hợp lệ của token
        # Nếu token không hợp lệ, trả về lỗi và status code 401 Unauthorized

        return f(*args, **kwargs)

    return decorated_function

if __name__ == '__main__':
    app.run(port=1234)
