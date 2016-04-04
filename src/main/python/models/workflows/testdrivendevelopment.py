'''
Created on 1 Apr 2016

@author: Tim
'''
from models.systems.software.softwaresystem import SoftwareSystem

class TestDrivenDevelopment(object):


    def __init__(self,
                project_characteristics, 
                 project_schedule, 
                 target_tests_per_feature, 
                 target_refactorings_per_feature):

        self.target_tests_per_feature = target_tests_per_feature
        self.target_refactorings_per_feature = target_refactorings_per_feature

        self.software_system = SoftwareSystem(project_characteristics)

        for feature_size in project_schedule:
            self.software_system.add_feature(feature_size)


    def work(self, developer):
        
        for feature in self.software_system.features:
            while not feature.is_implemented:
                pass
                
                