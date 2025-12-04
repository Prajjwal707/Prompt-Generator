import React from 'react';
import { motion } from 'framer-motion';
import { Search as SearchIcon } from 'lucide-react';

export default function Search() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex-1 overflow-y-auto pb-20 md:pb-0 flex items-center justify-center px-4"
    >
      <div className="text-center max-w-2xl">
        <motion.div
          className="text-6xl mb-6"
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          🔍
        </motion.div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Search Your Conversations
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          Use the search bar at the top to find past conversations, saved prompts, and documents.
        </p>

        <motion.div
          className="bg-white dark:bg-slate-800 rounded-xl p-8 border border-gray-200 dark:border-slate-700"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Search Tips
          </h2>
          <div className="space-y-3 text-left">
            <div className="flex gap-3">
              <SearchIcon className="text-blue-500 flex-shrink-0" size={20} />
              <span className="text-gray-700 dark:text-gray-300">
                Search across all your previous chats
              </span>
            </div>
            <div className="flex gap-3">
              <SearchIcon className="text-blue-500 flex-shrink-0" size={20} />
              <span className="text-gray-700 dark:text-gray-300">
                Find specific topics and keywords
              </span>
            </div>
            <div className="flex gap-3">
              <SearchIcon className="text-blue-500 flex-shrink-0" size={20} />
              <span className="text-gray-700 dark:text-gray-300">
                Quick access to saved documents
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
