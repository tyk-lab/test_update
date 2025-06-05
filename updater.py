import os


class Updater:
    def __init__(self, version_file='version.txt'):
        self.version_file = version_file
        self.current_version = self.get_current_version()

    def get_current_version(self):
        # 假设本地有 version.txt 文件，内容为当前版本号
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return "0.0.0"

    def get_latest_version(self, branch='main', file_path='version'):
        from utils.git_api import run_git_command
        return run_git_command(['git', 'show', f'origin/{branch}:{file_path}'])

    def check_for_updates(self):
        latest_version = self.get_latest_version()
        if latest_version and self.is_update_available(latest_version):
            return latest_version
        return None

    def is_update_available(self, latest_version):
        from utils.version import Version
        return Version(latest_version) > Version(self.current_version)

