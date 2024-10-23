import re
import sys


def read_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()
    
    
def convert_to_webgl(file_path):
    content = read_file(file_path)
    test_find = re.findall(r"Runtime\.dynCall\(\"(\w+)\",(\w+),\[(.*?)\]\)", content)
    content = fix_bug(content)
    if not test_find:
        print('No matches found')
        return content
    content = re.sub(r"Runtime\.dynCall\(\"(\w+)\",(\w+),\[(.*?)\]\)", r"Module['dynCall_\1'](\2,\3)", content)
    save_file(file_path.replace('.js', '_old.js'), content)
    return content


def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def fix_bug(content):
    wr_line = "var wr={requestInstances:{},nextRequestId:1,loglevel:2,responses:{},timer:{},requests:{},abortControllers:{}};"
    content = content.replace("var wr={requestInstances:{},nextRequestId:1,loglevel:2};", wr_line)
    
    return content
        
def main(file_path):
    content = convert_to_webgl(file_path)
    save_file(file_path, content)
    
if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != '-f':
        print('Invalid command line arguments. Usage: python convert.py -f [file_name]')
        sys.exit(1)
        
    file_name = sys.argv[2]
    main(file_name)