#!/user/bin/env python
import yaml
import  json

def main():
    yaml_file = 'my_test.yml'
    json_file = 'my_test.json'

    my_dict = {
        'ip_addr': '10.10.10.10',
        'platform': 'cisco_ios'
    }

    my_list = [
        'some string',
        99,
        100,
        my_dict
    ]

    with open(yaml_file, "w") as f:
        f.write(yaml.dump(my_list, default_flow_style=False))

    with open(json_file, "w") as f:
        json.dump(my_list, f)

if __name__ == "__main__":
    main()


