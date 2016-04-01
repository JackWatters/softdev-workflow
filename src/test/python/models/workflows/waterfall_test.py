'''
Created on 30 Mar 2016

@author: Tim
'''
import unittest
from models.workflows.waterfall import Waterfall
from random import Random


class Test(unittest.TestCase):

    def setUp(self):
        self.workflow = Waterfall(
                project_characteristics = 
                {
                 'gain_feature_dependency' : 0.5,
                 'gain_system_dependency' : 0.1,
                 'lose_feature_dependency' : 0.25,
                 'lose_system_dependency' : 0.25,
                 'new_bug' : 0.5,
                 'debug_known' : 0.9,
                 'debug_unknown' : 0.01,
                 'detection' : 0.5,
                 'coverage' : 0.5,
                 'failure_on_demand' : 0.01
                },
                project_schedule=[3,5,7],
                target_tests_per_feature=2.5,
                target_refactorings_per_feature = 20
        )
        pass
    
    
    def test_implement_system_and_operate_regression(self):

        random = Random()
        random.seed(1)
        self.workflow.work(random, None)
        
        software_system = self.workflow.deliver()
        
        successful_operations = software_system.operate(random,10000)
        self.assertEquals(70, len(successful_operations))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()