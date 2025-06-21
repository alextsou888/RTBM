from ftplib import FTP
from pathlib import Path

FTP_HOST = "xx.xx.xx.xx"
FTP_USER = "admin"
FTP_PASS = "admin"

DOWNLOAD_DIR = Path("logs")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def download_latest_txt():
    with FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd("/")  # 修改為正確 FTP 目錄

        files = ftp.nlst()
        txt_files = [f for f in files if f.endswith(".txt")]
        if not txt_files:
            print("❌ No .txt files found on FTP.")
            return

        latest_file = max(txt_files, key=lambda name: ftp.sendcmd(f"MDTM {name}"))
        local_path = DOWNLOAD_DIR / latest_file

        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {latest_file}", f.write)

        print(f"✅ Downloaded {latest_file} to {local_path}")

if __name__ == "__main__":
    download_latest_txt()