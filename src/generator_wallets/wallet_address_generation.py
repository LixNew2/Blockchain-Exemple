import random, json

alphabet_lower = "abcdefghijkmnopqrstuvwxyz"
alphabet_upper = "ABCDEFGHJKLMNPQRSTUVWXYZ"
number = "123456789"

def generate_wallet(lower, upper, num):
    wallet = ""

    while len(wallet) < 34:
        random_int = random.randint(0, 2)

        if random_int == 0:
            wallet += "".join(random.choice(lower))
        elif random_int== 1:
            wallet += "".join(random.choice(upper))
        else:
            wallet += "".join(random.choice(num))

    data = json.loads(open("./data/wallets/wallets.json", "r").read())
    data[wallet] = {"balance": 0} 
    json.dump(data, open("./data/wallets/wallets.json", "w"))

    return wallet

if __name__ == "__main__":
    generate_wallet(alphabet_lower, alphabet_upper, number)