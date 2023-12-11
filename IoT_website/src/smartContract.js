
// Rhino 导入
//var Web3 = Java.type('org.web3j.protocol.Web3j');
//var System = Java.type('java.lang.System');

// Connect to the Ethereum node
var web3;
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3("https://goerli.infura.io/v3/8600c337513c4cbc8e8d3d9f1f577598");
}

// Contract address and ABI
var contractAddress = '0x408449Ae12bF1f3154b422f56f9BEBB04B6B1b9d';
var contractABI = [
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
    }// Contract ABI (same as the one used in the Python code)
];

// Create contract instance
var contract = new web3.eth.Contract(contractABI, contractAddress);

// Define the function to get all messages
function getAllMessages() {
    console.log("Calling getAllMessages");
    return contract.methods.getLastMessage().call()
}


window.onload = function() {

    try {
        var messages = getAllMessages();
        console.log(messages);
        document.getElementById('out1').innerText = "All Messages: " + JSON.stringify(messages);
    } catch (error) {
        document.getElementById('out1').innerText = "Error: " + error;
    }

};

