# Deployment Guide

This guide explains how to deploy your application to Streamlit Cloud and a backend hosting service.

## Architecture

Your application consists of two parts:
1. **Frontend (Streamlit)**: User interface - deploy to Streamlit Cloud
2. **Backend (FastAPI)**: API server - deploy to a separate service (Railway, Render, Fly.io, etc.)

## Prerequisites

1. **GitHub Account**: Streamlit Cloud requires your code to be on GitHub
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Backend Hosting**: Choose one of:
   - [Railway](https://railway.app) (recommended, easy setup)
   - [Render](https://render.com)
   - [Fly.io](https://fly.io)
   - [Heroku](https://heroku.com) (paid)

---

## Step 1: Deploy Backend (FastAPI)

### Option A: Railway (Recommended)

1. **Sign up** at [railway.app](https://railway.app)
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select your repository**
4. **Configure the service**:
   - Go to your service → **Settings** tab
   - **Root Directory**: Leave empty (or set to `Backend/` if needed)
   
   **CRITICAL - Override Build Settings**:
   - In Settings, find **"Build Command"** section
   - **Clear/Override** the auto-detected build command
   - Set **Build Command** to: `bash build.sh` or `uv sync`
   - Set **Start Command** to: `uv run python Backend/main.py`
   
   **If Railway still uses pip** (and you see `pip install -r requirements.txt` in logs):
   - The updated `requirements.txt` now has all dependencies with `pandas>=2.2.0`
   - But you still need Python 3.12, not 3.13
   - Try adding this to **Variables**: `NIXPACKS_PYTHON_VERSION=3.12`
   - Or use the build script: Set Build Command to `bash build.sh`
   
   **Important Notes**: 
   - Railway may auto-detect Python 3.13, which causes pandas build failures
   - The `nixpacks.toml` file should force Python 3.12, but Railway might ignore it
   - Railway will automatically set the `PORT` environment variable (already handled in `Backend/main.py`)

5. **Add Environment Variables**:
   - Go to your service → **Variables** tab
   - Click **"New Variable"** or **"Raw Editor"**
   - Add these variables (one per line in Raw Editor, or add individually):
     ```
     PYTHON_VERSION=3.12
     GEMINI_API_KEY=your_api_key_here
     ```
   - **OR** if using the form interface:
     - **Variable Name**: `PYTHON_VERSION`
     - **Value**: `3.12`
     - Then add another:
     - **Variable Name**: `GEMINI_API_KEY`
     - **Value**: `your_api_key_here`

6. **Get your backend URL**: Railway will provide a URL like `https://your-app.railway.app`

### Option B: Render

1. **Sign up** at [render.com](https://render.com)
2. **New** → **Web Service**
3. **Connect your GitHub repository**
4. **Configure**:
   - **Name**: `your-backend-name`
   - **Root Directory**: Leave empty
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt` (or use uv)
   - **Start Command**: `python Backend/main.py` or `uvicorn Backend.main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**:
   - `GEMINI_API_KEY` = `your_api_key_here`

6. **Get your backend URL**: Render provides `https://your-app.onrender.com`

---

## Step 2: Deploy Frontend (Streamlit Cloud)

1. **Push your code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure your app**:
   - **Repository**: Select your repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `Frontend/app.py`
   - **Python version**: **3.12** (recommended) or 3.11
     - **Note**: If you see numpy build errors, Streamlit Cloud may be using Python 3.13. Explicitly set to 3.12.

6. **Add Secrets** (click "Advanced settings" → "Secrets"):
   ```
   API_BASE_URL=https://s-aof7.onrender.com
   ```
   (Use your actual backend URL - example shown is for Render deployment)

7. **Click "Deploy"**

8. **Wait for deployment** (usually 1-2 minutes)

9. **Your app will be live at**: `https://your-app-name.streamlit.app`

---

## Step 3: Update Environment Variables

### For Streamlit Cloud:
- Go to your app → Settings → Secrets
- Add/update: `API_BASE_URL` = your backend URL

### For Backend (Railway/Render/etc.):
- Add: `GEMINI_API_KEY` = your Gemini API key
- The backend will automatically use port provided by the hosting service

---

## Troubleshooting

### Frontend can't connect to backend
- Check that `API_BASE_URL` is set correctly in Streamlit Cloud secrets
- Verify your backend is running and accessible
- Check backend logs for errors

### Backend SSL errors
- The backend should handle SSL verification (already configured in `FHIRClient.py`)

### Backend not starting
- Check that `GEMINI_API_KEY` is set in backend environment variables
- Verify Python version matches (3.11 or 3.12, **NOT 3.13**)
- Check build logs for dependency installation errors

### Pandas/Numpy build error (Python 3.13 compatibility)
**Error**: `pandas==2.1.0` or `numpy==1.26.0` fails to build with Python 3.13
**Solution**:
1. **For Streamlit Cloud**: 
   - Set Python version to **3.12** in app settings (not 3.13)
   - Or update `requirements.txt` to use `numpy>=2.0.0` and `pandas>=2.2.0` (already done)
2. **For Railway**:
   - Set Python version to **3.12** in Railway settings (not 3.13)
   - If Railway is using `pip install -r requirements.txt`:
     - Ensure `requirements.txt` has `pandas>=2.2.0` and `numpy>=2.0.0` (already done)
     - Or use `uv sync` as build command to use `pyproject.toml` instead
3. If using `uv sync`, it should automatically use the correct Python version from `pyproject.toml`

### CORS errors
- FastAPI should allow CORS (you may need to add CORS middleware to `main.py`)

---

## Adding CORS to Backend (if needed)

If you get CORS errors, add this to `Backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Streamlit app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Locally

Before deploying, test with environment variables:

```bash
# Terminal 1: Start backend
API_BASE_URL=http://localhost:8000 uv run python Backend/main.py

# Terminal 2: Start frontend
API_BASE_URL=http://localhost:8000 uv run streamlit run Frontend/app.py
```

---

## Cost

- **Streamlit Cloud**: Free (public repos) or $20/month (private repos)
- **Railway**: Free tier with $5 credit/month, then pay-as-you-go
- **Render**: Free tier available (with limitations)

---

## Next Steps

1. Deploy backend first and get the URL
2. Deploy frontend with the backend URL in secrets
3. Test the full application
4. Share your Streamlit app URL!

