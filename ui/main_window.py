from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from updater import Updater
from utils.git_api import GitSyncThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub Updater")
        self.setGeometry(100, 100, 400, 200)

        self.updater = Updater()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.check_updates_button = QPushButton("Check for Updates")
        self.check_updates_button.clicked.connect(self.check_for_updates)
        layout.addWidget(self.check_updates_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_for_updates(self):
        from ui.updater_dialog import UpdaterDialog
        if self.updater.is_update_available():
            dlg = UpdaterDialog(self)
            dlg.update_status("检测到新版本，正在同步...")
            dlg.progress_bar.setValue(0)
            self.sync_thread = GitSyncThread()
            self.sync_thread.progress.connect(dlg.update_progress)
            self.sync_thread.status.connect(dlg.update_status)
            self.sync_thread.log.connect(dlg.append_log)  # 连接日志信号

            def on_finished(ok):
                if ok:
                    dlg.update_status("同步完成")
                else:
                    dlg.update_status("同步失败")

            self.sync_thread.finished.connect(on_finished)
            self.sync_thread.start()
            dlg.exec()
        else:
            QMessageBox.information(self, "No Updates", "You are using the latest version.")
# ...existing code...