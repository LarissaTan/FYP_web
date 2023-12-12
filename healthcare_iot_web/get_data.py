from flask import Flask, render_template, request, jsonify
from web3 import Web3
from cryptography.fernet import Fernet

# 创建 Flask 应用
app = Flask(__name__)

# Ethereum 智能合约交互代码
key = b'SfMxJjQQBBZ1DrJZ0xZwiM0K1jvFAWB1c8pQL7W9mQs='
cipher_suite = Fernet(key)

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

# Flask 路由，与智能合约交互并在终端输出数据
@app.route("/get_last_message")
def get_last_message():
    result = contra.functions.getLastMessage().call()
    decrypted_message = cipher_suite.decrypt(bytes(result, 'utf-8')).split(b'|')[-1].decode('utf-8')
    
    # 在终端输出数据
    print("Last Message:", decrypted_message)

    return jsonify({"last_message": decrypted_message})

# Flask 路由，渲染 index.html 模板
@app.route("/")
def root():
    return render_template("index.html")

# 运行 Flask 应用在端口 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
