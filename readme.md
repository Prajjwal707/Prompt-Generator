# PromptGenius - AI Chat Frontend

A modern, fully-featured AI chat interface built with React, combining the best design elements from Perplexity AI and ChatGPT.

## 🎨 Features

### UI/UX
- **Light & Dark Mode** - Auto-detects system preference with manual toggle
- **Glassmorphic Design** - Modern, clean interface with blur effects
- **Smooth Animations** - Powered by Framer Motion
- **Responsive Layout** - Mobile-first design with collapsible sidebar
- **Modern Icons** - Lucide React icons throughout

### Core Features
- **Chat Interface**
  - Message history with timestamps
  - Auto-scroll to latest messages
  - Typing indicators
  - Copy message functionality
  - Markdown support with code blocks

- **File Management**
  - Image upload and preview
  - File attachment with preview
  - Drag-and-drop support
  - File removal

- **Voice & Audio**
  - Speech-to-text recognition
  - Real-time transcript conversion
  - Mic recording button with visual feedback

- **Chat History**
  - Persistent chat storage (localStorage)
  - Previous chats panel
  - Quick access to recent conversations
  - Chat deletion

- **Search**
  - Global search with suggestions
  - Search across chats and prompts
  - Animated dropdown suggestions

- **Enhancement Tools**
  - Enhance prompt button
  - Rewrite suggestion
  - Regenerate response option

## 🛠️ Tech Stack

- **React 18.2** - UI library
- **Vite** - Build tool (fast HMR)
- **TailwindCSS 3.3** - Styling
- **Framer Motion 10.16** - Animations
- **React Router 6** - Navigation
- **Lucide React** - Icons
- **Zustand** (ready for state management)
- **Axios** (ready for API integration)

## 📁 Project Structure

```
Prompt-Generator/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx              # Navigation sidebar with chat history
│   │   ├── TopSearch.jsx            # Global search bar
│   │   ├── ChatWindow.jsx           # Main chat interface
│   │   ├── ChatMessage.jsx          # Individual message component
│   │   ├── ChatInput.jsx            # Input area with attachments
│   │   ├── FileUploadPreview.jsx    # File/image preview
│   │   ├── MicRecorderButton.jsx    # Voice recording
│   │   ├── ImageUploadButton.jsx    # Image upload
│   │   ├── FileUploadButton.jsx     # File upload
│   │   └── ThemeToggle.jsx          # Theme switcher
│   ├── pages/
│   │   ├── Home.jsx                 # Home page with features
│   │   ├── Discover.jsx             # Discovery/explore page
│   │   └── Search.jsx               # Search page
│   ├── context/
│   │   ├── ThemeContext.jsx         # Theme management
│   │   └── ChatContext.jsx          # Chat state management
│   ├── App.jsx                      # Main app wrapper
│   ├── AppRouter.jsx                # Route definitions
│   ├── main.jsx                     # React DOM entry
│   └── index.css                    # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── README.md
```

## 🚀 Getting Started

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

   The app will open at `http://localhost:3000`

3. **Build for production**
   ```bash
   npm run build
   ```

## 📱 Responsive Design

- **Desktop** (>768px)
  - Full sidebar navigation
  - Wide chat layout
  - Desktop-optimized inputs

- **Mobile** (<768px)
  - Bottom navigation bar
  - Collapsible sidebar
  - Touch-optimized buttons
  - Single-column layout

## 🎯 Key Components

### Sidebar (`Sidebar.jsx`)
- Collapsible navigation
- Quick new chat button
- Recent chats list
- Profile & Settings links
- Mobile bottom nav fallback

### Chat Window (`ChatWindow.jsx`)
- Message display with animations
- Auto-scroll functionality
- Typing indicator
- Header with action buttons
- Responsive layout

### Chat Input (`ChatInput.jsx`)
- Auto-expanding textarea
- File/image attachment
- Voice recording integration
- Send button with loading state
- Enhancement options toggle
- Shift+Enter for new line

### Context API

**ThemeContext**: Manages light/dark mode with localStorage persistence

**ChatContext**: Manages chat state including:
- Chat creation and deletion
- Message history
- Current chat selection
- localStorage sync

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change the color scheme:
```js
colors: {
  primary: { /* your colors */ },
  secondary: { /* your colors */ },
  accent: { /* your colors */ }
}
```

### Animations
Framer Motion variants are defined in each component for easy customization.

### Theme
System preference is detected automatically on first load. Users can toggle manually with the theme button.

## 💾 Data Persistence

- **Chat History**: Stored in localStorage as JSON
- **Theme Preference**: Saved to localStorage
- **Current Chat**: Session tracking via localStorage

## 🔌 API Integration Ready

The app is structured to integrate with a backend:

```javascript
// In ChatInput.jsx or ChatWindow.jsx
const response = await axios.post('/api/chat', {
  message: content,
  chatId: currentChatId,
  attachments: uploads
});
```

## 🌐 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers with ES6 support

## 📝 Features Not Yet Implemented

These are ready to add:
- Real API integration
- User authentication
- Chat export/sharing
- Prompt templates
- Custom system prompts
- Rate limiting UI
- Settings page

## 🤝 Contributing

The codebase is organized and modular for easy extension:

1. Add new components to `src/components/`
2. Add new pages to `src/pages/`
3. Extend context in `src/context/`
4. Update routes in `AppRouter.jsx`

## 📄 License

MIT License - Feel free to use this project!

## 🙏 Credits

- UI Inspiration: Perplexity AI, ChatGPT
- Icons: Lucide React
- Animations: Framer Motion
- Styling: Tailwind CSS

---

**Built with ❤️ for modern AI chat interfaces**

Original Team: Saloni Tanishq Gauranshi