import web3
import eth_abi
import eth_account
from web3.auto import w3

import datetime
import struct
import json
import itertools
import math

gnosisrpc = 'https://rpc.gnosischain.com/'
w3 = web3.Web3(web3.HTTPProvider(gnosisrpc))

uint64 = pow(2, 64) - 1     # 18446744073709551615
uint128 = pow(2, 128) - 1   # 340282366920938463463374607431768211455
addrtype = pow(2, 20 * 8) - 1

lotaddr = '0x6dB8381b2B41b74E17F5D4eB82E8d5b04ddA0a82'
lotabi =  json.loads("[ { \"inputs\": [ { \"internalType\": \"uint64\", \"name\": \"day\", \"type\": \"uint64\" } ], \"stateMutability\": \"nonpayable\", \"type\": \"constructor\" }, { \"anonymous\": false, \"inputs\": [ { \"indexed\": true, \"internalType\": \"contract IERC20\", \"name\": \"token\", \"type\": \"address\" }, { \"indexed\": true, \"internalType\": \"address\", \"name\": \"funder\", \"type\": \"address\" }, { \"indexed\": true, \"internalType\": \"address\", \"name\": \"signer\", \"type\": \"address\" } ], \"name\": \"Create\", \"type\": \"event\" }, { \"anonymous\": false, \"inputs\": [ { \"indexed\": true, \"internalType\": \"bytes32\", \"name\": \"key\", \"type\": \"bytes32\" }, { \"indexed\": false, \"internalType\": \"uint256\", \"name\": \"unlock_warned\", \"type\": \"uint256\" } ], \"name\": \"Delete\", \"type\": \"event\" }, { \"anonymous\": false, \"inputs\": [ { \"indexed\": true, \"internalType\": \"address\", \"name\": \"funder\", \"type\": \"address\" }, { \"indexed\": true, \"internalType\": \"address\", \"name\": \"recipient\", \"type\": \"address\" } ], \"name\": \"Enroll\", \"type\": \"event\" }, { \"anonymous\": false, \"inputs\": [ { \"indexed\": true, \"internalType\": \"bytes32\", \"name\": \"key\", \"type\": \"bytes32\" }, { \"indexed\": false, \"internalType\": \"uint256\", \"name\": \"escrow_amount\", \"type\": \"uint256\" } ], \"name\": \"Update\", \"type\": \"event\" }, { \"inputs\": [ { \"internalType\": \"contract IERC20\", \"name\": \"token\", \"type\": \"address\" }, { \"internalType\": \"address\", \"name\": \"recipient\", \"type\": \"address\" }, { \"components\": [ { \"internalType\": \"bytes32\", \"name\": \"data\", \"type\": \"bytes32\" }, { \"internalType\": \"bytes32\", \"name\": \"reveal\", \"type\": \"bytes32\" }, { \"internalType\": \"uint256\", \"name\": \"packed0\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"packed1\", \"type\": \"uint256\" }, { \"internalType\": \"bytes32\", \"name\": \"r\", \"type\": \"bytes32\" }, { \"internalType\": \"bytes32\", \"name\": \"s\", \"type\": \"bytes32\" } ], \"internalType\": \"struct OrchidLottery1.Ticket[]\", \"name\": \"tickets\", \"type\": \"tuple[]\" }, { \"internalType\": \"bytes32[]\", \"name\": \"refunds\", \"type\": \"bytes32[]\" } ], \"name\": \"claim\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"contract IERC20\", \"name\": \"token\", \"type\": \"address\" }, { \"internalType\": \"uint256\", \"name\": \"amount\", \"type\": \"uint256\" }, { \"internalType\": \"address\", \"name\": \"signer\", \"type\": \"address\" }, { \"internalType\": \"int256\", \"name\": \"adjust\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"warn\", \"type\": \"int256\" }, { \"internalType\": \"uint256\", \"name\": \"retrieve\", \"type\": \"uint256\" } ], \"name\": \"edit\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"address\", \"name\": \"signer\", \"type\": \"address\" }, { \"internalType\": \"int256\", \"name\": \"adjust\", \"type\": \"int256\" }, { \"internalType\": \"int256\", \"name\": \"warn\", \"type\": \"int256\" }, { \"internalType\": \"uint256\", \"name\": \"retrieve\", \"type\": \"uint256\" } ], \"name\": \"edit\", \"outputs\": [], \"stateMutability\": \"payable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"bool\", \"name\": \"cancel\", \"type\": \"bool\" }, { \"internalType\": \"address[]\", \"name\": \"recipients\", \"type\": \"address[]\" } ], \"name\": \"enroll\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"address\", \"name\": \"funder\", \"type\": \"address\" }, { \"internalType\": \"address\", \"name\": \"recipient\", \"type\": \"address\" } ], \"name\": \"enrolled\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"contract IERC20\", \"name\": \"token\", \"type\": \"address\" }, { \"internalType\": \"address\", \"name\": \"signer\", \"type\": \"address\" }, { \"internalType\": \"uint64\", \"name\": \"marked\", \"type\": \"uint64\" } ], \"name\": \"mark\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"address\", \"name\": \"sender\", \"type\": \"address\" }, { \"internalType\": \"uint256\", \"name\": \"amount\", \"type\": \"uint256\" }, { \"internalType\": \"bytes\", \"name\": \"data\", \"type\": \"bytes\" } ], \"name\": \"onTokenTransfer\", \"outputs\": [ { \"internalType\": \"bool\", \"name\": \"\", \"type\": \"bool\" } ], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"contract IERC20\", \"name\": \"token\", \"type\": \"address\" }, { \"internalType\": \"address\", \"name\": \"funder\", \"type\": \"address\" }, { \"internalType\": \"address\", \"name\": \"signer\", \"type\": \"address\" } ], \"name\": \"read\", \"outputs\": [ { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" }, { \"internalType\": \"uint256\", \"name\": \"\", \"type\": \"uint256\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"uint256\", \"name\": \"count\", \"type\": \"uint256\" }, { \"internalType\": \"bytes32\", \"name\": \"seed\", \"type\": \"bytes32\" } ], \"name\": \"save\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"address\", \"name\": \"sender\", \"type\": \"address\" }, { \"internalType\": \"uint256\", \"name\": \"amount\", \"type\": \"uint256\" }, { \"internalType\": \"bytes\", \"name\": \"data\", \"type\": \"bytes\" } ], \"name\": \"tokenFallback\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }]")
lottery = w3.eth.contract(address=lotaddr, abi=lotabi)
token = '0x' + '0' * 40

def to_32byte_hex(val):
   return web3.Web3.toHex(web3.Web3.toBytes(val).rjust(32, b'\0'))

def ticket(amount, reveal, ratio, funder, recipient, key):
   data = b'\x00' * 32
   issued = int(datetime.datetime.now().timestamp())
   l2nonce = int(web3.Web3.keccak(text=(f'{datetime.datetime.now()}')).hex(), base=16) & (pow(2,64) - 1)
   expire = pow(2,31) - 1
   packed0 = issued << 192 | l2nonce << 128 | amount
   packed1 = expire << 224 | ratio << 160 | int(funder, base=16)
   digest = web3.Web3.solidityKeccak(
                              ['bytes1', 'bytes1', 'address', 'bytes32', 'address', 'address',
                               'bytes32', 'uint256', 'uint256', 'bytes32'], 
                              [b'\x19', b'\x00', 
                               lotaddr, b'\x00' * 31 + b'\x64', 
                               token, recipient,
                               web3.Web3.solidityKeccak(['bytes32'], [reveal]), packed0,
                               packed1, data])
   sig = w3.eth.account.signHash(digest, private_key=key)

   packed1 = packed1 << 1 | ((sig.v - 27) & 1)
   tk = [data, int(reveal, base=16).to_bytes(32, byteorder='big'), 
         packed0, packed1, 
         to_32byte_hex(sig.r), to_32byte_hex(sig.s)]
   return tk

def claimTicket(tkt, plyr):
   l1nonce = w3.eth.get_transaction_count(plyr['account'])
   func = lottery.functions.claim(token, plyr['account'], [tkt], [])
   tx = func.buildTransaction({
     'chainId': 100,
     'gas': 70000,
     'maxFeePerGas': w3.toWei('2', 'gwei'),
     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
     'nonce': l1nonce
     })

   signed = w3.eth.account.sign_transaction(tx, private_key=plyr['key'])
   txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
   print('Claim transaction hash: ', txhash.hex())

def serializeTicket(tk):
  return tk[0].hex() + tk[1].hex() + to_32byte_hex(tk[2])[2:] + to_32byte_hex(tk[3])[2:] + tk[4][2:] + tk[5][2:]
  return json.dumps([tk[0].hex(), tk[1].hex(), tk[2], tk[3], tk[4], tk[5]])

def deserializeTicket(tstr):
  tk = [tstr[i:i+64] for i in range(0, len(tstr), 64)]
  tk[2] = int(tk[2], base=16)
  tk[3] = int(tk[3], base=16)
  return tk

def setupPlayerTickets(plyr):
   amount_ = input("What size face value do you want to use? ")
   plyr['amount'] = int(float(amount_) * pow(10,18))
   prob = input("What win probability do you want to use (value between 0 and 1)? ")
   plyr['ratio'] = math.floor(uint64 * float(prob))
   return plyr

def newReveal(username):
   str = f'{username}'
   hash = web3.Web3.keccak(text=str).hex()
   return {'str': str, 'hash': hash}

def printPlayer(plyr):
   account = plyr['account']
   print('Player: ', plyr['name'])
   if 'key' in plyr:
      print('  Key: ', plyr['key'].hex())
   if 'reveal' in plyr:
      print('  Reveal: ', plyr['reveal']['hash'])
   print('  L1/L2 Address: ', account)
   if 'amount' in plyr:
      print('  Ticket facevalues: {:.4f}'.format(plyr['amount'] / pow(10,18)))
      print('  Ticket win ratio: {:.2f}'.format(plyr['ratio'] / uint64))

   balance, escrow = checkBalance(account)
   print('  Balance: ', balance)
   print('  Escrow: ', escrow)
   print('  Player code: ', plyr['share'])

def checkBalance(address):
   escrow_amount = lottery.functions.read(token, address, address).call(block_identifier='latest')[0]
   balance = float(escrow_amount & uint128) / pow(10,18)
   escrow = float(escrow_amount >> 128) / pow(10,18)
   return balance, escrow
   

def serializePlayer(plyr):
   return plyr['account'] + plyr['reveal']['hash']

def printHelp():
   print('Commands are help, opponent, pay, claim, info')

def enterOppo():
   opstr = input("Enter opponent's player code. ")
   out = {}
   out['name'] = 'opponent'
   out['account'] = opstr[:42]
   out['reveal'] = {}
   out['reveal']['hash'] = opstr[42:]
   out['share'] = opstr
   return out

def generateTicket(plyr, oppo):
   if oppo == None:
      print("Error! You must set up your opponent's info before you can pay them!")
      return
   tk = ticket(plyr['amount'], plyr['reveal']['hash'], plyr['ratio'], plyr['account'], oppo['account'], plyr['key'])
   print('Send this to your opponent:   ', serializeTicket(tk))

def isWinner(tk):
   data, reveal, packed0, packed1, r, s = tk
   nonce = (packed0 >> 128) & uint64
   ratio = uint64 & (packed1 >> 161)

   hash = web3.Web3.solidityKeccak(['uint256', 'uint128'], [int(reveal, base=16), nonce])
   comp = uint64 & int(hash.hex(), base=16)
   if ratio < comp:
     return False
   return True


def printTicket(tk):
   data, reveal, packed0, packed1, r, s = tk
   amount = packed0 & uint128
   nonce = (packed0 >> 128) & uint64
   funder = addrtype & (packed1 >> 1)
   ratio = uint64 & (packed1 >> 161)

   print('Ticket data:')
   print(f'  Data: {data}')
   print(f'  Reveal: {reveal}')
   print(f'  Packed0: {packed0}')
   print(f'  Packed1: {packed1}')
   print(f'  r: {r}   s: {s}')
   print(f'Packed data:')
   print(f'  Amount: {amount}')
   print(f'  Nonce: {nonce}')
   print(f'  Funder: {funder}')
   print(f'  Ratio: {ratio}')
   
   if isWinner(tk):
      print('\nThis ticket is a winner!')
   else:
      print('\nThis ticket is a loser.')   
   

def claim(plyr, oppo):
   if oppo == None:
      print("Error! You must set up your opponent's info before you can pay them!")
      return
   tstr = input("Enter ticket code. ")
   tk = deserializeTicket(tstr)
   printTicket(tk)
#   print(tk)
   if isWinner(tk):
      claimTicket(tk, plyr)

def printInfo(plyr, oppo):
   print('Your information:')
   printPlayer(plyr)
   if oppo != None:
     print('\nOpponent:')
     printPlayer(oppo)
   

username = input("What is your player's name? ")
player = {'name': username}
player['key'] = web3.Web3.keccak(text=username)
player['account'] = eth_account.account.Account.from_key(player['key']).address
print(f"Your address is {player['account']} which is used as both funder and signer for your Orchid account")
balance, escrow = checkBalance(player['account'])
print(f"Your account balance is {balance} and your escrow is {escrow}")
player['reveal'] = newReveal(username)
player = setupPlayerTickets(player)
player['share'] = serializePlayer(player)

print("Your setup code includes your address and your precommitment for lottery tickets.")
print('Send this setup code to your opponent:   ', player['share'])

opponent = None

while True:
   cmd = input("> ").lower()
   if cmd == 'help':
      printHelp()
   if cmd == 'opponent':
      opponent = enterOppo()
   if cmd == 'pay':
      generateTicket(player, opponent)
   if cmd == 'claim':
      claim(player, opponent)
   if cmd == 'info':
      printInfo(player, opponent)



