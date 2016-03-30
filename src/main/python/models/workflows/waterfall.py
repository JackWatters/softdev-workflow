'''
Created on 23 Mar 2016

@author: Tim
'''
from models.systems.software.softwaresystem import SoftwareSystem


class MyClass(object):
    '''
    classdocs
    '''

    def __init__(self, project_schedule):
        self.software_system = SoftwareSystem()
        for feature_size in project_schedule:
            self.software_system.add_feature(feature_size)


    def work(self, resources):
        features = self.software_system.features
        
        for feature in features:
            if not feature.is_implemented:



    def deliver (self):
        return self.software_system