# Deployment Guide for AI Native Book RAG Chatbot

This guide provides step-by-step instructions for deploying the frontend to Vercel and the backend to a cloud server.

## Architecture Overview

- **Frontend**: Docusaurus-based website deployed to Vercel
- **Backend**: FastAPI server deployed to cloud server (e.g., AWS, GCP, DigitalOcean, etc.)
- **Vector Database**: Qdrant Cloud instance (already configured)
- **AI Models**: Cohere API (external service)

## 1. Frontend Deployment to Vercel

### Prerequisites
- Vercel account
- Git repository with your code
- Access to your domain (if using custom domain)

### Steps

1. **Prepare your repository**
   ```bash
   # Ensure your code is committed and pushed to GitHub/GitLab/Bitbucket
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign in and import your repository
   - Configure the project settings:
     - **Framework**: Docusaurus
     - **Build Command**: `npm run build`
     - **Output Directory**: `build`
     - **Root Directory**: `ai-native-book-website`

3. **Set Environment Variables**
   In Vercel dashboard → Project Settings → Environment Variables:
   ```
   REACT_APP_API_BASE_URL=https://your-backend-domain.com
   ```

4. **Build and Deploy**
   - Vercel will automatically build and deploy your site
   - Note the deployment URL (e.g., `https://your-project.vercel.app`)

## 2. Backend Deployment to Cloud Server

### Option A: Deploy to Cloud Server (AWS/GCP/DigitalOcean)

#### Prerequisites
- Cloud server instance (Ubuntu/Debian recommended)
- SSH access to the server
- Domain name pointing to your server IP

#### Steps

1. **SSH into your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y

   # Install Python 3.10 and pip
   sudo apt install python3.10 python3-pip python3.10-venv -y

   # Install Git
   sudo apt install git -y

   # Install Docker (optional, for containerized deployment)
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker $USER
   ```

3. **Clone your repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo/backend
   ```

4. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create production environment file**
   ```bash
   # Create .env file with production values
   cat > .env << EOF
   COHERE_API_KEY=your-production-cohere-api-key
   FRONTEND_URL=https://your-frontend-domain.com
   EOF
   ```

6. **Install and configure Nginx (reverse proxy)**
   ```bash
   sudo apt install nginx -y
   sudo systemctl start nginx
   sudo systemctl enable nginx

   # Create Nginx configuration
   sudo tee /etc/nginx/sites-available/your-backend << EOF
   server {
       listen 80;
       server_name your-backend-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host \$host;
           proxy_set_header X-Real-IP \$remote_addr;
           proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto \$scheme;
       }
   }
   EOF

   sudo ln -s /etc/nginx/sites-available/your-backend /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

7. **Set up SSL with Let's Encrypt (recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-backend-domain.com
   ```

8. **Run the application with a process manager**
   ```bash
   # Install Gunicorn for production
   pip install gunicorn

   # Run with Gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000 --daemon
   ```

9. **Set up systemd service (recommended for production)**
   ```bash
   sudo tee /etc/systemd/system/ai-native-book-backend.service << EOF
   [Unit]
   Description=AI Native Book Backend
   After=network.target

   [Service]
   Type=simple
   User=$USER
   WorkingDirectory=/home/$USER/your-repo/backend
   EnvironmentFile=/home/$USER/your-repo/backend/.env
   ExecStart=/home/$USER/your-repo/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF

   sudo systemctl daemon-reload
   sudo systemctl start ai-native-book-backend
   sudo systemctl enable ai-native-book-backend
   ```

### Option B: Deploy with Docker (Alternative)

1. **Build and run with Docker**
   ```bash
   # Navigate to backend directory
   cd backend

   # Build the Docker image
   docker build -t ai-native-book-backend .

   # Run the container
   docker run -d \
     --name ai-native-book-backend \
     -p 8000:8000 \
     -e COHERE_API_KEY=your-production-cohere-api-key \
     -e FRONTEND_URL=https://your-frontend-domain.com \
     ai-native-book-backend
   ```

## 3. Environment Variables Configuration

### Backend Environment Variables
Create a `.env` file in the backend directory:

```bash
# Production API key from Cohere
COHERE_API_KEY=your-production-cohere-api-key

# Production frontend URL (Vercel deployment URL)
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

### Frontend Environment Variables
The frontend will use the environment variable during build time:
```bash
# This is set in Vercel dashboard
REACT_APP_API_BASE_URL=https://your-backend-domain.com
```

## 4. Security Best Practices

### API Security
- **Never expose API keys in frontend code** - API keys are properly stored in backend environment variables
- **CORS Configuration** - The backend only allows requests from the specified frontend URL
- **HTTPS** - Use SSL certificates for both frontend and backend

### Environment Variables
- Store sensitive information (API keys, database credentials) in environment variables
- Never commit `.env` files to version control
- Use different API keys for development and production

### Server Security
- Keep the server OS and packages updated
- Configure firewall to only allow necessary ports (80, 443, 22)
- Use SSH keys instead of passwords for server access
- Regular security audits and monitoring

## 5. Production Best Practices

### Backend Production Settings
- Use Gunicorn with multiple workers for better performance
- Implement proper logging and monitoring
- Set up health checks
- Configure proper error handling

### Frontend Production Settings
- Enable gzip compression
- Implement proper caching strategies
- Optimize assets and images
- Set up proper error boundaries

### Monitoring and Maintenance
- Set up logging for both frontend and backend
- Monitor API response times and error rates
- Regular backups of any persistent data
- Performance monitoring and optimization

## 6. Connecting Frontend to Backend APIs

### CORS Configuration
The backend is configured to only accept requests from the specified frontend URL:

```python
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Only allow specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Communication Flow
1. Frontend makes requests to backend API endpoints
2. Backend validates the origin using CORS settings
3. Backend processes the request and returns data
4. Frontend receives and displays the data

### Error Handling
- Network errors are handled gracefully in the frontend
- Backend returns appropriate HTTP status codes
- Frontend displays user-friendly error messages

## 7. Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `FRONTEND_URL` in backend environment matches your frontend domain exactly

2. **API Connection Issues**: Check that `REACT_APP_API_BASE_URL` points to the correct backend URL

3. **SSL Certificate Issues**: Ensure both frontend and backend have valid SSL certificates in production

4. **Environment Variables**: Verify all required environment variables are set in both frontend and backend

### Health Checks
- Backend health endpoint: `GET /health`
- Frontend should implement retry logic for failed API calls

## 8. Scaling Considerations

- **Backend**: Use multiple Gunicorn workers and consider load balancing
- **Database**: Monitor Qdrant performance and consider scaling options
- **CDN**: Consider using a CDN for static assets
- **Caching**: Implement response caching for frequently requested data