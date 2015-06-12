# Convert all files in arg[1] dir to mp3 format into arg[2] dir

__author__ = 'alex'

import sys
import os
import subprocess


def usage():
    return """Not enough parameters.
Use: python converter.py /dir/with/sources /output/dir"""

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def convert():
    if len(sys.argv) < 3:
        pass
        print(usage())
        exit(1)

    cmd = which('ffmpeg')

    if not cmd:
        print("FFMPEG not found on your system. Install it first")
        exit(1)

    indir = sys.argv[1]
    outdir = sys.argv[2]

    if not os.path.exists(indir):
        print("Input directory doesn't exist.")
        exit(1)

    try:
        for file in os.listdir(indir):
            if file.startswith('.'):
                continue

            if not os.path.exists(outdir):
                os.makedirs(outdir)


            input_file = os.path.join(indir, file)
            output_file = os.path.join(outdir, os.path.splitext(file)[0] + '.mp3')

            command = [cmd, '-y', '-v', '0',
                            '-i', input_file,
                            '-c:a', 'libmp3lame',
                            '-ab', '256k', output_file]

            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.stdout.readline()
            p.terminate()

    except Exception as e:
        print("Error: {}".format(e))
        exit(1)

if __name__ == "__main__":
    convert()
