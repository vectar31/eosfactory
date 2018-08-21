import os
import unittest
import setup
import eosf

from eosf import Verbosity
from eosf_wallet import Wallet

logger.Logger.verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
logger.set_throw_error(False)

remote_testnet = "http://88.99.97.30:38888"
_ = logger.Logger()

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)
        print('''

NEXT TEST ====================================================================
''')

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        logger.set_is_testing_errors(False)
        logger.set_throw_error(True)

    def test_create_keosd_wallet(self):
        _.SCENARIO('''
Test creation of a wallet under the KEOSD Wallet Manager.
Set-up: 
    * delete existing, if any, wallet named ``jungle_wallet`` using
        a general procedure as the EOSFactory does not have any;
    * set KEOSD as the Wallet Manager;
    * set the URL of a remote testnet;
    * stop the KEOSD Wallet Manager.
Tests:
    * create a wallet named ``jungle_wallet``;
        Expected result is that a password message is printed.
        ''')        
        wallet_name = "jungle_wallet"
        try:
            os.remove(eosf.wallet_dir() + wallet_name + ".wallet")
        except:
            pass
        logger.set_throw_error(False)
        logger.set_is_testing_errors()
        setup.set_nodeos_address(remote_testnet)
        ######################################################################

        wallet = Wallet(wallet_name)
        self.assertTrue("keys will not be retrievable." in wallet.out_buffer )

        _.COMMENT("wallet.index()")
        wallet.index()

        _.COMMENT(" wallet.open()")
        wallet.open()

        _.COMMENT("wallet.lock()")
        wallet.lock()

        _.COMMENT("wallet.lock_all()")
        wallet.lock_all()

        _.COMMENT("wallet.unlock()")
        wallet.unlock()

        _.COMMENT("wallet.keys()")
        wallet.keys()



    # def test_reopen_with_stored_password(self): 
    #     eosf.reset([logger.Verbosity.INFO])
    #     eosf.Wallet()
    #     eosf.stop(is_verbose=0)
    #     eosf.run(is_verbose=0)
        
    #     wallet = eosf.Wallet()
    #     self.assertTrue(wallet.error)


    # def test_invalid_password(self): 
    #     eosf.reset([logger.Verbosity.INFO])
    #     wallet = eosf.Wallet()
    #     eosf.stop(is_verbose=0)
    #     eosf.run(is_verbose=0)        
        
    #     wallet = eosf.Wallet(
    #         None, "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")
    #     self.assertTrue(wallet.error)


    # def test_is_not_running_not_keosd_set(self):
    #     eosf.stop(is_verbose=0)
        
    #     wallet = eosf.Wallet()
    #     self.assertTrue(wallet.error)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()


