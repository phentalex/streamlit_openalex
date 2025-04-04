import subprocess
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
to_run_path = os.path.join(BASE_DIR, "ui/pages/main_page.py")


def streamlit_run():
    subprocess.run([
        "streamlit", "run", to_run_path,
        "--server.address=0.0.0.0",
        "--server.port=8501"
    ])


if __name__ == "__main__":
    streamlit_run()
