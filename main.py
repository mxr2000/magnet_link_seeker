import sys
from typing import List, Tuple

import requests
import re


def find_links(code: str) -> List[str]:
    url = "https://btsow.bar/search?keyword=" + code
    content = requests.get(url).text
    pattern = re.compile(r'btsow.bar/magnet/detail/hash/\w+(?=\")')
    return re.findall(pattern, content)


def find_files(link: str) -> Tuple[str, List[Tuple[str, str]]]:
    content = requests.get("https://" + link).text
    file_name_pattern = re.compile(r'(?<=</span>\s).+(?=</div><div\sclass=)')
    file_size_pattern = re.compile(r'(?<=text-right\ssize\">)[\d.MKGB]+(?=</div>)')
    magnet_pattern = re.compile(r'magnet:\?xt[\w:=&-_]+(?=</textarea>)')
    file_names = re.findall(file_name_pattern, content)
    file_sizes = re.findall(file_size_pattern, content)
    magnet = re.findall(magnet_pattern, content)[0]
    files = []
    for i in range(len(file_names)):
        files.append((file_names[i], file_sizes[i]))

    return magnet, files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("not enough arguments")
        exit(1)
    for link in find_links(sys.argv[1]):
        magnet, files = find_files(link)
        print(magnet)
        for file in files:
            print("\t{:10}{:10}".format(file[1], file[0]))
