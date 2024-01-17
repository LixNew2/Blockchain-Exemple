import json

def add_transaction_to_pool(sender, receiver, amount):
    """
    Add transaction to pool
    """

    #get data from pool.json
    pool = json.loads(open("data/transactions/pool.json", "r").read())
    #get number of transactions
    data_transactions = open("data/transactions/transactions.dat", "r").read()
    
    #add transaction to pool
    pool[int(data_transactions) + 1] = {"sender": sender, "receiver": receiver, "amount": amount}
    json.dump(pool, open("data/transactions/pool.json", "w"), indent=2)

    #increment number of transactions
    with open("data/transactions/transactions.dat", "w") as dat:
        dat.write(str(int(data_transactions) + 1))