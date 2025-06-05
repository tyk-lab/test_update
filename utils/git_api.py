import subprocess
from PyQt6.QtCore import Qt, QThread, pyqtSignal

def run_git_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


class GitSyncThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def run(self):
        self.status.emit("正在同步远程分支...")
        # 这里只是模拟进度，实际可根据输出调整
        process = subprocess.Popen(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        total_steps = 5
        for i in range(total_steps):
            self.progress.emit(int((i + 1) * 100 / total_steps))
            self.msleep(300)
        output, _ = process.communicate()
        if process.returncode == 0:
            self.status.emit("同步完成")
            self.progress.emit(100)
            self.finished.emit(True)
        else:
            self.status.emit("同步失败")
            self.finished.emit(False)

