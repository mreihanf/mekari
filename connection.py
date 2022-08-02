# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:11:00 2022

@author: investree
"""

import sqlalchemy as db
import pandas as pd
from configparser import ConfigParser

class Engine:

    
    def __init__(self,config_path,db_type,sql_type):
        #Initialize config parameters for engine
        self.cfg = ConfigParser()
        self.cfg.read(config_path)
        self.sql_type = sql_type
        self.user = self.cfg.get(db_type,'user')
        self.password = self.cfg.get(db_type,'password')
        self.host = self.cfg.get(db_type,'host')
        self.port = self.cfg.get(db_type,'port')
        self.database = self.cfg.get(db_type,'database_name')
      
    def get_engine(self):
        #Create database engine
        return db.create_engine(self.sql_type+"://{}:{}@{}:{}/{}".format(self.user, self.password, self.host, self.port, self.database))
    
    