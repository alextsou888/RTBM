import ftplib
import os
import argparse

def download_largest_log_file(host, remote_dir, local_dir):
    user = 'admin'
    passwd = 'admin'

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    with ftplib.FTP(host) as ftp:
        print(f"Connecting to FTP {host} ...")
        ftp.login(user=user, passwd=passwd)
        ftp.set_pasv(True)
        for part in remote_dir.strip('/').split('/'):
            print(f"Changing into: {part}")
            ftp.cwd(part)

        files = ftp.nlst()
        log_files = [f for f in files if f.lower().endswith('.log')]
        if not log_files:
            print("No .log files found")
            return

        largest_file = max(log_files, key=lambda f: ftp.size(f))
        local_path = os.path.join(local_dir, largest_file)

        print(f"Downloading largest .log file: {largest_file}")
        with open(local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {largest_file}', f.write)
        print(f"Downloaded to: {local_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help='FTP server IP or hostname')
    parser.add_argument('--remote_dir', default='/E/RTBM_StabilityTool_2.1.2.1/Log', help='Remote FTP directory path')
    parser.add_argument('--local_dir', default='logs', help='Local directory to save downloaded files')
    args = parser.parse_args()

    download_largest_log_file(args.host, args.remote_dir, args.local_dir)

 
