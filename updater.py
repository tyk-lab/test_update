import os
import subprocess
import requests
import zipfile
import io

from utils.git_sync import run_git_command


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
        self, repo_url, tag, filename, extract_to="."
    ):
        """
        :param repo_url: 仓库地址，如 https://github.com/yourusername/yourrepo
        :param tag: release 的 tag 名
        :param filename: release 上传的 zip 文件名
        :param extract_to: 解压目录
        """
        zip_url = f"{repo_url}/releases/download/{tag}/{filename}"
        local_zip = "test.zip"
        print(f"使用curl下载: {zip_url}")
        try:
            # 使用curl下载
            result = subprocess.run(
                ["curl", "-L", "-o", local_zip, zip_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"curl下载失败: {result.stderr}")
                return False
            # 解压
            with zipfile.ZipFile(local_zip, "r") as zf:
                zf.extractall(extract_to)
            print(f"解压完成，文件已保存到: {extract_to}")
            if os.path.exists(local_zip):
                os.remove(local_zip)
            return True
        except Exception as e:
            print(f"下载或解压过程中发生异常: {e}")
            return False
