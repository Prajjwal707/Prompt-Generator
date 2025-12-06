# PromptGenius - Visual Layout Guide

## 🎨 Desktop Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐  ┌─────────────────────────────────────────────┐│
│  │ SIDEBAR  │  │           TOP SEARCH BAR                    ││
│  │          │  └─────────────────────────────────────────────┘│
│  │ Logo     │  ┌─────────────────────────────────────────────┐│
│  │ ────────│  │                                             ││
│  │ New Chat │  │         CHAT MESSAGES AREA                  ││
│  │ ────────│  │                                             ││
│  │ Home     │  │  User:  "Hello, how are you?"          ──→ ││
│  │ Discover │  │                                             ││
│  │ Search   │  │  AI: "I'm doing great! How can I help? ←── ││
│  │ ────────│  │                                             ││
│  │ HISTORY  │  │  User: "Tell me about React"           ──→ ││
│  │ • Chat 1 │  │                                             ││
│  │ • Chat 2 │  │  AI: "React is a JavaScript library..." ←── ││
│  │ • Chat 3 │  │                                             ││
│  │ ────────│  ├─────────────────────────────────────────────┤│
│  │ Profile  │  │ 🖼️  📎  Input Box  🎤  ➤ SEND             ││
│  │ Settings │  └─────────────────────────────────────────────┘│
│  │          │                                                 │
│  └──────────┘                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📱 Mobile Layout (< 768px)

```
┌─────────────────────────────────────────────┐
│ PromptGenius  [🎤][📤][📎][+][🌙]           │
├─────────────────────────────────────────────┤
│                                             │
│         CHAT MESSAGES AREA                  │
│                                             │
│  User: "Hello"                          ──→ │
│                                             │
│  AI: "Hi there!"                        ←── │
│                                             │
│  User: "How are you?"                   ──→ │
│                                             │
│  AI: "Doing well!"                      ←── │
│                                             │
├─────────────────────────────────────────────┤
│ [🖼️] [🎤] [📎] [Input Box...] [➤]           │
├─────────────────────────────────────────────┤
│ [🏠] [🔍] [🗺️] [💬] [+]                    │
└─────────────────────────────────────────────┘
```

## 🧩 Component Hierarchy

```
App (Dark/Light Theme Wrapper)
│
├── ThemeProvider
│   │
│   └── ChatProvider
│       │
│       └── AppRouter
│           │
│           ├── Sidebar
│           │   ├── Logo "PromptGenius"
│           │   ├── New Chat Button
│           │   ├── Navigation Menu
│           │   │   ├── Home
│           │   │   ├── Discover
│           │   │   ├── Search
│           │   │   └── New Chat
│           │   ├── History Section
│           │   │   └── [Recent Chats List]
│           │   └── Footer Section
│           │       ├── Profile
│           │       └── Settings
│           │
│           └── Main Content Area
│               ├── TopSearch (Desktop Only)
│               │   ├── Search Input
│               │   └── Suggestions Dropdown
│               │
│               └── Routes
│                   ├── / (Home)
│                   │   ├── Hero Section
│                   │   ├── Features Grid
│                   │   └── Example Prompts
│                   │
│                   ├── /discover (Discover)
│                   │   ├── Header
│                   │   └── Category Grid
│                   │       ├── Programming
│                   │       ├── Business
│                   │       ├── Creative
│                   │       ├── Learning
│                   │       ├── Reference
│                   │       ├── Productivity
│                   │       ├── General Knowledge
│                   │       └── Entertainment
│                   │
│                   ├── /search (Search)
│                   │   └── Search Tips
│                   │
│                   └── /chat (ChatWindow)
│                       ├── Header
│                       │   ├── Title
│                       │   └── Action Buttons
│                       ├── Messages Container
│                       │   ├── ChatMessage (User)
│                       │   ├── ChatMessage (AI)
│                       │   └── Typing Indicator
│                       └── ChatInput
│                           ├── FileUploadPreview
│                           ├── Textarea
│                           ├── Enhancement Options
│                           ├── Button Row
│                           │   ├── ImageUploadButton
│                           │   ├── MicRecorderButton
│                           │   ├── FileUploadButton
│                           │   └── Send Button
│                           └── Theme Toggle
```

## 🎨 Color Scheme

### Light Mode
```
Background:     #FFFFFF (white)
Secondary:      #F1F5F9 (light gray)
Borders:        #E2E8F0 (light gray)
Text:           #0F172A (dark gray)
Primary:        #3B82F6 (blue)
Accent:         #06B6D4 (cyan)
```

### Dark Mode
```
Background:     #0F172A (very dark blue)
Secondary:      #1E293B (dark blue-gray)
Tertiary:       #334155 (medium gray-blue)
Borders:        #475569 (medium gray)
Text:           #FFFFFF (white)
Primary:        #3B82F6 (blue)
Accent:         #06B6D4 (cyan)
```

## 🎯 Chat Message Styling

### User Message (Right-aligned)
```
┌────────────────────────────────────────┐
│                                        │
│                                        │
│          ┌──────────────────────────┐  │
│          │ This is my question      │  │
│          │ about React.             │  │
│          └──────────────────────────┘  │
│               👤 You    12:34 PM       │
│                                        │
```

### AI Message (Left-aligned)
```
┌────────────────────────────────────────┐
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Great question! Here's what I    │  │
│  │ know about React:                │  │
│  │                                  │  │
│  │ ```javascript                    │  │
│  │ const Hello = () => <h1>Hi!</h1> │  │
│  │ ```                              │  │
│  └──────────────────────────────────┘  │
│  🤖 AI    12:34 PM                     │
│                                        │
```

## 📐 Responsive Breakpoints

### Tailwind MD Breakpoint (768px)
- Sidebar switches from full-width to mobile nav
- Chat layout from two-column to full-width
- Top search bar hidden on mobile

```
Desktop (> 768px):
┌────────┬──────────────────────────┐
│        │                          │
│ SIDEBAR│    MAIN CONTENT          │
│        │                          │
└────────┴──────────────────────────┘

Mobile (< 768px):
┌──────────────────────────────┐
│     MAIN CONTENT             │
│                              │
│                              │
├──────────────────────────────┤
│ [NAV ICONS]                  │
└──────────────────────────────┘
```

## 🎬 Animation Flows

### Message Appearance
```
Message enters:
1. Scale: 0.8 → 1.0
2. Opacity: 0 → 1
3. Y-position: +10px → 0px
Duration: 0.3s ease-out
```

### Typing Indicator
```
Dots bounce:
• First dot:  y: 0 → -8px → 0 (delay: 0ms)
• Second dot: y: 0 → -8px → 0 (delay: 100ms)
• Third dot:  y: 0 → -8px → 0 (delay: 200ms)
Duration: 0.6s infinite
```

### Button Interactions
```
Hover:  scale: 1.0 → 1.05
Click:  scale: 1.0 → 0.95
Duration: 0.2s
```

## 📊 Layout Specifications

### Sidebar (Desktop)
```
Expanded:  Width: 16rem (256px)
Collapsed: Width: 5rem (80px)
Height:    100vh (full screen)
Transition: 300ms ease
```

### Chat Input
```
Height:      Auto-expand (1-5 lines)
Min height:  48px
Max height:  200px
Padding:     16px
Border radius: 12px
```

### Message Bubbles
```
Max width:   75% of container
Min width:   Fit content
Padding:     12px 16px
Border radius: 16px
```

## 🎨 Theme Toggle Position

```
Desktop (Top-right corner):
┌──────────────────────────┐
│         [🌙]             │
│                          │
│    Main Content          │
│                          │
└──────────────────────────┘

Mobile (Top-right header):
┌────────────────┐
│ Title  [🌙][+] │
├────────────────┤
│   Content      │
└────────────────┘
```

## 📱 Bottom Navigation (Mobile)

```
┌────────────────────────────────┐
│   Main Content Area            │
│                                │
├────────────────────────────────┤
│ [🏠] [🔍] [🗺️] [💬] [+]         │
│ Home Search Discover Chat  New  │
└────────────────────────────────┘
```

## 🎯 Input Area Layout

```
┌─────────────────────────────────────────┐
│ 🖼️ 🎤 [Textarea input field...] 📎 ➤   │
│                                         │
│ [Enhancement options toggle]            │
│ [✨ Enhance] [✏️ Rewrite] [🔄 Regen]    │
└─────────────────────────────────────────┘
```

## 🗂️ File Upload Preview

```
Before upload:
[Empty state - only input visible]

After image upload:
┌─────────────────────────┐
│ [📷 thumbnail.jpg] [X]  │
│ [🖼️ image_preview.png] [X]
├─────────────────────────┤
│ Input field...          │
└─────────────────────────┘

After file upload:
┌──────────────────────────┐
│ [📄 document.pdf] [X]    │
│ [📎 data.xlsx] [X]      │
├──────────────────────────┤
│ Input field...           │
└──────────────────────────┘
```

## 🎨 Gradient Buttons

```
Primary Button (Blue to Cyan):
┌──────────────────────────────┐
│  from-blue-500 to-cyan-500   │
│  →→→→→→→→→→→→→→→            │
│  Send Message                │
└──────────────────────────────┘

Secondary Button (Gray):
┌──────────────────────────────┐
│  bg-gray-100 dark:bg-slate-800
│  hover:bg-gray-200           │
│  New Chat                    │
└──────────────────────────────┘
```

## 📐 Spacing & Sizing

```
Standard Spacing:
- 4px (xs)  - Icon margins
- 8px (sm)  - Compact spacing
- 12px (md) - Component padding
- 16px (lg) - Section padding
- 24px (xl) - Major sections

Component Heights:
- Buttons:      40-48px
- Input:        48-56px (auto-expand)
- Header:       64px
- Sidebar:      100vh
- Chat bubble:  Auto (min 44px)
```

---

**This layout is fully responsive and adapts seamlessly from mobile to desktop! 🚀**