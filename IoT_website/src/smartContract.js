// Connect to the Ethereum node
var Web3 = Java.type('org.web3j.protocol.Web3j');
var web3;
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider("https://goerli.infura.io/v3/8600c337513c4cbc8e8d3d9f1f577598"));
}

// Contract address and ABI
var contractAddress = '0x408449Ae12bF1f3154b422f56f9BEBB04B6B1b9d';
var contractABI = [
    // Contract ABI (same as the one used in the Python code)
];

// Create contract instance
var contract = new web3.eth.Contract(contractABI, contractAddress);

// Define the function to get all messages
function getAllMessages() {
    return contract.methods.getAllMessages().call();
}

// Call the function and log the result
try {
    var messages = getAllMessages();
    print('All Messages:', JSON.stringify(messages));
} catch (error) {
    print('Error:', error);
}
