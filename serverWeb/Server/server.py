from flask import Flask, request
from preview_generator.manager import PreviewManager
from queue import Queue
from worker import Worker
import os
import subprocess

app = Flask(__name__)
dataset_path = '/data/AllProjectIA/pamella/dataset/'
base_name_dir = '/data/AllProjectIA/pamella/'
cache_path = '/data/AllProjectIA/pamella/serverWeb/dist/tmp'
count = 0
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
    print('folders')

    if folder is not None:
        path = '/data/AllProjectIA/pamella/dataset/' + folder
    else:
        path = '/data/AllProjectIA/pamella/dataset'
    response = command_ls_files(path)
    response = list(map(to_array_files, ['/'.join(path.split('/')[4:]) for path in response['data']]))
    queue = Queue()
    for x in range(12):
        worker = Worker(queue)
        worker.daemon = True
        worker.start()
    for file in response:
        queue.put((file, cache_path, base_name_dir))
    queue.join()
    return response


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
    global count
    name = os.path.basename(folder)
    parent = os.path.basename(os.path.dirname(folder))
    return {
        'id': folder,
        'name': name,
        'folder': parent if parent != '' else None,
        'thumbnail': 'assets/images/android-chrome-192x192.png'
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


def files_filter(files: list, extensions: list):
    response = []
    for file in files:
        file_split = str(file).split('.')
        extension = file_split[1] if len(file_split) > 1 else None
        if extension is not None and (extension in extensions):
            response.append(file)
    return response


def command_ls_files(path):
    command = f'cd {path} && ls -l | grep -v \'^\'d | tr -s \' \' | cut -d \' \' -f9'
    response = subprocess.run(command, capture_output=True, shell=True)
    if response.stderr.decode() != '':
        return {"data": "", "error": response.stderr.decode()}
    if response.stdout.decode() != '':
        elements = response.stdout.decode().strip().split('\n')
        elements = files_filter(elements, ['pdf', 'txt', 'docx'])
        print(f'array returned is: {elements}')
        return {"data": ['/'.join(path.split('/')) + f'/{element}' for element in elements], "error": ''}


def get_thumbnail(filename, size):
    manager = PreviewManager(cache_path, create_folder=True)
    path_to_preview_image = manager.get_jpeg_preview(filename)
    return path_to_preview_image


if __name__ == "__main__":
    app.run(debug=True)
