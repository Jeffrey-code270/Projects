# Netlify Deployment Fix

## Updated Settings for Netlify:

**Base directory:** `portfolio-website/frontend`
**Build command:** `npm run build`  
**Publish directory:** `dist`

## If Still Not Working:

### Option 1: Manual Deploy
1. Download your repository as ZIP
2. Extract and navigate to `portfolio-website/frontend`
3. Go to [netlify.com/drop](https://netlify.com/drop)
4. Drag the entire `frontend` folder
5. Netlify will build automatically

### Option 2: Check Build Logs
1. In Netlify dashboard, click "Deploys"
2. Click on failed deploy
3. Check build logs for errors
4. Common issues:
   - Missing dependencies
   - Build command errors
   - Wrong directory paths

### Option 3: Alternative - GitHub Pages
1. Go to repository Settings
2. Pages → Source: GitHub Actions
3. Use the workflow I created

## Quick Test:
Your site should show:
- Dark theme portfolio
- Navigation menu
- Projects section
- Contact form

If blank page: Check browser console for errors.