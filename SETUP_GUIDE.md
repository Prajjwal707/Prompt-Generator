# PromptGenius - Setup & Usage Guide

## 📦 Quick Start

### 1. Install Dependencies
```bash
npm install
```

This will install all required packages:
- React 18.2
- Vite (build tool)
- TailwindCSS (styling)
- Framer Motion (animations)
- React Router (navigation)
- Lucide React (icons)

### 2. Run Development Server
```bash
npm run dev
```

The app will start at `http://localhost:3000` with hot module reloading.

### 3. Build for Production
```bash
npm run build
```

Creates an optimized build in the `dist/` folder.

---

## 🎯 Features Overview

### 1. **Dark/Light Mode** 
- Auto-detects system preference on first visit
- Manual toggle with the theme button (top right)
- Preference saved to localStorage

### 2. **Chat Interface**
- Create new chats instantly
- View chat history in sidebar
- Auto-scrolling to latest messages
- Typing indicator animation
- Markdown support with syntax highlighting

### 3. **File & Image Upload**
- Click image/file buttons to upload
- Drag-and-drop support ready
- Preview before sending
- Remove attachments with X button

### 4. **Voice Recording**
- Click mic button to start recording
- Browser Web Speech API integration
- Automatic transcript insertion
- Visual recording indicator

### 5. **Smart Input**
- Auto-expanding textarea
- Shift+Enter for new lines
- Enhancement options (Enhance, Rewrite, Regenerate)
- Send button with loading state

### 6. **Chat History**
- Recent chats listed in sidebar
- Click any chat to load it
- Delete chats with trash icon
- All data persisted to localStorage

### 7. **Search & Discovery**
- Global search bar at top center
- Discover page with topic categories
- Quick access to exploration areas

---

## 🗂️ Project Structure Explanation

### `/src/components/` - Reusable UI Components
- **Sidebar.jsx** - Navigation with collapsible menu
- **ChatWindow.jsx** - Main chat display area
- **ChatMessage.jsx** - Individual message bubble
- **ChatInput.jsx** - Message input with attachments
- **TopSearch.jsx** - Global search bar
- **ThemeToggle.jsx** - Dark/light mode switcher
- **MicRecorderButton.jsx** - Voice input
- **ImageUploadButton.jsx** - Image upload
- **FileUploadButton.jsx** - File upload
- **FileUploadPreview.jsx** - Attachment preview

### `/src/pages/` - Full Page Components
- **Home.jsx** - Landing page with features
- **Discover.jsx** - Topic exploration page
- **Search.jsx** - Search interface

### `/src/context/` - State Management
- **ThemeContext.jsx** - Dark/light mode management
- **ChatContext.jsx** - Chat state & history

### Root Files
- **App.jsx** - Main component wrapper
- **AppRouter.jsx** - Route configuration
- **main.jsx** - React DOM entry point
- **index.css** - Global styles

---

## 🎨 Customization Guide

### Change Colors
Edit `tailwind.config.js`:
```js
colors: {
  primary: {
    500: '#your-color', // Change to your brand color
  },
  // ... other colors
}
```

### Change Typography
In `tailwind.config.js`, extend the theme:
```js
fontFamily: {
  sans: ['Your Font', 'sans-serif'],
}
```

### Add New Routes
1. Create a new page in `src/pages/YourPage.jsx`
2. Add to AppRouter.jsx:
```js
<Route path="/yourpath" element={<YourPage />} />
```

### Add New Components
1. Create in `src/components/YourComponent.jsx`
2. Import and use in other components

---

## 🔌 API Integration

The app is ready to connect to a backend. Example:

```javascript
// In ChatWindow.jsx or ChatInput.jsx
import axios from 'axios';

const handleSendMessage = async (messageData) => {
  try {
    const response = await axios.post('/api/v1/chat', {
      message: messageData.content,
      chatId: currentChatId,
      attachments: messageData.attachments,
    });
    
    // Handle response
    addMessage({
      content: response.data.reply,
      isUser: false,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

**Backend API Example** (Flask):
```python
@app.route('/api/v1/chat', methods=['POST'])
def handle_chat():
    data = request.json
    message = data.get('message')
    
    # Process with your AI model
    response = your_ai_model.generate(message)
    
    return {'reply': response}
```

---

## 📱 Responsive Behavior

### Desktop (> 768px)
- Full sidebar visible on left
- Wide chat layout
- All buttons visible

### Mobile/Tablet (< 768px)
- Sidebar collapses to bottom nav bar
- Touch-optimized buttons
- Full-width chat layout
- Cleaner header

---

## 💾 Data Storage

All data is stored in **localStorage** (client-side):

### Chat History
- Stored as JSON array
- Key: `chats`
- Includes: id, title, messages, timestamps

### Theme Preference
- Key: `theme`
- Value: 'light' or 'dark'

### Current Chat
- Key: `currentChatId`
- Value: chat ID string

**⚠️ Note**: localStorage is limited to ~5-10MB per domain. For large apps, use a backend database.

---

## 🚀 Performance Tips

1. **Lazy Load Pages**
   ```js
   const Home = lazy(() => import('./pages/Home'));
   ```

2. **Image Optimization**
   - Compress before upload
   - Use WebP format when possible

3. **Animation Performance**
   - Use Framer Motion's `transform` and `opacity` for best performance
   - Avoid animating `width`/`height`

4. **Code Splitting**
   - Vite automatically handles this
   - Dynamic imports for heavy components

---

## 🐛 Troubleshooting

### Issue: Sidebar won't collapse
- Check browser console for errors
- Ensure Framer Motion is installed

### Issue: Mic not working
- Browser must support Web Speech API (Chrome, Edge, Safari)
- Ensure HTTPS or localhost in production
- Check microphone permissions

### Issue: Styles not applying
- Clear cache: `npm run build` then refresh
- Check tailwind.config.js is valid
- Ensure CSS is imported in index.html

### Issue: Slow on mobile
- Check message count in chat
- Reduce animation complexity
- Clear localStorage if too much data

---

## 📚 Learning Resources

- [React Documentation](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Framer Motion Guide](https://www.framer.com/motion/)
- [React Router Docs](https://reactrouter.com/)
- [Lucide Icons](https://lucide.dev/)

---

## 🤝 Contributing

To add features:

1. Create a feature branch
2. Make changes in components/context/pages
3. Test thoroughly
4. Update README if needed
5. Commit with clear messages

---

## 📝 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload dist/ folder to Netlify
```

### Traditional Server
```bash
npm run build
# Copy dist/ to your server's public folder
```

---

## ⚡ Environment Variables

Create a `.env.local` file (optional):
```
VITE_API_URL=https://api.example.com
VITE_API_KEY=your_key_here
```

Access in code:
```js
const apiUrl = import.meta.env.VITE_API_URL;
```

---

## 🎓 Next Steps

1. ✅ Install and run the app
2. ✅ Explore all components
3. ✅ Customize colors and fonts
4. ✅ Connect to your backend API
5. ✅ Add user authentication
6. ✅ Deploy to production

---

**Happy Coding! 🚀**