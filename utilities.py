import os
import shutil
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def download_file(url, save_path):
    r = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(r.content)


def download_multiple(urls, save_folder, prefix):
    for idx, url in enumerate(urls):
        # Parse the URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        # Get the filename from the path
        filename = os.path.basename(path)
        # Split the filename into its root and extension
        root, ext = os.path.splitext(filename)

        download_file(url, f'{save_folder}/{prefix}-{idx}{ext}')


def collect_links(page_links, target_selector, target_property):
    elements = []
    for link in page_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        targets = soup.select(target_selector)
        # print(len(targets))
        for target in targets:
            elements.append(target[target_property])
    return elements


def valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return


def create_folder(folder_path):
    del_copy_cmd = f'rm -rf {folder_path}'
    subprocess.run(del_copy_cmd.split())

    results_folder = os.path.join(folder_path, 'results')
    os.makedirs(results_folder, exist_ok=True)
    return results_folder


def copy_folder(src, dest):
    shutil.copytree(src, dest, symlinks=False, dirs_exist_ok=True)


def run_jadoogar(input_folder, opt_args):
    run_cmd = f'python run.py --inputs {input_folder} ' + opt_args
    subprocess.run(run_cmd.split())
