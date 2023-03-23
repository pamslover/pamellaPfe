from flask import Flask, request
import os
import subprocess

app = Flask(__name__)
dataset_path = '/data/AllProjectIA/pamella/dataset/'
paths = []


@app.route("/api/folders")
@app.route("/api/folders/<parent_dir>")
def list_directory(parent_dir=None):
    global paths
    if parent_dir is None:
        parent_dir = dataset_path
    paths = []
    get_liste_of_directory(parent_dir)
    return list(map(to_array_folder, ['/'.join(path.split('/')[5:]) for path in paths]))


@app.route("/api/files")
def list_files():
    args = request.args
    folder = args.get('folder')

    if folder is not None:
        path = '/data/AllProjectIA/pamella/dataset/' + folder
    else:
        path = '/data/AllProjectIA/pamella/dataset'
    response = command_ls_files(path)
    print(response['data'])
    return list(map(to_array_files,  ['/'.join(path.split('/')[4:]) for path in response['data']]))


def to_array_folder(folder):
    tmp = os.path.dirname(folder)
    name = os.path.basename(tmp)
    parent = os.path.basename(os.path.dirname(tmp))
    return {
        'id': tmp,
        'name': name,
        'parent': parent if parent != '' else None
    }


def to_array_files(folder):
    name = os.path.basename(folder)
    parent = os.path.basename(os.path.dirname(folder))
    return {
        'id': folder,
        'name': name,
        'url': '',
        'folder': parent if parent != '' else None

    }


def get_liste_of_directory(path_directory):
    global paths
    currentDir = ''
    r = command_ls(path_directory)
    if r['error'] == '':
        paths += r['data']
        for element in r['data']:
            get_liste_of_directory(element)


def command_ls(path):
    command = f'cd {path} && ls -1 -dX */'
    response = subprocess.run(command, capture_output=True, shell=True)
    if response.stderr.decode() != '':
        return {"data": "", "error": response.stderr.decode()}
    if response.stdout.decode() != '':
        elements = response.stdout.decode().split('\n')
        return {"data": ['/'.join(path.split('/')[:-1]) + f'/{element}' for element in elements][:-1], "error": ''}


def command_ls_files(path):
    command = f'cd {path} && ls -l | grep -v \'^\'d | tr -s \' \' | cut -d \' \' -f9'
    response = subprocess.run(command, capture_output=True, shell=True)
    if response.stderr.decode() != '':
        return {"data": "", "error": response.stderr.decode()}
    if response.stdout.decode() != '':
        elements = response.stdout.decode().strip().split('\n')
        print(elements)
        return {"data": ['/'.join(path.split('/')) + f'/{element}' for element in elements], "error": ''}


if __name__ == "__main__":
    app.run(debug=True)
