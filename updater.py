import os
from utils.git_api import run_git_command

class Updater:
    def __init__(self, version_file='version.txt', remote='origin'):
        self.version_file = version_file
        self.remote = remote
        self.current_version = self.get_current_version()

    def get_current_version(self):
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return "0.0.0"

    def get_latest_version(self, branch='main', file_path='version'):
        return run_git_command(['git', 'show', f'{self.remote}/{branch}:{file_path}'])

    def is_update_available(self):
        from utils.version import Version
        latest_version = self.get_latest_version()
        return Version(latest_version) > Version(self.current_version)

    def is_dirty(self):
        status = run_git_command(['git', 'status', '--porcelain'])
        return bool(status.strip())

    def restore_if_dirty(self):
        if self.is_dirty():
            run_git_command(['git', 'restore', '.'])

    def update(self, branch='main'):
        # 先还原，再拉取
        self.restore_if_dirty()
        return run_git_command(['git', 'pull', self.remote, branch])