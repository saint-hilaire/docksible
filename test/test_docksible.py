import unittest
from docksible.docksible import Docksible


#######################################################
# TODO: Unit tests would be really cool.
# But it's a little difficult, because we need to mock
# some kind of server against which Docksible can run.
#######################################################

class TestDocksible(unittest.TestCase):

    def setUp(self):
        self.docksible = Docksible(
            user='user',
            host='localhost',
            action='wordpress',
            private_data_dir=os.path.join(
                'test',
                'tmp-private-data',
            )
        )


    def tearDown(self):
        self.docksible.cleanup_private_data()
