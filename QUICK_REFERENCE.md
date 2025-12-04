# PromptGenius - Quick Reference

## 🚀 5-Minute Setup

```bash
# 1. Install dependencies
npm install

# 2. Start dev server  
npm run dev

# 3. Open browser to http://localhost:3000
# Done! You now have a full AI chat interface
```

---

## 📁 Project Files at a Glance

| File | Purpose |
|------|---------|
| `src/App.jsx` | Main app wrapper with theme/chat providers |
| `src/main.jsx` | React DOM entry point |
| `src/AppRouter.jsx` | Route definitions |
| `src/index.css` | Global styles + Tailwind |
| `package.json` | Dependencies & scripts |
| `vite.config.js` | Build configuration |
| `tailwind.config.js` | Theme colors & animations |

---

## 🧩 Component Quick Reference

### Must-Use Components
```jsx
// Chat functionality
import ChatWindow from './components/ChatWindow';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';

// UI Components
import Sidebar from './components/Sidebar';
import TopSearch from './components/TopSearch';
import ThemeToggle from './components/ThemeToggle';

// File handling
import FileUploadPreview from './components/FileUploadPreview';
import ImageUploadButton from './components/ImageUploadButton';
import FileUploadButton from './components/FileUploadButton';

// Voice
import MicRecorderButton from './components/MicRecorderButton';
```

---

## 🎯 Context API Quick Ref

### Chat State
```js
import { useChat } from './context/ChatContext';

const {
  chats,           // All chats array
  currentChatId,   // Active chat ID
  createNewChat,   // Create new chat
  addMessage,      // Add to current
  deleteChat,      // Remove chat
  loadChat,        // Switch chat
  getCurrentChat   // Get current object
} = useChat();
```

### Theme State
```js
import { useTheme } from './context/ThemeContext';

const { theme, toggleTheme } = useTheme();
// theme = 'light' | 'dark'
```

---

## 🎨 Common TailwindCSS Classes

```jsx
// Colors
className="text-blue-500"           // Primary blue
className="bg-cyan-500"             // Accent cyan
className="dark:bg-slate-900"       // Dark bg
className="dark:text-white"         // Dark text

// Spacing
className="p-4"                     // Padding
className="gap-3"                   // Gap between items
className="mb-4"                    // Margin bottom

// Styling
className="rounded-lg"              // Border radius
className="border border-gray-200"  // Border
className="shadow-lg"               // Shadow
className="hover:bg-gray-100"       // Hover state

// Layout
className="flex"                    // Flexbox
className="grid"                    // Grid
className="hidden md:flex"          // Responsive
```

---

## ✨ Common Framer Motion Patterns

```jsx
// Fade In
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} />

// Slide Up
<motion.div 
  initial={{ y: 20, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
/>

// Hover Scale
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
/>

// Exit Animation
<AnimatePresence>
  {isVisible && <motion.div exit={{ opacity: 0 }} />}
</AnimatePresence>
```

---

## 🔑 Key Features By Component

| Component | Key Features |
|-----------|-------------|
| **Sidebar** | Navigation, chat history, collapse/expand |
| **ChatWindow** | Messages, typing indicator, auto-scroll |
| **ChatInput** | File upload, voice, send, enhancements |
| **ChatMessage** | Markdown, copy button, timestamps |
| **TopSearch** | Search suggestions, animated dropdown |
| **ThemeToggle** | Dark/light mode with animation |
| **Home** | Landing page with features & prompts |
| **Discover** | 8 topic categories with subcategories |
| **Search** | Search tips and instructions |

---

## 💾 Data Structures

### Chat Object
```js
{
  id: "1234567890",
  title: "First Chat",
  messages: [
    {
      id: "msg1",
      content: "Hello!",
      isUser: true,
      timestamp: "2024-01-01T12:00:00Z",
      attachments: []
    }
  ],
  createdAt: "2024-01-01T12:00:00Z",
  updatedAt: "2024-01-01T12:05:00Z"
}
```

### Message Object
```js
{
  id: "unique-id",
  content: "Message text with **bold** and `code`",
  isUser: true,  // or false for AI
  timestamp: "2024-01-01T12:00:00Z",
  attachments: [
    {
      type: "image" | "file",
      file: File,
      preview: "base64string",
      name?: "filename",
      size?: 12345
    }
  ]
}
```

---

## 🔌 API Integration Template

```js
// In ChatWindow.jsx
import axios from 'axios';

const handleSendMessage = async (messageData) => {
  // Add user message first
  addMessage({
    content: messageData.content,
    isUser: true,
    timestamp: new Date().toISOString()
  });

  try {
    // Call your backend
    const response = await axios.post('/api/v1/chat', {
      message: messageData.content,
      chatId: currentChatId,
      attachments: messageData.attachments
    });

    // Add AI response
    addMessage({
      content: response.data.reply,
      isUser: false,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 🎯 Common Tasks

### Add a New Navigation Item
```jsx
// In Sidebar.jsx
const navItems = [
  { icon: Home, label: 'Home', path: '/' },
  // Add your new item:
  { icon: YourIcon, label: 'Your Label', path: '/yourpath' },
];
```

### Add a New Page
```js
// 1. Create src/pages/NewPage.jsx
// 2. Add to AppRouter.jsx
<Route path="/newpage" element={<NewPage />} />

// 3. Add to Sidebar navigation
```

### Change Colors
```js
// In tailwind.config.js
colors: {
  primary: { 500: '#your-color' },
  secondary: { 500: '#your-color' },
}
```

### Customize Animations
```jsx
// In any component
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}  // Change duration
/>
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Mic not working | Use Chrome/Edge/Safari, not Firefox |
| Styles not applied | Clear cache, restart dev server |
| Dark mode not working | Check theme context provider |
| Messages not saving | Check localStorage isn't disabled |
| Sidebar not collapsing | Verify Framer Motion is installed |

---

## 📚 File Descriptions

### Config Files
- **vite.config.js** - Vite build settings (port 3000)
- **tailwind.config.js** - Colors, animations, breakpoints
- **postcss.config.js** - CSS processing for Tailwind
- **package.json** - Dependencies and scripts

### Source Files
- **src/App.jsx** - Theme + Chat context wrappers
- **src/main.jsx** - React DOM render
- **src/AppRouter.jsx** - BrowserRouter + routes
- **src/index.css** - Tailwind directives

### Components (src/components/)
- **Sidebar.jsx** - Navigation + history
- **ChatWindow.jsx** - Main chat area
- **ChatMessage.jsx** - Message bubble
- **ChatInput.jsx** - Input + attachments
- **TopSearch.jsx** - Search bar
- **ThemeToggle.jsx** - Dark/light toggle
- **MicRecorderButton.jsx** - Voice input
- **ImageUploadButton.jsx** - Image upload
- **FileUploadButton.jsx** - File upload
- **FileUploadPreview.jsx** - Preview display

### Pages (src/pages/)
- **Home.jsx** - Landing page
- **Discover.jsx** - Topic exploration
- **Search.jsx** - Search page

### Context (src/context/)
- **ChatContext.jsx** - Chat state management
- **ThemeContext.jsx** - Theme management

---

## 🚀 Build & Deploy

```bash
# Development
npm run dev          # Start dev server

# Production
npm run build        # Create optimized build

# Preview built app
npm run preview      # Test production build
```

---

## 📱 Responsive Breakpoints

```
Default (Mobile):  < 768px
md (Tablet):       768px+
lg (Desktop):      1024px+
xl (Large Desktop):1280px+
```

Example:
```jsx
className="hidden md:flex"  // Hidden on mobile, flex on tablet+
className="text-sm md:text-lg"  // Small on mobile, large on tablet+
```

---

## 🎨 Color Palette

| Use Case | Light | Dark |
|----------|-------|------|
| Background | white | slate-950 |
| Secondary | gray-100 | slate-800 |
| Text | gray-900 | white |
| Primary | blue-500 | blue-500 |
| Accent | cyan-500 | cyan-500 |
| Border | gray-200 | slate-700 |

---

## 🔗 Useful Links

- [React Docs](https://react.dev)
- [Tailwind Docs](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)
- [React Router](https://reactrouter.com/)
- [Lucide Icons](https://lucide.dev/)

---

## 📞 Component Props Reference

### ChatMessage
```jsx
<ChatMessage 
  message={{ content: string, timestamp: string }}
  isUser={boolean}
/>
```

### ChatInput
```jsx
<ChatInput 
  onSendMessage={(data) => {}}
  isLoading={boolean}
/>
```

### MicRecorderButton
```jsx
<MicRecorderButton 
  onTranscript={(text) => {}}
/>
```

### ImageUploadButton
```jsx
<ImageUploadButton 
  onImageSelect={(imageData) => {}}
/>
```

### FileUploadButton
```jsx
<FileUploadButton 
  onFileSelect={(fileData) => {}}
/>
```

### FileUploadPreview
```jsx
<FileUploadPreview 
  uploads={array}
  onRemove={(index) => {}}
/>
```

---

**For detailed documentation, see:**
- 📖 `README.md` - Full feature overview
- 🛠️ `SETUP_GUIDE.md` - Installation & customization
- 🧩 `COMPONENTS.md` - Component API
- 🎨 `LAYOUT_GUIDE.md` - Visual layouts
- ✅ `FEATURES.md` - Complete checklist

---

**Created**: December 2024  
**Status**: Production Ready ✅