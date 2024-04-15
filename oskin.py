import sys,os

dn = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, dn)

import shutil
import zipfile

import click
import requests

from lib.project import REPO_ROOT

@click.group()
def cli():
    pass

def download_github_zip(url, output_path):
    # Send HTTP GET request
    response = requests.get(url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open a local file with write-binary mode
        with open(output_path, 'wb') as file:
            # Write the contents of the response (raw bytes) to the file
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Download complete: {output_path}")
    else:
        print("Failed to download file")

def unzip_file(zip_path, extract_to):
    # Check if the ZIP file exists
    if os.path.exists(zip_path):
        # Open the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all the contents into the directory
            zip_ref.extractall(extract_to)
        print(f"Unzipped files to: {extract_to}")
    else:
        print(f"No file found at {zip_path}")

@cli.command()
def fetch():
    if os.path.exists(os.path.join(REPO_ROOT, 'temp')):
        shutil.rmtree(os.path.join(REPO_ROOT, 'temp'))
    os.mkdir(os.path.join(REPO_ROOT, 'temp'))
    href="https://github.com/ppy/osu-resources/zipball/master/"
    download_github_zip(href, os.path.join(REPO_ROOT, 'temp', 'osu-resources.zip'))
    unzip_file(
        os.path.join(REPO_ROOT, 'temp', 'osu-resources.zip'),
        os.path.join(REPO_ROOT, 'temp', 'osu-resources')
    )
    d = os.path.join(REPO_ROOT, 'temp', 'osu-resources')
    file_list = list(os.listdir(d))
    while "osu.Game.Resources" not in file_list:
        print(d)
        for file in os.listdir(d):
            full_path = os.path.join(d, file)
            if os.path.isdir(full_path):
                d = full_path
                file_list = list(os.listdir(d))
                break
    d = os.path.join(d, "osu.Game.Resources")
    d = os.path.join(d, "Skins")
    d = os.path.join(d, "Legacy")
    if os.path.exists(os.path.join(REPO_ROOT, 'clean')):
        shutil.rmtree(os.path.join(REPO_ROOT, 'clean'))
    shutil.copytree(d, os.path.join(REPO_ROOT, 'clean'))
    shutil.rmtree(os.path.join(REPO_ROOT, 'temp'))



if __name__ == '__main__':
    cli()