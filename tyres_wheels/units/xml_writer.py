[Unit]
Description=xml_writer
After=multi-user.target

[Service]
User=root
Type=idle
ExecStart=/usr/bin/python3 /usr/local/bin/fuck_debian/tyres_wheels/shedul.py
Restart=always

[Install]
WantedBy=multi-user.target