import pickle

# Đường dẫn tới file dataset.pkl
dataset_file = "D:\TEST\dataset.pkl"

# Đọc nội dung của file
with open(dataset_file, "rb") as f:
    dataset = pickle.load(f)

# Sử dụng dataset cho các mục đích khác
print(dataset)