## install the following libraries

apt-get install python-pip python3-dev libpq-dev
sudo pip install virtualenv
source venv/bin/activate
pip install -r requirements.txt

## symbolic links for nginx

copy ecom.conf to sites-available folders
sudo ln -s /etc/nginx/sites-available/ecom.conf /etc/nginx/sites-enabled/
systemctl restart nginx

## create systemd service

sudo vi /etc/systemd/system/uwsgi_ecom.service

## copy uwsgi.ini files

eg cp uwsgi.digital.ini uwsgi.ini
