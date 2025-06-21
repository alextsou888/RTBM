import ftplib
import os

FTP_HOST = "xx.xx.xx.xx"
FTP_USER = "admin"
FTP_PASS = "admin"

LOCAL_DIR = "logs"

def download_logs():
    os.makedirs(LOCAL_DIR, exist_ok=True)
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd("/")  # 根目錄，可修改
    files = ftp.nlst()
    for file in files:
        if file.endswith(".log") or file.endswith(".txt"):
            local_path = os.path.join(LOCAL_DIR, file)
            with open(local_path, "wb") as f:
                ftp.retrbinary(f"RETR {file}", f.write)
            print(f"Downloaded {file} to {local_path}")
    ftp.quit()

if __name__ == "__main__":
    download_logs()
