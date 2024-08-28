import argparse

def get_args()->argparse:
    parser = argparse.ArgumentParser(description="Data crawling for specific URL.")
    parser.add_argument("--yaml", default="./yaml/data_crawling.yaml")
    args = parser.parse_args()
    return args