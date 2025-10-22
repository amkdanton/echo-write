# 🎨 EchoWrite Frontend

Modern React frontend for AI-powered content curation and newsletter generation.

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── components/        # Reusable UI Components
│   │   ├── Layout.tsx     # Main layout wrapper
│   │   ├── ProtectedRoute.tsx # Route protection
│   │   └── AuthModal.tsx  # Authentication modal
│   ├── contexts/          # React Context
│   │   └── AuthContext.tsx # Authentication state
│   ├── pages/             # Page Components
│   │   ├── Landing.tsx    # Landing page
│   │   ├── Dashboard.tsx  # Main dashboard
│   │   ├── Sources.tsx    # Source management
│   │   ├── Drafts.tsx     # Draft management
│   │   └── Settings.tsx   # User settings
│   ├── services/          # API Services
│   │   ├── api.ts         # API client
│   │   └── auth.ts        # Authentication service
│   ├── utils/             # Utilities
│   ├── App.tsx            # Root component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS config
└── tsconfig.json          # TypeScript config
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 🔧 Environment Variables

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1

# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🎨 Tech Stack

### Core Technologies

- **React 18**: Modern React with hooks and context
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework

### Key Libraries

- **@supabase/supabase-js**: Supabase client
- **@tanstack/react-query**: Data fetching and caching
- **react-router-dom**: Client-side routing
- **react-hot-toast**: Toast notifications
- **@heroicons/react**: Icon library

## 📱 Features

### 🏠 Landing Page

- **Hero Section**: Compelling value proposition
- **Feature Showcase**: Key benefits and capabilities
- **Authentication**: Sign up and sign in forms
- **User Types**: Creator and Agency options

### 📊 Dashboard

- **Real-time Stats**: Sources, drafts, and generation metrics
- **Quick Actions**: Generate newsletter button
- **Recent Drafts**: Latest newsletter drafts
- **Status Indicators**: Generation and delivery status

### 📰 Sources Management

- **Source Types**: RSS feeds and YouTube channels
- **CRUD Operations**: Add, edit, delete, and test sources
- **Real-time Testing**: Test source connectivity
- **Bulk Operations**: Manage multiple sources

### 📝 Drafts Management

- **Draft List**: All generated newsletters
- **Live Preview**: Real-time Markdown preview
- **Status Management**: Draft, generating, sent states
- **Actions**: Send, delete, and feedback options

### ⚙️ Settings

- **User Profile**: Personal information and preferences
- **Voice Training**: Writing style samples
- **Notification Preferences**: Email and app notifications
- **Account Management**: Password and security settings

## 🔐 Authentication

### Authentication Flow

1. **Sign Up**: Create account with email/password
2. **Email Verification**: Verify email address
3. **Sign In**: Authenticate with credentials
4. **Session Management**: Automatic token refresh
5. **Protected Routes**: Secure access to app features

### User Types

- **Creator**: Independent content creators
- **Agency**: Marketing agencies and teams

### State Management

- **AuthContext**: Global authentication state
- **React Query**: Server state caching
- **Local Storage**: Session persistence

## 🎨 UI/UX Features

### Design System

- **Color Palette**: Professional blue and gray scheme
- **Typography**: Clean, readable fonts
- **Spacing**: Consistent spacing system
- **Components**: Reusable UI components

### Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Enhanced tablet experience
- **Desktop**: Full desktop functionality
- **Progressive Enhancement**: Works on all devices

### Accessibility

- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: ARIA labels and descriptions
- **Color Contrast**: WCAG compliant colors
- **Focus Management**: Clear focus indicators

## 🔧 Development

### Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking
npm run test         # Run tests
```

### Code Structure

- **Components**: Functional components with hooks
- **Pages**: Route-level components
- **Services**: API and external service integrations
- **Contexts**: Global state management
- **Utils**: Helper functions and utilities

### Styling

- **Tailwind CSS**: Utility-first styling
- **Component Styles**: Scoped component styles
- **Global Styles**: Base styles and resets
- **Responsive**: Mobile-first responsive design

## 🧪 Testing

### Testing Strategy

- **Unit Tests**: Component testing with Jest
- **Integration Tests**: API integration testing
- **E2E Tests**: Full user journey testing
- **Visual Regression**: UI consistency testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## 📊 Performance

### Optimization Features

- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Component lazy loading
- **Image Optimization**: Optimized images
- **Bundle Analysis**: Bundle size monitoring

### Performance Metrics

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

## 🚨 Troubleshooting

### Common Issues

1. **Build Errors**: Check TypeScript errors and dependencies
2. **API Connection**: Verify API URL and CORS settings
3. **Authentication**: Check Supabase configuration
4. **Styling**: Verify Tailwind CSS configuration

### Debug Mode

```bash
# Run with debug logging
DEBUG=true npm run dev
```

### Browser DevTools

- **React DevTools**: Component inspection
- **Network Tab**: API request monitoring
- **Console**: Error logging and debugging
- **Performance**: Performance profiling

## 📱 Browser Support

- **Chrome**: Latest 2 versions
- **Firefox**: Latest 2 versions
- **Safari**: Latest 2 versions
- **Edge**: Latest 2 versions

## 🔄 Deployment

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Deployment Checklist

- [ ] Set production environment variables
- [ ] Configure production API URL
- [ ] Set up proper caching headers
- [ ] Configure error tracking
- [ ] Set up analytics
- [ ] Test production build
- [ ] Configure SSL/TLS
- [ ] Set up monitoring

### Deployment Platforms

- **Vercel**: Recommended for React apps
- **Netlify**: Alternative static hosting
- **AWS S3**: Static website hosting
- **GitHub Pages**: Free hosting option

---

**EchoWrite Frontend** — _Beautiful, modern interface for AI-powered newsletters_
