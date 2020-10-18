import glob
import os
import subprocess
from pathlib import Path
import uuid
import shutil

def update_repos():
    task = subprocess.Popen(['ls', '|', 'xargs', '-I{}', 'git', '-C', '{}', 'pull'])
    task.wait()


def run_set_update():
    task = subprocess.Popen([ 'python3', 'nonRedundantRNASetDownload/main.py'], stdout=subprocess.PIPE)
    task.wait()

def run_rnapdbee():
    if not os.path.exists(Path('./dotbracket_files')):
        os.makedirs(Path('dotbracket_files'))
    temp_path = Path('/tmp/' + str(uuid.uuid4()))
    os.makedirs(temp_path)
    for files in glob.glob('PDB_files/*.cif'):
        files = Path(files)
        task = subprocess.Popen([ '/opt/rnapdbee-standalone-old/rnapdbee', '-i', files.absolute(), '-o', temp_path, '-a', 'DSSR'], stdout=subprocess.PIPE)
        task.wait()
        try:
            shutil.move(temp_path / '0' / 'strands.dbn','./dotbracket_files/' + files.stem + '-2D-dotbracket.dbn')
        except:
            f= open("log.txt","a+")
            f.write(str(files.absolute()) + "\n")
            f.close()

def dbn_cleaner():
    for file in glob.glob('dotbracket_files/*.dbn'):
        with open(file,"r") as dot_bracket_file:
            lines = dot_bracket_file.readlines()
            for line_number in range(len(lines)):
                if lines[line_number].startswith(">strand"):
                    dot_bracket_representation = lines[line_number + 2]
                    fragments_to_remove = [pos for pos, char in enumerate(dot_bracket_representation) if char == '-']
                    lines[line_number + 1] = "".join([char for idx, char in enumerate(lines[line_number + 1]) if idx not in fragments_to_remove])
                    lines[line_number + 2] = "".join([char for idx, char in enumerate(lines[line_number + 2]) if idx not in fragments_to_remove])
        clean_file = open(file, "w")
        clean_file.writelines(lines)
        clean_file.close()




def run_euler_angle_calculator():
    task = subprocess.Popen(['python3', 'nWayJunction_release/main.py'])
    task.wait()

if __name__ == "__main__":
    #update_repos()
    f= open("log.txt","w+")
    f.close()
    run_set_update()
    run_rnapdbee()
    dbn_cleaner()
    run_euler_angle_calculator()
