from time import sleep
import json, os, copy, hashlib, datetime, random, threading

class Pionner:
    def __init__(self):
        self.pionner_wallet = input("Enter your wallet: ")
        self.main()
        
    def main(self):
        """
        Main function of Pionner
        """
        self.running = False
        self.thread_started = False

        trs = json.loads(open("data/transactions/pool.json", "r").read())

        if len(trs) <= 0:
            while True:
                #Get transactions from pool
                trs = json.loads(open("data/transactions/pool.json", "r").read())

                #Check if pool.json is not empty
                if len(trs) > 0:
                    self.running = False
                    os.system("cls")
                    break
                elif not self.thread_started:
                    self.thread_started = True
                    self.running = True
                    t1 = threading.Thread(target=self.text_info, args=("Waiting for transactions",1))
                    t1.start()

        self.reward = self.random_factor()
        self.text_info("Initiating Pionner")
        self.max_transactions = 5
        self.valid_transactions = []
        self.number_of_transactions = ""
        self.merkle_root_value = ""
        self.proof_of_work_value = ""
        self.previous_hash_value = ""
        self.hash_value = ""
        self.hash_object = hashlib.sha256()
        self.get_wallets()
       
    def random_factor(self) -> float:
        """
        Generate random factor
        """

        random_factor = random.uniform(0.7, 1.5)
        return random.uniform(3.2, 5.6) * random_factor

    def get_wallets(self):
        """
        Get wallets from wallets.json
        """

        #Get wallets from wallets.json
        self.wallets = json.loads(open("data/wallets/wallets.json", "r").read())

        self.get_data_from_pool()

    def get_data_from_pool(self):
        """
        Get transaction from pool
        """

        self.text_info("Getting data from pool")

        #Get data from pool
        self.transactions = json.loads(open("data/transactions/pool.json", "r").read())
        self.del_transaction = copy.deepcopy(self.transactions)

        sleep(3)
        print("Pool data retrieved !")

        #Check len of self.transactions
        if len(self.transactions) > 1:
            print(f"Pionner have get {len(self.transactions)} transactions in pool !")
        else:
            print(f"Pionner have get {len(self.transactions)} transaction in pool !")

        self.check_data_on_wallet()

    def check_data_on_wallet(self):
        """
        Check if transactions in self.transactions is valid
        """
        get_transactions = 0

        for data in self.transactions:
            #Increment get_transactions
            get_transactions += 1
            #Check if address of sender is in wallets
            if get_transactions <= self.max_transactions:
                #Delete transaction from pool
                self.delete_transaction(data)
                #Check if address of sender is in wallets
                if self.transactions[data]["sender"] in self.wallets:
                    #Check if address of receiver is in wallets
                    if self.transactions[data]["receiver"] in self.wallets:
                        #Check if amount is egal or superior to balance of sender
                        if self.transactions[data]["amount"] <= self.wallets[self.transactions[data]["sender"]]["balance"]:
                            #Add transaction to valid_transactions
                            self.valid_transactions.append(self.transactions[data])
        
        if len(self.valid_transactions) > 0:
            self.get_transactions()
            
    def delete_transaction(self, transaction_id):
        """
        Delete getted transactions from pool
        """
        
        del self.del_transaction[transaction_id]
            
        json.dump(self.del_transaction, open("data/transactions/pool.json", "w"), indent=2)

    def get_transactions(self):
        """
        Get all transactions in valid_transactions
        """

        #Get number of valid transactions
        self.number_of_transactions = len(self.valid_transactions)

        self.merkle_root()

    def merkle_root(self):
        """
        Hash of all transactions in self.transactions
        """
        
        #Value to all information of transactions and previous hash
        value = ""

        #Add all transactions to value
        for data in self.valid_transactions:
            value += str(data)
        
        #Hash value
        self.hash_object.update(value.encode())
        #Get merkle root value
        self.merkle_root_value = self.hash_object.hexdigest()

        self.get_previous_hash()

    def get_previous_hash(self):
        """
        Get previous hash
        """

        #Get all information of blockchain
        blockchain = json.loads(open("data/blockchain/blockchain.json", "r").read())

        #Get previous hash
        previous_hash = max(blockchain.keys())
        
        #Add previous hash to value
        self.previous_hash_value = str(blockchain[previous_hash]["hash"])

        self.proof_of_work()

    def proof_of_work(self):
        """
        Calculate proof of work
        """

        print("Calculating proof of work")

        #Initialise difficulty
        difficulty = ""
        #Initialise nonce
        nonce = 0
        #Get difficulty value
        difficulty_value = open("data/blockchain/difficulty.dat", "r").read()

        #Add "0" * difficulty_value to difficulty
        for i in range(int(difficulty_value)):
            difficulty += "0"

        while True:
            data_with_nonce = self.merkle_root_value + str(nonce)
            
            hash_result = hashlib.sha256(data_with_nonce.encode()).hexdigest()

            if hash_result[:int(difficulty_value)] == "0" * int(difficulty_value):
                self.proof_of_work_value = hash_result
                self.hash()
                self.running = False
                return
        
            nonce += 1

    def hash(self):
        """
        Hash of merkle root, previous block hash, proof of work and timestamp
        """

        #Get timestamp
        timestamp = datetime.datetime.now()
        
        #Generate hash value of block
        print(self.merkle_root_value + self.previous_hash_value + self.proof_of_work_value + str(self.number_of_transactions) + str(timestamp))
        self.hash_value = hashlib.sha256((self.merkle_root_value + self.previous_hash_value + self.proof_of_work_value + str(self.number_of_transactions) + str(timestamp)).encode()).hexdigest()
        self.add_block()

    def add_block(self):
        """
        Add block to blockchain
        """

        #Get blockchain data
        blockchain = json.loads(open("data/blockchain/blockchain.json", "r").read())

        #Add block to blockchain
        blockchain[len(blockchain) + 1] = {"hash":self.hash_value, "merkle_root":self.merkle_root_value,"proof_of_work":self.proof_of_work_value, "previous_hash":self.previous_hash_value, "number_of_transactions":self.number_of_transactions, "timestamp":str(datetime.datetime.now())}

        #Update blockchain.json
        json.dump(blockchain, open("data/blockchain/blockchain.json", "w"), indent=2)


        if len(blockchain) % 1 == 0:
            difficulty_value = open("data/blockchain/difficulty.dat", "r").read()

            difficulty_value = int(difficulty_value) + 1

            open("data/blockchain/difficulty.dat", "w").write(str(difficulty_value))

        self.transfer_money()

    def transfer_money(self):
        """
        Transfer money from sender to receiver
        """

        #Get sender wallet
        for transaction in self.valid_transactions:
            #Get sender wallet
            sender_wallet = transaction["sender"]
            #Get receiver wallet
            reciever_wallet = transaction["receiver"]
            #Get amount to send
            amount_to_send = transaction["amount"]

            #Substract amount to send to sender wallet
            self.wallets[sender_wallet]["balance"] -= amount_to_send
            #Add amount to send to receiver wallet
            self.wallets[reciever_wallet]["balance"] += amount_to_send

            #Update wallets.json
            json.dump(self.wallets, open("data/wallets/wallets.json", "w"), indent=2)

        self.give_reward()

    def give_reward(self):
        """
        Give reward to pionner
        """

        #Try to add reward to pionner wallet
        try:
            self.wallets[self.pionner_wallet]["balance"] += self.reward

            #Update wallets.json
            json.dump(self.wallets, open("data/wallets/wallets.json", "w"), indent=2)
            print(f"Block {self.hash_value} added !")
            print("Your reward is: " + str(self.reward) + " !")

            sleep(5)
            self.main()
        except:
            pass

    def text_info(self, text, way=0):
        """
        Display text with time
        """
        if way == 0:
            self.running = True

        while self.running:
            for i in range(3):
                os.system("cls")
                text += "."
                print(text)
                sleep(1)
            text = text[:-3]

            if way == 0:
                self.running = False

        self.thread_started = False

if __name__ == "__main__":
    pionner = Pionner()