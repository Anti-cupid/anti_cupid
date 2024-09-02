import yaml

def read_yaml(yaml_path:str)->dict:
    with open(yaml_path, encoding='UTF8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_data


