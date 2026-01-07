# Deployment Guide - LiveScore Team Game Crawler

This guide will help you deploy the LiveScore crawler to **Streamlit Community Cloud** (free hosting).

## Prerequisites

- GitHub account
- Streamlit Cloud account (free - sign up at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Push to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   cd /Users/mac/Desktop/web/backend/crawl-games
   git init
   git add .
   git commit -m "Initial commit - LiveScore crawler"
   ```

2. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new)
   - Name it: `livescore-scraper` (or any name you prefer)
   - Don't initialize with README (we already have files)
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/livescore-scraper.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Deploy new app**:
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/livescore-scraper`
   - Set **Main file path**: `src/app.py`
   - Click "Deploy!"

3. **Wait for deployment** (usually 2-3 minutes):
   - Streamlit will automatically install dependencies from `requirements.txt`
   - Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Step 3: Configure (Optional)

### Custom Domain
- In Streamlit Cloud dashboard, go to Settings → General
- Add your custom domain if you have one

### Secrets Management
If you need to add any API keys or secrets in the future:
- Go to Settings → Secrets
- Add them in TOML format

## Files for Deployment

The following files are already configured for deployment:

### ✅ `requirements.txt`
Contains all necessary Python dependencies:
- streamlit>=1.40.0
- requests>=2.32.0
- pandas>=2.2.0
- beautifulsoup4>=4.12.0

### ✅ `src/app.py`
Main Streamlit application entry point

### ✅ `.gitignore`
Excludes unnecessary files from Git

## Troubleshooting

### Build fails with dependency errors
- Check `requirements.txt` has correct package names
- Try pinning specific versions if needed

### App crashes on startup
- Check the logs in Streamlit Cloud dashboard
- Ensure `src/app.py` has no syntax errors

### Build ID extraction fails
- This is normal - LiveScore's build ID changes periodically
- The scraper automatically extracts the current build ID
- No manual intervention needed

## Alternative Deployment Options

If you prefer other platforms:

### Docker Deployment
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "src/app.py", "--server.port=8501"]
```

### Railway.app
1. Connect your GitHub repo
2. Add start command: `streamlit run src/app.py`
3. Deploy

### Render.com
1. Connect your GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run src/app.py --server.port=$PORT`

## Post-Deployment

Once deployed, your app will be accessible at:
```
https://YOUR-APP-NAME.streamlit.app
```

Share this URL with anyone who needs to use the LiveScore crawler!

## Updating the App

To push updates:
```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically redeploy with the latest changes.
