import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))


# Create blockchain and add genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain
# after the genesis block
num_blocks_to_add = 10

# Add blocks to the chain
for i in range(0, num_blocks_to_add):
    log_information = f'Block #{blockchain[i].index} has been added to the blockchain!' \
                      f'Previous hash: {blockchain[i - 1].hash}'
    print(log_information)
    timestamp = int(time.time())
    data = f'Data for block #{blockchain[i].index}'
    hash = calculate_hash(blockchain[i].index, blockchain[i - 1].hash, timestamp, data)
    block = Block(i + 1, blockchain[i - 1].hash, timestamp, data, hash)
    blockchain.append(block)
    previous_block = block

# Proof of Work
def proof_of_work(last_block):
    last_hash = last_block.hash
    timestamp = int(time.time())
    nonce = 0

    while True:
        value = str(last_block.index) + str(last_hash) + str(timestamp) + str(nonce)
        hash = hashlib.sha256(value.encode('utf-8')).hexdigest()
        if hash[:4] == "0000":
            return hash, nonce
        nonce += 1


# Mine a new block
def mine_block(block):
    last_block = blockchain[-1]
    last_hash = last_block.hash
    proof = proof_of_work(last_block)
    timestamp = int(time.time())
    data = f'Block #{block.index} has been mined!'
    hash = calculate_hash(block.index, last_hash, timestamp, data + proof[1])
    mined_block = Block(block.index + 1, last_hash, timestamp, data + proof[1], hash)
    blockchain.append(mined_block)


# Test proof of work
last_block = blockchain[-1]
proof = proof_of_work(last_block)
print(f'Proof of work: {proof[0]}, nonce: {proof[1]}')

# Mine a new block
mine_block(last_block)
print(f'Block #{blockchain[-1].index} has been mined!')
