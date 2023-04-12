import os
from threading import Thread
from preview_generator.manager import PreviewManager


def get_thumbnail(file, cache_path, basename_dir):
    filename = basename_dir + file['id']
    manager = PreviewManager(cache_path, create_folder=True)
    path_to_preview_image = manager.get_jpeg_preview(filename)
    name_of_file = os.path.basename(path_to_preview_image)
    file['thumbnail'] = 'tmp/' + name_of_file


class Worker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            file, cache_path, basename_dir = self.queue.get()
            try:
                get_thumbnail(file, cache_path, basename_dir)
            finally:
                self.queue.task_done()
