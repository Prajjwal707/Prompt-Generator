import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Copy, Check } from 'lucide-react';
import { useState } from 'react';

export default function ChatMessage({ message, isUser }) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const messageVariants = {
    initial: { opacity: 0, y: 10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -10 },
  };

  // Simple markdown to HTML conversion
  const renderContent = (text) => {
    // Code block detection
    const codeBlockRegex = /```(.*?)\n([\s\S]*?)```/g;
    const inlineCodeRegex = /`([^`]+)`/g;
    const boldRegex = /\*\*(.*?)\*\*/g;
    const linkRegex = /\[(.*?)\]\((.*?)\)/g;

    let html = text
      .replace(codeBlockRegex, (match, lang, code) => {
        return `<pre class="bg-gray-900 text-gray-100 p-3 rounded-lg overflow-x-auto my-2"><code>${code.trim()}</code></pre>`;
      })
      .replace(inlineCodeRegex, '<code class="bg-gray-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">$1</code>')
      .replace(boldRegex, '<strong class="font-bold">$1</strong>')
      .replace(linkRegex, '<a href="$2" target="_blank" class="text-blue-500 hover:underline">$1</a>');

    return html;
  };

  return (
    <motion.div
      variants={messageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className={`flex gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-cyan-500'
            : 'bg-gradient-to-br from-purple-500 to-pink-500'
        }`}
      >
        {isUser ? 'You' : 'AI'}
      </div>

      {/* Message Bubble */}
      <motion.div
        className={`max-w-xs md:max-w-md lg:max-w-xl relative group ${
          isUser ? 'flex-row-reverse' : ''
        }`}
        whileHover={{ scale: 1.01 }}
      >
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-br-none'
              : 'bg-gray-100 dark:bg-slate-700 text-gray-900 dark:text-white rounded-bl-none'
          }`}
        >
          <div
            className="text-sm leading-relaxed break-words"
            dangerouslySetInnerHTML={{ __html: renderContent(message.content) }}
          />
        </div>

        {/* Copy Button */}
        <motion.button
          onClick={copyToClipboard}
          className={`opacity-0 group-hover:opacity-100 p-1 rounded transition absolute ${
            isUser ? 'right-0 -left-10' : 'left-0 -right-10'
          } top-1/2 -translate-y-1/2`}
          whileHover={{ scale: 1.1 }}
        >
          {copied ? (
            <Check size={16} className="text-green-500" />
          ) : (
            <Copy size={16} className="text-gray-500 dark:text-gray-400" />
          )}
        </motion.button>
      </motion.div>

      {/* Time */}
      <motion.span
        className="text-xs text-gray-400 dark:text-gray-500 self-end"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </motion.span>
    </motion.div>
  );
}
