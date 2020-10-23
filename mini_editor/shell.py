import os
import subprocess


def c_compile(data):
    with open("tmp.c", mode='w') as file:
        file.write(data)
    process = subprocess.Popen(["gcc", "tmp.c"]
                               , stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return process.returncode, output, error


def c_run(command):
    subprocess.call(command, shell=True)
