# Portfolio Website Deployment Guide

## Quick Deploy to Netlify (Recommended)

### Option 1: Netlify Drop (Instant)
1. Run the build script: `./deploy.sh`
2. Go to [netlify.com/drop](https://netlify.com/drop)
3. Drag and drop the `frontend/dist` folder
4. Get instant live URL!

### Option 2: GitHub Integration (Automatic)
1. Push your code to GitHub
2. Go to [netlify.com](https://netlify.com) and sign up
3. Click "New site from Git"
4. Connect your GitHub repository
5. Set build settings:
   - Base directory: `portfolio-website/frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
6. Deploy automatically on every push!

## Alternative Platforms

### Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `portfolio-website/frontend`
4. Deploy with zero configuration

### GitHub Pages
1. Enable GitHub Pages in repository settings
2. Use GitHub Actions for automated deployment

## Local Testing
```bash
cd frontend
npm install
npm run dev
```

## Build for Production
```bash
./deploy.sh
```

Your portfolio will be live and accessible to anyone worldwide! 🌍