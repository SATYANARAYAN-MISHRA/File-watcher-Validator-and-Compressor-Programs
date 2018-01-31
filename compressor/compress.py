import sched
import time
import os, tarfile
import hashlib


scheduler = sched.scheduler(time.time, time.sleep)

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def compress(name):

    #get all list new files from db if not compressed
    for file_ in os.listdir('compreesdfile'):
        md5 = hashlib.md5(file_).hexdigest()
        print md5
        make_tarfile(file_+".tar.gz","compreesdfile/"+file_)
        

while (1):
    scheduler.enter(2, 2, compress, ('first',))
    scheduler.run()
