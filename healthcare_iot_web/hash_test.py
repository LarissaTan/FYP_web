import hashlib

data = "2023-12-13 02:15:141.501-1"
hashed_result = hashlib.sha256(data.encode()).hexdigest()
print(hashed_result)
