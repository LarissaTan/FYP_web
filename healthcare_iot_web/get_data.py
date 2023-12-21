from flask import Flask, render_template, request, jsonify
from datetime import datetime
from store_data import *
from store_data_pulse import *
from web3 import Web3
from arima import *
import hashlib

# 创建 Flask 应用
app = Flask(__name__)

# Ethereum 智能合约交互代码
key = b'SfMxJjQQBBZ1DrJZ0xZwiM0K1jvFAWB1c8pQL7W9mQs='

account_address = '0x46C3d6d846Ada43774999Fc066211BC961b19F70'
private_key = '0f52b49df6f1d8c737dad58969e6b66bc1ee53f8e2f314b19eb7a4cddd9e9000'

web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/8600c337513c4cbc8e8d3d9f1f577598'))

conadress = "0x408449Ae12bF1f3154b422f56f9BEBB04B6B1b9d"
conabi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "newMessage",
				"type": "string"
			}
		],
		"name": "addMessage",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllMessages",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLastMessage",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getMessage",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "newMessage",
				"type": "string"
			}
		],
		"name": "setMessage",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

contra = web3.eth.contract(address=conadress, abi=conabi)



@app.route("/get_previous_ecg")
def get_previous_ecg():
	data = read_data()
	data_ecg = []
	print(data.__len__())
	for i in data:
		tmp_ecg_data = i[1]
		print(tmp_ecg_data)
                
		data_ecg.append(float(tmp_ecg_data))
    
	print(data_ecg.__len__())
                
	return jsonify(data_ecg)

@app.route("/get_previous_pulse")
def get_previous_pulse():
	data = read_data_pulse()
	data_pulse = []
	print(data.__len__())
	for i in data:
		tmp_pulse_data = i[1]
		print(tmp_pulse_data)
                
		data_pulse.append(int(tmp_pulse_data))
    
	print(data_pulse.__len__())
                
	return jsonify(data_pulse)

	


# Flask 路由，与智能合约交互并在终端输出数据
@app.route("/get_last_message")
def get_last_message():

    result = contra.functions.getLastMessage().call()
    #get last message
    print(result)
    
    # 在终端输出数据
    #print("Last Message:", decrypted_message)

    # 解析字符串中的数据
    data_start_index = result.find("['")
    data_end_index = result.find("']")
    if data_start_index != -1 and data_end_index != -1:
        data_string = result[data_start_index + 2: data_end_index]
        data_list = data_string.split("', '")          
        for element in data_list:
            print("here is element")
            parts = element.split(', ')
            time = parts[0][0:-1]
            print(parts)
            value1 = float(parts[1])
            value2 = int(parts[2])
            value3 = parts[3][1:]
            #只看最新的
            tmps = read_data()
            tmp_time = tmps[-1][0]
            tmp_time = datetime.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            print(time)
            print(tmp_time)
            
            #开始ISF

            if time > tmp_time:
                print("start ISF")

                data_ecg_pre_set = read_data()
                data_ecg_pre_set = [float(x[1]) for x in data_ecg_pre_set]
            
                forecast_data_set = perform_arma_prediction(data_ecg_pre_set)
                
                print("Forecast data set is: ")
                print(forecast_data_set)
                for y in forecast_data_set:
                    if isinstance(y, (int, float)):
                          y = round(y, 3)
                          
                # 计算均值
                data_combined_ecg = forecast_data_set + data_ecg_pre_set
                print("data_combined_ecg is: "+ str(data_combined_ecg))
                tmp_len = len(data_combined_ecg)
                tmp_sum = sum([x for x in data_combined_ecg if isinstance(x, (int, float))])
                tmp_sum = round(tmp_sum, 3)
                '''
                print("type pf tmp_sum is: " + str(type(tmp_sum)))
                print("tmp_len is: " + str(tmp_len))
                print("tmp_sum is: " + str(tmp_sum))
             	'''
                if isinstance(tmp_sum, (int, float)):
                    mean_ecg = round(tmp_sum / tmp_len, 3)

                print(f"The combined average value is: {mean_ecg}")
                raw_ecg = round((value1 + mean_ecg) - float(5.0),3)
                print(f"The raw value is: {raw_ecg}")
                #check hash
                data_for_hash = str(time) + str(raw_ecg) + str(value2)
                hash_vaule = hashlib.sha256(data_for_hash.encode()).hexdigest()
                print(data_for_hash)

                if(hash_vaule == value3):
                    print("The hash value is correct")
                    tmp_write_data = str(time) + ";" + str(raw_ecg)
                    write_data(tmp_write_data)

                    response_data = {
        			    "ecg": raw_ecg,
        			    "time": time
    			    }
                    return jsonify(response_data)

                else:
                    print("The hash value is not correct")
                    return jsonify({"error": "Hash is not correct"})
    tmp_ecg_pre_data = read_data()
    tmp_ecg_pre_data = tmps[-1][1]
    tmp_time_pre_data = tmps[-1][0]
    response_data = {
		"ecg": tmp_ecg_pre_data,
		"time": tmp_time_pre_data
	}
    return jsonify(response_data)

   
@app.route("/get_last_valid_pulse")
def get_last_valid_pulse():
    result = contra.functions.getLastMessage().call()

    # 解析字符串中的数据
    data_start_index = result.find("['")
    data_end_index = result.find("']")
    tmp_pulse = 0
    
    if data_start_index != -1 and data_end_index != -1:
        data_string = result[data_start_index + 2: data_end_index]
        data_list = data_string.split("', '")
        
        # 输出每个元素
        for element in data_list:
            
            print(element)
            time = element[0:19]
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            tmps = read_data_pulse()
            tmp_time = tmps[-1][0]
            tmp_pulse = tmps[-1][1]
            tmp_time = datetime.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
            
			#忽略前面的数据，只输出和存的最新数据一样的数据
            if time == tmp_time:
                pulse = tmps[-1][1]
            
			#比存的更新的数据
            if time > tmp_time:
                tmp = element[29]
                if (tmp != '-'):
                    pulse = element[29:32]
                    tmp_write_data = element[0:19] + ";" + pulse
                    write_data_pulse(tmp_write_data)
                    print(pulse)
                    return jsonify(pulse)
                
    pulse = tmp_pulse
    return jsonify(pulse)
      

# Flask 路由，渲染 index.html 模板
@app.route("/")
def root():
    return render_template("index.html")

# 运行 Flask 应用在端口 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
