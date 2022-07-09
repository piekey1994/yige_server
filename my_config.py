import yaml
import os
os_dict=os.environ

class MyConfig(object):
    def __init__(self,path):
        with open(path,'r',encoding='utf-8') as f:
            self.config=yaml.load(f)
    def get_conf(self,index,key,type=None):
        value=os_dict.get('{}_{}'.format(index,key),self.config[index][key])
        if type is not None and not isinstance(value,type):
            if type==bool:
                if value=='True':
                    return True
                else:
                    return False
            elif type==list:
                values=value.split(',')
                return values
            else:
                return type(value)
        else:
            return value
    def __getitem__(self,item):
        return self.config[item]

default_config=MyConfig(os_dict.get('conf_path','conf/config.yaml'))
# default_config=config_model.config