import subprocess


def get_N50(path):
    """ Find N50 value of assembly. """
    process = subprocess.Popen(['fastainfo', path], stdout=subprocess.PIPE)
    out = process.communicate()
    out = out[0].splitlines()
    for line in out:
        if line[0:3] == 'N50':
            N50 = line[5:]

    return N50
