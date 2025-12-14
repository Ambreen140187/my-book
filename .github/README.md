# GitHub Actions CI/CD Setup

This repository uses GitHub Actions for continuous integration and deployment of the AI Native Book application, which includes both a backend API and a Docusaurus frontend with a floating chatbot.

## Workflows

### 1. CI - Test Backend and Frontend (`ci.yml`)
- Runs on every push and pull request
- Tests multiple Python and Node.js versions
- Performs linting and code formatting checks
- Scans for security vulnerabilities
- Builds Docker images (if Dockerfiles exist)

### 2. Deploy Backend (`deploy-backend.yml`)
- Deploys the FastAPI backend to cloud platforms (Railway, Heroku, or Render)
- Builds and pushes Docker images to GitHub Container Registry
- Runs on pushes to the `main` branch
- Requires environment secrets to be configured

### 3. Deploy Frontend (`deploy-frontend.yml`)
- Deploys the Docusaurus frontend to GitHub Pages, Vercel, or Netlify
- Runs comprehensive tests before deployment
- Supports multiple hosting platforms
- Runs on pushes to the `main` branch

### 4. Health Check (`health-check.yml`)
- Runs daily health checks on deployed services
- Tests API endpoints and frontend accessibility
- Provides automated monitoring of deployed applications
- Can be triggered manually

### 5. Release (`release.yml`)
- Creates GitHub releases when version tags are pushed
- Generates changelogs automatically
- Builds and uploads Docker images to container registry
- Can be triggered manually with custom version numbers

## Required Secrets

For full functionality, configure these secrets in your GitHub repository settings:

### Backend Deployment Secrets
- `RAILWAY_TOKEN` - Railway account token
- `RAILWAY_PROJECT_ID` - Railway project ID
- `HEROKU_API_KEY` - Heroku account API key
- `HEROKU_APP_NAME` - Heroku app name
- `RENDER_DEPLOY_HOOK` - Render deployment hook URL
- `BACKEND_URL` - Public URL of deployed backend

### Frontend Deployment Secrets
- `VERCEL_TOKEN` - Vercel account token
- `VERCEL_PROJECT_ID` - Vercel project ID
- `VERCEL_ORG_ID` - Vercel organization ID
- `NETLIFY_AUTH_TOKEN` - Netlify account token
- `NETLIFY_SITE_ID` - Netlify site ID
- `FRONTEND_URL` - Public URL of deployed frontend

### General Secrets
- `COHERE_API_KEY` - Cohere API key (for backend, though this should be set in the deployment platform's environment variables, not in GitHub secrets for security)

## Environments

The workflows use GitHub Environments for deployment:
- `production` - For backend deployments
- `github-pages` - For frontend GitHub Pages deployment

## Deployment Platforms

The workflows support multiple deployment platforms:

### Backend
- **Railway** (primary): Modern cloud platform with easy environment variable management
- **Heroku**: Traditional platform-as-a-service
- **Render**: Simple deployment platform with free tier

### Frontend
- **GitHub Pages** (primary): Built-in GitHub hosting
- **Vercel**: Optimized for React/Next.js applications
- **Netlify**: Static site hosting with form handling

## Getting Started

1. **Fork this repository**
2. **Configure repository secrets** in Settings > Secrets and variables
3. **Set up environments** in Settings > Environments (if needed)
4. **Push to main branch** to trigger deployments
5. **Create version tags** (e.g., `v1.0.0`) to create releases

## Best Practices

- Always test in a separate branch before merging to main
- Use semantic versioning for tags (e.g., `v1.0.0`, `v1.0.1`)
- Monitor the Actions tab for workflow status and logs
- Keep secrets secure and never commit them to the repository
- Use environment-specific configurations for different deployment stages

## Troubleshooting

If workflows fail:
1. Check the Actions logs for specific error messages
2. Verify that all required secrets are properly configured
3. Ensure Dockerfiles exist if using container-based deployments
4. Confirm that deployment platform tokens have the necessary permissions