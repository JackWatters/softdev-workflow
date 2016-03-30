'''
Created on 14 Mar 2016

@author: tws
'''
import unittest
from models.systems.software.softwaresystem import SoftwareSystem
from random import Random
from models.systems.software.bug import BugEncounteredException
from models.systems.software.test import Test

class SoftwareSystemTest(unittest.TestCase):


    def setUp(self):
        self.software_system = SoftwareSystem()
        pass


    def tearDown(self):
        pass



    def complete_feature(self, random, size):
        feature = self.software_system.add_feature(size)
        while not feature.is_implemented():
            feature.extend(random)
        for _ in range (0, 30):
                self.software_system.add_test(feature)
 

    def test_operate_test_debug_operate_regression(self):
        
        my_random = Random()
        my_random.seed(1)
        
        for _ in range(0,2):
            self.complete_feature(my_random, 3)

        successful_operations = self.software_system.operate(my_random, 10000)
        self.assertEquals(0, successful_operations)
        #Ensures that tests are executed in pre-determined order for repeatability.
        ordered_tests = \
            sorted(list(self.software_system.tests), key=lambda t : t.id)

        for test in ordered_tests:
            test_failing = True

            while test_failing :
                try:
                    test.exercise()
                    test_failing = False
                except BugEncounteredException as e:
                    test.feature.debug(my_random, e.bug)

        successful_operations = self.software_system.operate(my_random, 10000)
        self.assertEquals(10000, successful_operations)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ChunkTest.testName']
    unittest.main()