'''
@author: tws
'''
import unittest
from mock import Mock
from random import Random

from models.systems.software.chunk import Chunk
from models.systems.software.feature import Feature
from sets import Set
from models.systems.software.softwaresystem import SoftwareSystem
from models.systems.software.bug import BugEncounteredException

class ChunkTest(unittest.TestCase):


    def setUp(self):
        '''
        Mocks a single feature system and gives it two chunks.
        '''

        feature_mock = Mock(spec=Feature)
        
        self.fixture_chunks = []
        
        feature_mock.chunks = Set()
        feature_mock.software_system = Mock(spec=SoftwareSystem)
        feature_mock.software_system.chunks = feature_mock.chunks
        
        self.fixture_chunks.append(Chunk(feature_mock))
        self.fixture_chunks.append(Chunk(feature_mock))
        
        feature_mock.chunks.union_update(Set(self.fixture_chunks))


    def tearDown(self):
        pass


    def test_modify_create_bug(self):
    
        random_mock = Mock(spec=Random)
        random_mock.random = Mock(side_effect=[1.0, 0.5, 0.51])        

        self.fixture_chunks[0].modify(random_mock)
        
        self.assertEqual(1, len(self.fixture_chunks[0].bugs), "Unexpected number of bugs")
    
    
    def test_modify_create_dependency(self):
    
        random_mock = Mock(spec=Random)
        random_mock.random = Mock(side_effect=[0.1, 0.51])        

        self.fixture_chunks[0].modify(random_mock)
        
        self.assertEqual(1, len(self.fixture_chunks[0].dependencies))


    def test_refactor(self):
        
        random_mock = Mock(spec=Random)
        random_mock.random = Mock(side_effect=[0.1, 0.51, 0.05])  
              
        self.fixture_chunks[0].modify(random_mock)
        self.fixture_chunks[0].refactor(random_mock)
        self.assertEqual(0, len(self.fixture_chunks[0].dependencies))
        
        
    def test_debug(self):

        random_mock = Mock(spec=Random)        
        
        random_mock.random = Mock(side_effect=[0.1, 0.49, 0.51])        
        self.fixture_chunks[0].modify(random_mock)
        
        random_mock.choice = Mock (side_effect=[next(iter(self.fixture_chunks[0].bugs))])
        random_mock.random = Mock(side_effect=[0.001])
        
        self.fixture_chunks[0].debug(random_mock)

        self.assertEqual(len(self.fixture_chunks[0].bugs), 0)


    def test_operate_bug_not_manifest (self):
        
        random_mock = Mock(spec=Random)

        random_mock.random = Mock(side_effect=[0.1, 0.49, 0.51])
        self.fixture_chunks[0].modify(random_mock)
        
        random_mock.random= Mock(side_effect=[0.11])   
        self.fixture_chunks[0].operate(random_mock)


    def test_operate_bug_manifest (self):
        
        random_mock = Mock(spec=Random)

        random_mock.random = Mock(side_effect=[0.1, 0.49, 0.51, 0.1])        
        self.fixture_chunks[0].modify(random_mock)
        with self.assertRaises(BugEncounteredException):
            self.fixture_chunks[0].operate(random_mock)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()
