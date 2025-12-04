import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, X } from 'lucide-react';

export default function TopSearch() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const allSuggestions = [
    'How to use React hooks effectively',
    'Best practices for AI prompt engineering',
    'Understanding machine learning models',
    'Web development trends 2024',
    'Python vs JavaScript comparison',
  ];

  const handleSearch = (value) => {
    setQuery(value);
    if (value.length > 0) {
      const filtered = allSuggestions.filter(s =>
        s.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setShowSuggestions(false);
  };

  return (
    <div className="hidden md:flex justify-center px-4 py-4">
      <motion.div
        className="w-full max-w-2xl relative"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            onFocus={() => query && setShowSuggestions(true)}
            placeholder="Search chats, prompts, documents..."
            className="w-full px-4 py-3 pl-10 rounded-xl bg-gray-100 dark:bg-slate-800 border border-gray-300 dark:border-slate-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          />
          {query && (
            <button
              onClick={() => {
                setQuery('');
                setShowSuggestions(false);
              }}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X size={18} />
            </button>
          )}
        </div>

        {/* Suggestions Dropdown */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{
            opacity: showSuggestions && suggestions.length > 0 ? 1 : 0,
            y: showSuggestions && suggestions.length > 0 ? 0 : -10,
          }}
          className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 overflow-hidden z-50"
        >
          {suggestions.map((suggestion, idx) => (
            <motion.button
              key={idx}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full text-left px-4 py-3 hover:bg-gray-100 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-slate-700 last:border-b-0 transition"
              whileHover={{ x: 4 }}
            >
              <Search size={14} className="inline mr-2 text-gray-400" />
              {suggestion}
            </motion.button>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}
