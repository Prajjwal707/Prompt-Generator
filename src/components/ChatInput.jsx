import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader, AlertCircle } from 'lucide-react';
import MicRecorderButton from './MicRecorderButton';
import ImageUploadButton from './ImageUploadButton';
import FileUploadButton from './FileUploadButton';
import FileUploadPreview from './FileUploadPreview';
import { useChat } from '../context/ChatContext';

export default function ChatInput({ onSendMessage, isLoading }) {
  const [message, setMessage] = useState('');
  const [uploads, setUploads] = useState([]);
  const [showEnhance, setShowEnhance] = useState(false);
  const [validationError, setValidationError] = useState('');
  const textareaRef = useRef(null);
  const { activeTaskType } = useChat();

  // Auto-expand textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(
        textareaRef.current.scrollHeight,
        200
      ) + 'px';
    }
  }, [message]);

  const handleSendMessage = () => {
    if (!activeTaskType) {
      setValidationError('Please choose a task type before sending your prompt.');
      setTimeout(() => setValidationError(''), 4000);
      return;
    }

    if (message.trim()) {
      onSendMessage({
        content: message,
        attachments: uploads.length > 0 ? uploads : undefined,
      });
      setMessage('');
      setUploads([]);
      setValidationError('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleImageSelect = (image) => {
    setUploads([...uploads, image]);
  };

  const handleFileSelect = (file) => {
    setUploads([...uploads, file]);
  };

  const handleRemoveUpload = (index) => {
    setUploads(uploads.filter((_, i) => i !== index));
  };

  const handleTranscript = (text) => {
    setMessage(prev => prev + (prev ? ' ' : '') + text);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="border-t border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-4"
    >
      {/* Validation Error */}
      <AnimatePresence>
        {validationError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-3 px-4 py-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 flex gap-2 items-center"
          >
            <AlertCircle size={18} className="text-red-500 flex-shrink-0" />
            <p className="text-sm text-red-700 dark:text-red-400">{validationError}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* File Preview */}
      <FileUploadPreview uploads={uploads} onRemove={handleRemoveUpload} />

      {/* Enhancement Buttons */}
      <AnimatePresence>
        {showEnhance && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex gap-2 mb-3 px-4 flex-wrap"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-3 py-1 text-sm rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50 transition"
            >
              ✨ Enhance
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-3 py-1 text-sm rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 hover:bg-purple-200 dark:hover:bg-purple-900/50 transition"
            >
              ✏️ Rewrite
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-3 py-1 text-sm rounded-full bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 hover:bg-green-200 dark:hover:bg-green-900/50 transition"
            >
              🔄 Regenerate
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input Area */}
      <div className="flex gap-2 px-4 items-end">
        <div className="flex-1 flex gap-2 items-end">
          {/* Input Field */}
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything or drop files…"
            rows={1}
            className="flex-1 px-4 py-3 rounded-xl bg-gray-100 dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition max-h-48"
          />

          {/* Icon Buttons */}
          <div className="flex gap-1">
            <ImageUploadButton onImageSelect={handleImageSelect} />
            <MicRecorderButton onTranscript={handleTranscript} />
            <FileUploadButton onFileSelect={handleFileSelect} />
          </div>
        </div>

        {/* Send Button */}
        <motion.button
          onClick={handleSendMessage}
          disabled={isLoading || !message.trim()}
          className={`flex-shrink-0 p-3 rounded-full transition ${
            isLoading || !message.trim()
              ? 'bg-gray-200 dark:bg-slate-700 text-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white cursor-pointer'
          }`}
          whileHover={!isLoading && message.trim() ? { scale: 1.05 } : {}}
          whileTap={!isLoading && message.trim() ? { scale: 0.95 } : {}}
        >
          {isLoading ? (
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity }}>
              <Loader size={20} />
            </motion.div>
          ) : (
            <Send size={20} />
          )}
        </motion.button>
      </div>

      {/* Enhancement Toggle */}
      <motion.button
        onClick={() => setShowEnhance(!showEnhance)}
        className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 mt-2 px-4 transition"
      >
        {showEnhance ? '▼ Hide' : '▶ Show'} enhancement options
      </motion.button>
    </motion.div>
  );
}
