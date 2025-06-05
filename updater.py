import os
from utils.git_api import run_git_command
import requests
import zipfile
import io


class Updater:
    def __init__(self, version_file="version", remote="origin"):
        self.version_file = version_file
        self.remote = remote
        self.current_version = self.get_current_version()

    def get_current_version(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        version_file_path = parent_dir + "/" + self.version_file
        print(version_file_path)
        if os.path.exists(version_file_path):
            with open(self.version_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "0.0.0"

    def get_latest_version(self, branch="master", file_path="version"):
        list = ["git", "show", f"{self.remote}/{branch}:{file_path}"]
        print(list)
        return run_git_command(["git", "show", f"{self.remote}/{branch}:{file_path}"])

    def is_update_available(self):
        from utils.version import Version

        latest_version = self.get_latest_version()
        print(latest_version, "----", self.current_version)
        return Version(latest_version) > Version(self.current_version)

    def is_dirty(self):
        status = run_git_command(["git", "status", "--porcelain"])
        return bool(status.strip())

    def restore_if_dirty(self):
        if self.is_dirty():
            run_git_command(["git", "restore", "."])

    def update(self, branch="main"):
        # 先还原，再拉取
        self.restore_if_dirty()
        return run_git_command(["git", "pull", self.remote, branch])

    def download_and_extract_release_zip(
        self, repo_url, branch="release", extract_to="."
    ):
        """
        从GitHub下载release分支的zip包并解压到指定目录
        :param repo_url: 仓库地址，如 https://github.com/yourusername/yourrepo
        :param branch: 分支名，默认为release
        :param extract_to: 解压目录
        """
        zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
        print(f"Downloading: {zip_url}")
        response = requests.get(zip_url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                zf.extractall(extract_to)
            print(f"解压完成，文件已保存到: {extract_to}")
            return True
        else:
            print(f"下载失败，状态码: {response.status_code}")
            return False
