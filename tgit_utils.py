"""
Invoke useful TortoiseGit GUI windows from Sublime Text

By Scott Stafford, https://github.com/ses4j
"""

import os
import time
import sublime

import subprocess

git_root_cache = {}
def git_root(directory):
    """ This method lifted from https://github.com/kemayo/sublime-text-git """
    global git_root_cache

    retval = False
    leaf_dir = directory

    if leaf_dir in git_root_cache and git_root_cache[leaf_dir]['expires'] > time.time():
        return git_root_cache[leaf_dir]['retval']

    while directory:
        if os.path.exists(os.path.join(directory, '.git')):
            retval = directory
            break
        parent = os.path.realpath(os.path.join(directory, os.path.pardir))
        if parent == directory:
            # /.. == /
            retval = False
            break
        directory = parent

    git_root_cache[leaf_dir] = {
        'retval': retval,
        'expires': time.time() + 5
    }

    return retval

def is_git_controlled(directory):
    return bool(git_root(directory))

def run_tortoise_git_command(command, args, path):
    settings = sublime.load_settings('TortoiseGit Context Integration.sublime-settings')
    tortoisegit_path = settings.get('tortoisegit_path')

    if tortoisegit_path is None or not os.path.isfile(tortoisegit_path):
        tortoisegit_path = 'TortoiseGitProc.exe'

    cmd = u'{0} /command:"{1}" /path:"{2}" {3}'.format(
        tortoisegit_path, 
        command,
        path, 
        u" ".join(args))

    try:
        print("Running {0}".format(cmd))
        with open(os.devnull, 'w') as devnull:
            proc = subprocess.Popen(cmd, 
                stdin=devnull, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False, 
                creationflags=subprocess.SW_HIDE)
    except IOError as ex:
        sublime.error_message("Failed to execute command: {}".format(
            str(ex)))
        raise
