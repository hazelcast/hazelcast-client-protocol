import subprocess


class ClangFormatter:
    def fix_formatting(self, file_path):
        """Check and modifies file if needs formatting"""
        try:
            subprocess.run(['clang-format', '-i', file_path],
                           capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"clang-format error for file {file_path}: {e}")
