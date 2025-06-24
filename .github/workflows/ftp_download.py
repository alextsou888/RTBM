    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11

      - name: Install dependencies
        run: python -m pip install --upgrade pip paramiko  # paramiko 是 Python SFTP 套件

      - name: Download logs from SFTP
        run: python ftp_download.py --target logs

      - name: Run log analysis
        run: python log_analyzer.py logs
