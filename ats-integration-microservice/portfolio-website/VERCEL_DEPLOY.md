# Deploy Portfolio on Vercel

## Quick Deploy Steps:

### 1. Go to Vercel
Visit [vercel.com](https://vercel.com) and sign up with GitHub

### 2. Import Project
- Click **"New Project"**
- Select your **"Projects"** repository
- Choose **"portfolio-website"** folder

### 3. Configure Settings
Vercel will auto-detect, but verify:
- **Framework Preset:** Vite
- **Root Directory:** `portfolio-website`
- **Build Command:** `cd frontend && npm run build`
- **Output Directory:** `frontend/dist`

### 4. Deploy
Click **"Deploy"** - Done in 2 minutes!

## Your Live URL:
`https://your-portfolio-name.vercel.app`

## Advantages of Vercel:
- ✅ Zero configuration for React/Vite
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-deploy on Git push
- ✅ Custom domains
- ✅ Better performance than Netlify

## Alternative: CLI Deploy
```bash
npm i -g vercel
cd portfolio-website
vercel
```