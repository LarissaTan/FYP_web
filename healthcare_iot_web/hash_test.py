import hashlib

data = "2023-12-13 02:15:141.501-1"
hashed_result = hashlib.sha256(data.encode()).hexdigest()
print(hashed_result)

'''


# 清空文件内容
with open(file_path, 'w') as file:
    file.write('')
    '''