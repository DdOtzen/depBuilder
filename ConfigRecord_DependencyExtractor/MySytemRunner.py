import os
import subprocess
import sys
 
def run(cmd):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
							shell = True,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True,
                            )
    while proc.poll() is None:
        line = proc.stdout.readline()
        if line != "":
            print(line, end='')
 
        line = proc.stderr.readline()
        if line != "":
            print(line, end='', file=sys.stderr)
 
    return proc.returncode
 
 
