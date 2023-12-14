from store_data import *
from datetime import datetime
from arima import perform_arma_prediction

data = [11, 23, 32, 43, 54, 65, 76, 87, 98, 102]


print(perform_arma_prediction(data))
'''
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")

write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
write_data("2023-12-13 23:46:27;2.056;104")
tmps = read_data()

for tmp in tmps:
    print(tmp)
    print("....")
    print(tmp[1])
    print(tmp[2])
    print(tmp[0])
    print("....")
    
    # 使用分号 ; 分割字符串
    fields = tmp.split(";")

    # 打印分割后的字段
    print("Date:", fields[0])
    date_object = datetime.strptime(fields[0], "%Y-%m-%d %H:%M:%S")
    print("Date Object:", date_object)
    # 获取当前时间
    current_time = datetime.now()

    # 比较两个 datetime 对象
    if date_object > current_time:
        print("日期在当前时间之后")
    elif date_object < current_time:
        print("日期在当前时间之前")
    else:
        print("日期与当前时间相同")
    print("Value 1:", fields[1])
    print("Value 2:", fields[2])
    '''
