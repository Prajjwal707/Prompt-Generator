import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  Compass,
  Search,
  MessageSquare,
  Clock,
  Settings,
  User,
  ChevronLeft,
  ChevronRight,
  Plus,
  Trash2,
} from 'lucide-react';
import { useChat } from '../context/ChatContext';
import { useTheme } from '../context/ThemeContext';
import { Link, useLocation, useNavigate } from 'react-router-dom';

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const { chats, currentChatId, createNewChat, deleteChat, loadChat } = useChat();
  const { theme } = useTheme();
  const location = useLocation();

  const handleNewChat = () => {
    const newChat = createNewChat();
    navigate(`/chat/${newChat.id}`);
  };

  const navItems = [
    { icon: Home, label: 'Home', path: '/' },
    { icon: Compass, label: 'Discover', path: '/discover' },
    { icon: Search, label: 'Search', path: '/search' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.aside
        className={`hidden md:flex flex-col h-screen bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-700 transition-all duration-300 ${
          collapsed ? 'w-20' : 'w-64'
        }`}
        initial={false}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4">
          {!collapsed && (
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
              PromptGenius
            </h1>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition"
          >
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          </button>
        </div>

        {/* New Chat Button */}
        <motion.button
          onClick={handleNewChat}
          className={`flex items-center gap-3 mx-3 p-3 rounded-lg bg-blue-500 hover:bg-blue-600 text-white transition mb-4 ${
            collapsed ? 'justify-center' : ''
          }`}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Plus size={20} />
          {!collapsed && <span>New Chat</span>}
        </motion.button>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto">
          {/* Main Nav */}
          <div className="space-y-1 px-3 mb-6">
            {navItems.map(({ icon: Icon, label, path }) => (
              <Link key={path} to={path}>
                <motion.button
                  className={`w-full flex items-center gap-3 p-3 rounded-lg transition ${
                    isActive(path)
                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800'
                  } ${collapsed ? 'justify-center' : ''}`}
                  whileHover={{ x: collapsed ? 0 : 4 }}
                >
                  <Icon size={20} />
                  {!collapsed && <span>{label}</span>}
                </motion.button>
              </Link>
            ))}
          </div>

          {/* History */}
          {!collapsed && (
            <div className="px-3">
              <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-3">
                RECENT CHATS
              </p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                <AnimatePresence mode="popLayout">
                  {chats.slice(0, 10).map(chat => (
                    <motion.div
                      key={chat.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      className={`flex items-center gap-2 p-2 rounded-lg cursor-pointer group transition ${
                        currentChatId === chat.id
                          ? 'bg-blue-100 dark:bg-blue-900/30'
                          : 'hover:bg-gray-100 dark:hover:bg-slate-800'
                      }`}
                      onClick={() => loadChat(chat.id)}
                    >
                      <Clock size={16} className="flex-shrink-0" />
                      <span className="text-sm flex-1 truncate text-gray-700 dark:text-gray-300">
                        {chat.title}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteChat(chat.id);
                        }}
                        className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 dark:hover:bg-red-900/30 rounded transition"
                      >
                        <Trash2 size={14} className="text-red-500" />
                      </button>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>
          )}
        </nav>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-slate-700 p-3 space-y-2">
          <motion.button
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition ${
              collapsed ? 'justify-center' : ''
            }`}
            whileHover={{ x: collapsed ? 0 : 4 }}
          >
            <User size={20} />
            {!collapsed && <span>Profile</span>}
          </motion.button>
          <motion.button
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition ${
              collapsed ? 'justify-center' : ''
            }`}
            whileHover={{ x: collapsed ? 0 : 4 }}
          >
            <Settings size={20} />
            {!collapsed && <span>Settings</span>}
          </motion.button>
        </div>
      </motion.aside>

      {/* Mobile Bottom Navigation */}
      <motion.nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-slate-700 flex justify-around p-2">
        {navItems.map(({ icon: Icon, label, path }) => (
          <Link key={path} to={path}>
            <motion.button
              className={`flex flex-col items-center gap-1 p-3 rounded-lg transition ${
                isActive(path)
                  ? 'text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400'
              }`}
              whileTap={{ scale: 0.9 }}
            >
              <Icon size={24} />
              <span className="text-xs">{label}</span>
            </motion.button>
          </Link>
        ))}
        <motion.button
          onClick={createNewChat}
          className="flex flex-col items-center gap-1 p-3 rounded-lg text-blue-600 dark:text-blue-400 transition"
          whileTap={{ scale: 0.9 }}
        >
          <Plus size={24} />
          <span className="text-xs">New</span>
        </motion.button>
      </motion.nav>
    </>
  );
}
