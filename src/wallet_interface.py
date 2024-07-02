import sys, json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QLineEdit, QLabel
from PyQt5 import uic

#Local imports
import generator_wallets.wallet_address_generation as wallet_generate
import transactions.pool as pool

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        #Load File gui
        uic.loadUi("gui/wallet.ui", self)
        
        #Widgets
        #Main
        self.stackwidget = self.findChild(QStackedWidget, "stackedWidget")
        #Login window
        self.go_btn = self.findChild(QPushButton, "pushButton")
        self.new_wallet_btn = self.findChild(QPushButton, "pushButton_4")
        self.wallet_address = self.findChild(QLineEdit, "lineEdit")
        
        #Wallet window
        self.display_wallet_address = self.findChild(QLabel, "label_2")
        self.wallet_balance = self.findChild(QLabel, "label_5")
        self.copy_btn = self.findChild(QPushButton, "pushButton_2")
        self.send_money_btn = self.findChild(QPushButton, "pushButton_3")
        self.other_wallet_address = self.findChild(QLineEdit, "lineEdit_2")
        self.amount_to_send = self.findChild(QLineEdit, "lineEdit_3")
        self.back_btn = self.findChild(QPushButton, "pushButton_5")
        
        #Initialisation
        self.stackwidget.setCurrentIndex(0)
        self.go_btn.clicked.connect(self.go_to_wallet)
        self.new_wallet_btn.clicked.connect(self.new_wallet)
        self.copy_btn.clicked.connect(self.copy_wallet_address)
        self.send_money_btn.clicked.connect(self.send_money)
        self.back_btn.clicked.connect(lambda: self.stackwidget.setCurrentIndex(0))
        
        #Show App
        self.show()
    
    #Go to wallet
    def go_to_wallet(self) -> None:
        """
        Go to wallet window if wallet exists
        """

        #If wallet address is not empty
        if self.wallet_address.text() != "":
            #If wallet exists
            if self.check_wallet(self.wallet_address.text()):
                #Change window
                self.stackwidget.setCurrentIndex(1)

                #Display address wallet
                self.display_wallet_address.setText(self.wallet_address.text())
                
                #Display wallet balance
                wallets = json.loads(open("./data/wallets/wallets.json", "r").read())
                    
                #Display wallet balance
                self.wallet_balance.setText(str(wallets[self.wallet_address.text()]["balance"]))
           
    #Generate new wallet
    def new_wallet(self) -> None:
        """
        Generate new wallet and display it
        """
        #Generate new wallet from wallet_address_generation.py
        wallet = wallet_generate.generate_wallet(wallet_generate.alphabet_lower, wallet_generate.alphabet_upper, wallet_generate.number)
        self.wallet_address.setText(wallet)

    #Check if wallet exists
    def check_wallet(self, address) -> list:
        """
        If wallet exists in wallets.json, return True and wallet address
        """
        #Read wallets.json
        wallets = open("./data/wallets/wallets.json", "r").read()
        
        #If wallet address exists in wallets.json
        if address in wallets:
            return True
            
    def copy_wallet_address(self):
        """
        Copy wallet address to clipboard
        """
        self.wallet_address.selectAll()
        self.wallet_address.copy()
        
    def send_money(self):
        """
        Send money to another wallet
        """

        #Get wallet data
        wallets = json.loads(open("./data/wallets/wallets.json", "r").read())
                
        #If wallet address is not empty and is not the wallet address of the sender
        if self.other_wallet_address.text() != "" and self.other_wallet_address.text() != self.wallet_address.text():
            #If wallet exists
            if self.check_wallet(self.other_wallet_address.text()):
                #If amount to send is not empty
                if self.amount_to_send.text() != "":
                    #If amount to send is superior to 0
                    if float(self.amount_to_send.text()) > 0 and float(self.amount_to_send.text()) <= wallets[self.wallet_address.text()]["balance"]:
                        pool.add_transaction_to_pool(self.wallet_address.text(), self.other_wallet_address.text(), float(self.amount_to_send.text()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())  