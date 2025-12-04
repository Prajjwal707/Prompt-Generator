import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Upload, Paperclip, Plus } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ThemeToggle from './ThemeToggle';
import TaskTypeSelector from './TaskTypeSelector';
import { useChat } from '../context/ChatContext';

export default function ChatWindow() {
  const { currentChatId, getCurrentChat, createNewChat, addMessage, activeTaskType, setActiveTaskType } = useChat();
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [typingMessage, setTypingMessage] = useState(null);

  const currentChat = getCurrentChat();
  const messages = currentChat?.messages || [];
  const showTaskSelector = messages.length === 0 && !activeTaskType;

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typingMessage]);

  // Initialize chat if none exists
  useEffect(() => {
    if (!currentChatId) {
      createNewChat();
    }
  }, [currentChatId, createNewChat]);

  const handleSendMessage = async (messageData) => {
    if (!currentChatId || !activeTaskType) {
      alert('Please choose a task type before sending your prompt.');
      return;
    }

    // Add user message
    const userMessage = {
      content: messageData.content,
      isUser: true,
      timestamp: new Date().toISOString(),
      attachments: messageData.attachments,
    };

    addMessage(userMessage);
    setIsLoading(true);
    setTypingMessage('...');

    try {
      // Make API call to backend
      const response = await fetch('/api/enhance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: messageData.content,
          task_type: activeTaskType,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to enhance prompt');
      }

      const data = await response.json();
      setTypingMessage(null);

      // Add AI message with enhanced prompt
      const aiMessage = {
        content: data.enhanced_prompt || data.response || 'Enhanced prompt generated successfully.',
        isUser: false,
        timestamp: new Date().toISOString(),
      };

      addMessage(aiMessage);
    } catch (error) {
      console.error('Error:', error);
      setTypingMessage(null);

      // Show error message
      const errorMessage = {
        content: 'Sorry, there was an error processing your request. Please try again.',
        isUser: false,
        timestamp: new Date().toISOString(),
      };

      addMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (!currentChatId) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-slate-950 dark:to-slate-900">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="text-5xl mb-4">💬</div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            PromptGenius
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Your AI companion for any question
          </p>
          <motion.button
            onClick={createNewChat}
            className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-medium hover:from-blue-600 hover:to-cyan-600 transition"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Start New Chat
          </motion.button>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-screen bg-white dark:bg-slate-950"
    >
      {/* Header */}
      <motion.header
        className="border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 sticky top-0 z-40"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="flex items-center justify-between p-4 md:px-6">
          <h1 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
            PromptGenius
          </h1>

          <div className="flex items-center gap-3">
            <motion.button
              className="hidden sm:flex items-center gap-2 p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition"
              whileHover={{ scale: 1.05 }}
            >
              <Mic size={20} className="text-gray-600 dark:text-gray-400" />
            </motion.button>
            <motion.button
              className="hidden sm:flex items-center gap-2 p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition"
              whileHover={{ scale: 1.05 }}
            >
              <Upload size={20} className="text-gray-600 dark:text-gray-400" />
            </motion.button>
            <motion.button
              className="hidden sm:flex items-center gap-2 p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition"
              whileHover={{ scale: 1.05 }}
            >
              <Paperclip size={20} className="text-gray-600 dark:text-gray-400" />
            </motion.button>
            <motion.button
              onClick={createNewChat}
              className="flex items-center gap-2 p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition"
              whileHover={{ scale: 1.05 }}
            >
              <Plus size={20} className="text-gray-600 dark:text-gray-400" />
            </motion.button>
            <ThemeToggle />
          </div>
        </div>
      </motion.header>

      {/* Messages */}
      <motion.div
        className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <AnimatePresence mode="popLayout">
          {messages.length === 0 && !activeTaskType ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex items-center justify-center h-full text-center"
            >
              <div>
                <div className="text-6xl mb-4">✨</div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Select a Task Type
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  Choose what you'd like to create to get started
                </p>
              </div>
            </motion.div>
          ) : (
            <>
              {messages.map((msg, idx) => (
                <ChatMessage
                  key={idx}
                  message={msg}
                  isUser={msg.isUser}
                />
              ))}

              {typingMessage && (
                <motion.div
                  key="typing"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                    AI
                  </div>
                  <div className="bg-gray-100 dark:bg-slate-700 px-4 py-3 rounded-2xl rounded-bl-none">
                    <motion.div
                      className="flex gap-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      {[0, 1, 2].map((i) => (
                        <motion.div
                          key={i}
                          className="w-2 h-2 rounded-full bg-gray-400"
                          animate={{ y: [0, -8, 0] }}
                          transition={{
                            duration: 0.6,
                            delay: i * 0.1,
                            repeat: Infinity,
                          }}
                        />
                      ))}
                    </motion.div>
                  </div>
                </motion.div>
              )}
            </>
          )}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </motion.div>

      {/* Input Area with Task Selector */}
      <div>
        {showTaskSelector && (
          <div className="px-4 md:px-6 py-4">
            <TaskTypeSelector selected={activeTaskType} onSelect={setActiveTaskType} />
          </div>
        )}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>

      {/* Mobile padding for bottom nav */}
      <div className="md:hidden h-16" />
    </motion.div>
  );
}
