# Django Deployment Guide

This guide provides step-by-step instructions for deploying a Django web Template on a server using VPS. By following these steps, you can deploy your Django project in a production environment.

## Prerequisites

Before you begin, make sure you have the following:

- A Django project hosted on GitHub.
- A server with a web server (e.g., Nginx or Apache) and a database server (e.g., PostgreSQL or MySQL) installed.
- Python and virtualenv installed on your server.

## Step 1: Clone Your GitHub Repository

Clone your Django project from GitHub to your server:

```bash
git clone https://github.com/your-username/template.git
cd template
```

## Step 2: Set Up Virtual Environment

Create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure Django Settings

Update your Django settings to match your production environment. Update the `DEBUG` setting to `False` and configure database settings.

```bash
nano template/settings.py
```

## Step 4: Collect Static Files

Collect static files to a directory that your web server can serve:

```bash
python manage.py collectstatic
```

## Step 5: Configure Database

Migrate your database and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Step 6: Set Up Gunicorn

Install Gunicorn (a WSGI server for Django):

```bash
pip install gunicorn
```

Create a Gunicorn service file:

```bash
nano /etc/systemd/system/template.service
```

Add the following content, adjusting paths as needed:

```ini
[Unit]
Description=gunicorn daemon for template
After=network.target

[Service]
User=your-user
Group=your-group
WorkingDirectory=/path/to/template
ExecStart=/path/to/venv/bin/gunicorn --workers=3 --bind unix:/path/to/template/template.sock template.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn service:

```bash
sudo systemctl start template
sudo systemctl enable template
```

## Step 7: Configure Nginx

Install Nginx:

```bash
sudo apt-get install nginx
```

Create an Nginx server block configuration:

```bash
sudo nano /etc/nginx/sites-available/template
```

Add the following content, adjusting paths and server_name:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /path/to/template;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/template/template.sock;
    }
}
```

Create a symbolic link to enable the Nginx configuration:

```bash
sudo ln -s /etc/nginx/sites-available/template /etc/nginx/sites-enabled
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

## Step 8: Set Up SSL (Optional)

If you want to enable SSL, consider using Let's Encrypt to obtain and install a free SSL certificate:

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts to complete the certificate installation.

## Step 9: Finalize Deployment

Restart Gunicorn and Nginx to apply changes:

```bash
sudo systemctl restart template
sudo systemctl restart nginx
```

Your Django project should now be deployed and accessible on your domain. Visit your domain in a web browser to verify the deployment.

Congratulations! Your Django project is now successfully deployed on your server using GitHub.
