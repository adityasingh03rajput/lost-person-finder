# Deployment Guide

This guide covers different deployment options for the Lost Person Finder system.

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
git clone https://github.com/yourusername/lost-person-finder.git
cd lost-person-finder
pip install -r requirements.txt
python init_database.py
python server_simple.py
```

## 🌐 Production Deployment

### Option 1: Traditional Server (Ubuntu/CentOS)

1. **Install Python and dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

2. **Clone and setup project**
   ```bash
   git clone https://github.com/yourusername/lost-person-finder.git
   cd lost-person-finder
   pip3 install -r requirements.txt
   python3 init_database.py
   ```

3. **Install Gunicorn**
   ```bash
   pip3 install gunicorn
   ```

4. **Create systemd service**
   ```bash
   sudo nano /etc/systemd/system/lost-person-finder.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Lost Person Finder
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/lost-person-finder
   Environment="PATH=/path/to/lost-person-finder/venv/bin"
   ExecStart=/path/to/lost-person-finder/venv/bin/gunicorn --workers 3 --bind unix:lost-person-finder.sock -m 007 server_simple:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/lost-person-finder/lost-person-finder.sock;
       }

       location /uploads/ {
           alias /path/to/lost-person-finder/uploads/;
       }
   }
   ```

### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   RUN python init_database.py

   EXPOSE 5000

   CMD ["python", "server_simple.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t lost-person-finder .
   docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads lost-person-finder
   ```

### Option 3: Cloud Deployment (Heroku)

1. **Create Procfile**
   ```
   web: gunicorn server_simple:app
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🔒 Security Considerations

### Production Settings
- Use HTTPS in production
- Set secure environment variables
- Configure proper file permissions
- Enable CORS only for trusted domains
- Implement rate limiting
- Use a reverse proxy (Nginx/Apache)

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

## 📊 Monitoring

### Health Checks
- Monitor `/api/health` endpoint
- Set up uptime monitoring
- Configure log aggregation

### Performance
- Use application performance monitoring (APM)
- Monitor database performance
- Track API response times

## 🔄 Updates

### Rolling Updates
```bash
git pull origin main
pip install -r requirements.txt
sudo systemctl restart lost-person-finder
```

### Database Migrations
```bash
python init_database.py  # Safe to run multiple times
```

## 🛠️ Troubleshooting

### Common Issues
1. **Port already in use**: Change port in server configuration
2. **Permission denied**: Check file permissions and user ownership
3. **Database locked**: Ensure only one instance is running
4. **Memory issues**: Increase server memory or optimize queries

### Logs
```bash
# System logs
sudo journalctl -u lost-person-finder

# Application logs
tail -f /path/to/lost-person-finder/app.log
```

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple instances
- Shared database and file storage

### Database Scaling
- Consider PostgreSQL for production
- Implement database replication
- Use connection pooling

### File Storage
- Use cloud storage (AWS S3, Google Cloud Storage)
- Implement CDN for static files
- Consider image optimization