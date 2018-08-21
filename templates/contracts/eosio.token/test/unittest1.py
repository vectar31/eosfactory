import sys
import unittest
import setup
import eosf
import time

from eosf import Verbosity
from eosf_wallet import Wallet
from eosf_account import account_create, account_master_create
from eosf_contract import Contract

logger.Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
logger.set_throw_error(False)

_ = logger.Logger()

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print('''

NEXT TEST ====================================================================
''')

    @classmethod
    def setUpClass(cls):
        print()

    def setUp(self):
        eosf.restart()
        logger.set_is_testing_errors(False)
        logger.set_throw_error(True)

    def test_eosio_token_contract(self):
        eosf.reset([logger.Verbosity.INFO]) 
        wallet = Wallet()
        account_master_create("account_master")
        logger.set_throw_error(False)
        logger.set_is_testing_errors()

        ######################################################################        

        _.SCENARIO('''
        With the master account, create four accounts: ``account_alice``, 
        ``account_bob``, account_carol`` and ``account_eosio_token``. Add the 
        ``eosio.token`` contract to the last account.
        ''')

        account_create("account_alice", account_master)
        account_create("account_bob", account_master)
        account_create("account_carol", account_master)
        account_create("account_eosio_token", account_master)
        contract_eosio_token = Contract(
            account_eosio_token, sys.path[0] + "/../")
        deploy = contract_eosio_token.deploy()

        time.sleep(1)

        _.COMMENT('''
        Execute actions on the contract account:
            * let eosio deposit an amount of 1000000000.0000 EOS there;
            * transfer some EOS to the ``alice`` account.
        ''')

        account_eosio_token.push_action(
            "create", 
            '{"issuer":"' 
                + str(account_master) 
                + '", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}')
                
        self.assertTrue(
            '"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS"' \
                in account_eosio_token.eosf_buffer)

        account_eosio_token.push_action(
            "issue",
            '{"to":"' + str(account_alice)
                + '", "quantity":"100.0000 EOS", '
                + '"memo":"issue 100.0000 EOS from eosio to alice"}',
            permission=account_master)

        _.COMMENT('''
        Execute a series of transfers between accounts:
        ''')

        account_eosio_token.push_action(
            "transfer",
            '{"from":"' + str(account_alice)
                + '", "to":"' + str(account_carol)
                + '", "quantity":"25.0000 EOS", '
                + '"memo":"transfer 25.0000 EOS from alice to carol"}',
            permission=account_alice)

        account_eosio_token.push_action(
            "transfer",
            '{"from":"' + str(account_carol)
                + '", "to":"' + str(account_bob)
                + '", "quantity":"11.0000 EOS", '
                + '"memo":"transfer 11.0000 EOS from carol to bob"}',
            permission=account_carol)

        account_eosio_token.push_action(
            "transfer",
            '{"from":"' + str(account_carol)
                + '", "to":"' + str(account_bob)
                + '", "quantity":"2.0000 EOS", '
                + '"memo":"transfer 2.0000 EOS from carol to bob"}',
            permission=account_carol)

        account_eosio_token.push_action(
            "transfer",
            '{"from":"' + str(account_bob)
                + '", "to":"' + str(account_alice)
                + '", "quantity":"2.0000 EOS", '
                + '"memo":"transfer 2.0000 EOS from bob to alice"}',
            permission=account_bob)                

        _.COMMENT('''
        See the records of the account:
        ''')

        table_alice = account_eosio_token.table("accounts", account_alice)
        table_bob = account_eosio_token.table("accounts", account_bob)
        table_carol = account_eosio_token.table("accounts", account_carol)

        _.COMMENT('''
        Check assertions:
        * assertEqual(table_alice.json["rows"][0]["balance"], '77.0000 EOS')
        * assertEqual(table_bob.json["rows"][0]["balance"], '11.0000 EOS')
        * assertEqual(table_carol.json["rows"][0]["balance"], '12.0000 EOS')
        ''')

        self.assertEqual(table_alice.json["rows"][0]["balance"], '77.0000 EOS')
        self.assertEqual(table_bob.json["rows"][0]["balance"], '11.0000 EOS')
        self.assertEqual(table_carol.json["rows"][0]["balance"], '12.0000 EOS')


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
