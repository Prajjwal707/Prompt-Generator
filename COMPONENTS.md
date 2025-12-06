# Component API Documentation

## Core Components

### Sidebar
**Location**: `src/components/Sidebar.jsx`

**Features**:
- Collapsible navigation menu
- Recent chats panel
- Mobile bottom navigation fallback
- Profile and Settings links

**Props**: None (uses Context API)

**Key Functions**:
- `createNewChat()` - Create new conversation
- `loadChat(chatId)` - Switch to different chat
- `deleteChat(chatId)` - Remove chat

**Responsive**: 
- Desktop: Full sidebar (64-256px wide)
- Mobile: Bottom navigation bar

---

### ChatWindow
**Location**: `src/components/ChatWindow.jsx`

**Features**:
- Message display with animations
- Auto-scroll to latest
- Typing indicator
- Empty state UI
- Header with action buttons

**Props**:
- None (uses Context API)

**Displays**:
- Current chat messages
- Typing animation
- Empty state with prompt

**Key Hooks**:
- `useChat()` - Access chat state
- `useRef()` - Message end reference
- `useEffect()` - Auto-scroll

---

### ChatMessage
**Location**: `src/components/ChatMessage.jsx`

**Props**:
```jsx
<ChatMessage 
  message={{ content: string, timestamp: ISO8601 }}
  isUser={boolean}
/>
```

**Features**:
- Message bubble styling (user vs AI)
- Copy to clipboard button
- Markdown rendering
- Code block highlighting
- Timestamp display
- Smooth animations

**Markdown Support**:
- Bold: `**text**`
- Code: `` `code` ``
- Links: `[text](url)`
- Code blocks: `` ```language code``` ``

---

### ChatInput
**Location**: `src/components/ChatInput.jsx`

**Props**:
```jsx
<ChatInput 
  onSendMessage={function(messageData)}
  isLoading={boolean}
/>
```

**Features**:
- Auto-expanding textarea
- File/image upload buttons
- Mic recording integration
- Enhancement options toggle
- Send button with loading state

**Keyboard Shortcuts**:
- Enter: Send message
- Shift+Enter: New line

**Message Data Structure**:
```js
{
  content: string,
  attachments: [
    {
      type: 'image' | 'file',
      file: File,
      preview: string,
      name?: string,
      size?: number
    }
  ]
}
```

---

### TopSearch
**Location**: `src/components/TopSearch.jsx`

**Features**:
- Global search bar
- Auto-suggest dropdown
- Animated suggestions
- Clear button

**Customization**:
Edit `allSuggestions` array to change suggestions:
```js
const allSuggestions = [
  'Your suggestion here',
];
```

**Responsive**: Hidden on mobile

---

### MicRecorderButton
**Location**: `src/components/MicRecorderButton.jsx`

**Props**:
```jsx
<MicRecorderButton 
  onTranscript={function(text: string)}
/>
```

**Features**:
- Browser Web Speech API integration
- Visual recording indicator
- Automatic speech detection
- Auto-stop on silence

**Requirements**:
- Chrome, Edge, or Safari
- HTTPS or localhost
- Microphone permissions

**Returns**: Transcript string via callback

---

### ImageUploadButton
**Location**: `src/components/ImageUploadButton.jsx`

**Props**:
```jsx
<ImageUploadButton 
  onImageSelect={function(imageData)}
/>
```

**Features**:
- Image file picker
- Automatic preview generation
- Base64 encoding

**Returned Data**:
```js
{
  file: File,
  preview: string (base64),
  type: 'image'
}
```

---

### FileUploadButton
**Location**: `src/components/FileUploadButton.jsx`

**Props**:
```jsx
<FileUploadButton 
  onFileSelect={function(fileData)}
/>
```

**Features**:
- Any file type support
- File metadata extraction
- Base64 preview

**Returned Data**:
```js
{
  file: File,
  name: string,
  size: number,
  type: string,
  preview: string
}
```

---

### FileUploadPreview
**Location**: `src/components/FileUploadPreview.jsx`

**Props**:
```jsx
<FileUploadPreview 
  uploads={array}
  onRemove={function(index)}
/>
```

**Features**:
- Image thumbnail preview
- File icon for documents
- Remove button on hover
- Animated entrance/exit

**Expected Upload Format**:
```js
[
  {
    type: 'image' | 'file',
    file: File,
    preview: string,
    name?: string
  }
]
```

---

### ThemeToggle
**Location**: `src/components/ThemeToggle.jsx`

**Features**:
- Light/dark mode toggle
- Animated sun/moon icon
- Stores preference

**No Props Required**

---

## Context API

### ChatContext
**Location**: `src/context/ChatContext.jsx`

**Usage**:
```js
const { 
  chats,              // Array of all chats
  currentChatId,      // Active chat ID
  getCurrentChat,     // Get current chat object
  createNewChat,      // Create and switch to new chat
  addMessage,         // Add message to current chat
  deleteChat,         // Remove chat by ID
  updateChatTitle,    // Update chat title
  loadChat           // Switch to different chat
} = useChat();
```

**Data Structure**:
```js
{
  id: string,
  title: string,
  messages: [
    {
      id: string,
      content: string,
      isUser: boolean,
      timestamp: ISO8601,
      attachments?: Array
    }
  ],
  createdAt: ISO8601,
  updatedAt: ISO8601
}
```

---

### ThemeContext
**Location**: `src/context/ThemeContext.jsx`

**Usage**:
```js
const { theme, toggleTheme } = useTheme();
// theme: 'light' | 'dark'
```

**Features**:
- Auto-detect system preference
- localStorage persistence
- HTML `dark` class management

---

## Page Components

### Home
**Location**: `src/pages/Home.jsx`

**Features**:
- Hero section with CTA
- Features showcase
- Example prompts
- Responsive grid layout

---

### Discover
**Location**: `src/pages/Discover.jsx`

**Features**:
- Topic categories (8 different)
- Expandable category cards
- Topic suggestions
- Click to start chat

**Categories Included**:
1. Programming
2. Business
3. Creative
4. Learning
5. Reference
6. Productivity
7. General Knowledge
8. Entertainment

---

### Search
**Location**: `src/pages/Search.jsx`

**Features**:
- Search tips display
- Placeholder content
- Animated layout

---

## Styling

### TailwindCSS Classes

**Key Color Classes**:
```
text-blue-500        # Primary blue
text-cyan-500        # Accent cyan
dark:bg-slate-900    # Dark background
dark:text-white      # Dark text
```

**Animation Classes**:
```
animate-fade-in      # Fade in animation
animate-slide-up     # Slide up animation
animate-pulse-glow   # Pulsing glow effect
```

**Component Classes**:
```
rounded-xl           # Large border radius
border-gray-200      # Light border
hover:scale-105      # Hover scale effect
```

---

## Framer Motion Usage

**Common Animations**:

```jsx
// Fade in
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
/>

// Slide up
<motion.div
  initial={{ y: 20, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
/>

// Scale on hover
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
/>
```

---

## Custom Hooks

### useChat()
Access chat state from any component:
```js
import { useChat } from '../context/ChatContext';

function MyComponent() {
  const { chats, createNewChat } = useChat();
  return <div>{chats.length} chats</div>;
}
```

### useTheme()
Access theme state from any component:
```js
import { useTheme } from '../context/ThemeContext';

function MyComponent() {
  const { theme, toggleTheme } = useTheme();
  return <button onClick={toggleTheme}>Toggle</button>;
}
```

---

## Component Tree

```
App
├── ThemeProvider
│   └── ChatProvider
│       └── AppRouter
│           ├── Sidebar
│           │   ├── NavItems
│           │   └── RecentChats
│           └── Main
│               ├── TopSearch
│               └── Routes
│                   ├── Home
│                   ├── Discover
│                   ├── Search
│                   └── ChatWindow
│                       ├── Header
│                       ├── Messages
│                       │   ├── ChatMessage
│                       │   └── TypingIndicator
│                       └── ChatInput
│                           ├── FileUploadPreview
│                           ├── Textarea
│                           ├── MicRecorderButton
│                           ├── ImageUploadButton
│                           ├── FileUploadButton
│                           └── SendButton
```

---

## Performance Considerations

1. **Message List**: Renders efficiently with AnimatePresence
2. **Chat History**: Filters limited to 10 items in sidebar
3. **Animations**: Uses GPU-accelerated transforms
4. **Re-renders**: Context API minimizes unnecessary updates
5. **localStorage**: Auto-syncs after state changes

---

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Basics | ✅ | ✅ | ✅ | ✅ |
| Voice API | ✅ | ❌ | ✅ | ✅ |
| localStorage | ✅ | ✅ | ✅ | ✅ |
| CSS Grid | ✅ | ✅ | ✅ | ✅ |

---

**Last Updated**: December 2024