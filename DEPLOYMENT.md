# 🚀 EchoWrite Deployment Guide - Render (Monorepo)

This guide walks you through deploying EchoWrite as a monorepo on Render.

## Why Render?

- ✅ **Native monorepo support** - No Docker needed
- ✅ **Pay-as-you-go** - Free tier + $7/mo for production
- ✅ **Auto-deploy** from GitHub
- ✅ **Native Python & Node.js** support
- ✅ **Built-in SSL** certificates
- ✅ **Simple environment variables** management

## 📋 Prerequisites

- [x] GitHub repository created and pushed
- [x] Supabase account with database setup
- [x] OpenAI API key
- [x] Resend API key (for email)

## 🎯 Deployment Steps

### Step 1: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Deploy Using Blueprint (Recommended)

**This deploys both frontend and backend in one click!**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository: `amkdanton/echo-write`
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

Render will create:
- ✅ `echowrite-backend` - Python web service
- ✅ `echowrite-frontend` - Static site

### Step 3: Configure Backend Environment Variables

After blueprint deployment, configure the backend:

1. Go to **echowrite-backend** service
2. Click **"Environment"** tab
3. Add these environment variables:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here

# Resend (Email)
RESEND_API_KEY=re_your-key-here

# CORS (Set after frontend deploys)
CORS_ORIGINS=https://echowrite-frontend.onrender.com
```

4. Click **"Save Changes"**
5. Service will automatically redeploy

### Step 4: Configure Frontend Environment Variables

1. Go to **echowrite-frontend** service
2. Click **"Environment"** tab
3. Add this variable:

```bash
# Point to your backend URL
VITE_API_URL=https://echowrite-backend.onrender.com/api/v1
```

4. Click **"Save Changes"**
5. Frontend will rebuild and redeploy

### Step 5: Update Backend CORS

Now that frontend is deployed:

1. Go back to **echowrite-backend** 
2. Update the `CORS_ORIGINS` variable with your actual frontend URL
3. Save and let it redeploy

---

## 🔧 Alternative: Manual Service Setup

If you prefer manual setup instead of Blueprint:

### Deploy Backend Manually

1. Click **"New"** → **"Web Service"**
2. Connect repository: `amkdanton/echo-write`
3. Configure:
   - **Name**: `echowrite-backend`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free or Starter ($7/mo)
4. Add environment variables (from Step 3 above)
5. Click **"Create Web Service"**

### Deploy Frontend Manually

1. Click **"New"** → **"Static Site"**
2. Connect repository: `amkdanton/echo-write`
3. Configure:
   - **Name**: `echowrite-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add environment variable (from Step 4 above)
5. Click **"Create Static Site"**

---

## 🔍 Verify Deployment

### Backend Health Check

Visit: `https://echowrite-backend.onrender.com/api/v1/health`

You should see:
```json
{
  "status": "healthy",
  "service": "echowrite-api",
  "version": "1.0.0"
}
```

### Frontend Check

Visit: `https://echowrite-frontend.onrender.com`

You should see the EchoWrite landing page.

---

## 📊 Cost Breakdown

### Free Tier (Development)
- **Backend**: Free (spins down after 15 min inactivity)
- **Frontend**: Free (always on)
- **Total**: $0/month

### Starter Tier (Production Recommended)
- **Backend**: $7/month (always on, 512 MB RAM)
- **Frontend**: Free (always on)
- **Total**: $7/month

### Pro Tier (Scale)
- **Backend**: $25/month (2 GB RAM, autoscaling)
- **Frontend**: Free
- **Total**: $25/month

---

## 🐛 Troubleshooting

### Backend Won't Start

**Check logs:**
1. Go to backend service
2. Click **"Logs"** tab
3. Look for errors

**Common issues:**
- Missing environment variables
- Python version mismatch
- Dependency installation failures

**Fix:**
```bash
# Ensure Python version in render.yaml matches
PYTHON_VERSION=3.11.0
```

### Frontend Build Fails

**Common issues:**
- Missing VITE_API_URL
- Node version mismatch

**Fix:**
```bash
# Set Node version
NODE_VERSION=18.17.0
```

### CORS Errors

**Fix:**
1. Go to backend service
2. Update CORS_ORIGINS to include your frontend URL:
   ```
   CORS_ORIGINS=https://echowrite-frontend.onrender.com,http://localhost:5173
   ```

### Database Connection Issues

**Check Supabase:**
1. Verify SUPABASE_URL is correct
2. Ensure RLS policies are set up
3. Check service role key has proper permissions

---

## 🔄 Auto-Deploy on Git Push

Render automatically deploys when you push to `main` branch:

```bash
git add .
git commit -m "your changes"
git push origin main
```

Both services will automatically rebuild and redeploy!

---

## 🔐 Security Best Practices

### Environment Variables
- ✅ Never commit `.env` files
- ✅ Use Render's environment variables dashboard
- ✅ Rotate API keys regularly

### CORS Configuration
- ✅ Only allow your frontend domain
- ✅ Remove localhost from production CORS

### Database
- ✅ Use Supabase RLS policies
- ✅ Never use service role key in frontend

---

## 📈 Monitoring & Logs

### View Logs
1. Go to service in Render dashboard
2. Click **"Logs"** tab
3. Real-time streaming logs available

### Metrics
1. Click **"Metrics"** tab
2. View CPU, Memory, Request count
3. Set up alerts for downtime

---

## 🚀 Production Checklist

Before going live:

- [ ] All environment variables set correctly
- [ ] Health check endpoint working
- [ ] CORS configured properly (only production domains)
- [ ] Database RLS policies active
- [ ] API keys rotated and secure
- [ ] Error logging configured
- [ ] Monitoring alerts set up
- [ ] Backup strategy for database
- [ ] Custom domain configured (optional)

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain to Frontend

1. Go to **echowrite-frontend** service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain: `app.yourdomain.com`
4. Follow DNS instructions
5. SSL certificate auto-generated

### Add Custom Domain to Backend

1. Go to **echowrite-backend** service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your API domain: `api.yourdomain.com`
4. Update frontend `VITE_API_URL` to new domain

---

## 💡 Tips for Free Tier

If using free tier (backend spins down):

1. **First request will be slow** (cold start ~30s)
2. **Use UptimeRobot** to ping backend every 14 minutes
3. **Or upgrade to Starter** for $7/mo (always on)

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Supabase Docs**: https://supabase.com/docs

---

**🎉 Your EchoWrite app is now live!**

Backend: `https://echowrite-backend.onrender.com`  
Frontend: `https://echowrite-frontend.onrender.com`

