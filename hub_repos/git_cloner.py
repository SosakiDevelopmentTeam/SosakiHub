from git import Repo, Remote
from os.path import join, isdir
import os, shutil

class ByondRepo:

    def __init__(self, name, branch = 'master', link=None):
        self.path = join(os.environ["WORKING_DIR"], name)
        self.repo = None

        if link and not isdir(self.path):
            self.repo = Repo.clone_from(link, self.path, branch=branch, depth=1, j=4)
        else:
            self.repo = Repo(self.path)

        if not self.is_byond():
            self.remove_repo()
            raise Exception("Not BYOND repo")

    def is_byond(self):
        for file in os.listdir(self.path):
            if file.endswith(".dme"):
                return True
        return False

    def remove_repo(self):
        if isdir(self.path):
            shutil.rmtree(self.path)

    def change_branch(self, name):
        assert name in self.repo.branches
        self.repo.active_branch.checkout(name)

    def pull(self):
        remote  = self.repo.remotes[self.repo.active_branch.remote_name]
        remote.pull()

