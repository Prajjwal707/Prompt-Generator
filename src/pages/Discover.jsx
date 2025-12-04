import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Code,
  Lightbulb,
  Palette,
  Brain,
  BookMarked,
  Zap,
  Globe,
  Headphones,
} from 'lucide-react';
import { useChat } from '../context/ChatContext';

export default function Discover() {
  const { createNewChat } = useChat();
  const [selectedCategory, setSelectedCategory] = useState(null);

  const categories = [
    {
      icon: Code,
      title: 'Programming',
      description: 'Learn coding, debugging, and development best practices',
      topics: ['JavaScript', 'Python', 'React', 'Web Development', 'DevOps'],
    },
    {
      icon: Lightbulb,
      title: 'Business',
      description: 'Startup ideas, growth strategies, and business insights',
      topics: ['Entrepreneurship', 'Marketing', 'Sales', 'Leadership', 'Analytics'],
    },
    {
      icon: Palette,
      title: 'Creative',
      description: 'Writing, design, and creative problem-solving',
      topics: ['Content Writing', 'Design Thinking', 'UX/UI', 'Storytelling', 'Art'],
    },
    {
      icon: Brain,
      title: 'Learning',
      description: 'Educational content and skill development',
      topics: ['Math', 'Science', 'History', 'Languages', 'Online Learning'],
    },
    {
      icon: BookMarked,
      title: 'Reference',
      description: 'Documentation, explanations, and reference materials',
      topics: ['APIs', 'Frameworks', 'Standards', 'Tools', 'Guides'],
    },
    {
      icon: Zap,
      title: 'Productivity',
      description: 'Optimization, automation, and efficiency tips',
      topics: ['Time Management', 'Workflows', 'Tools', 'Automation', 'Habits'],
    },
    {
      icon: Globe,
      title: 'General Knowledge',
      description: 'Curious about the world? Ask anything',
      topics: ['News', 'Culture', 'Nature', 'Society', 'Technology'],
    },
    {
      icon: Headphones,
      title: 'Entertainment',
      description: 'Movies, music, games, and pop culture',
      topics: ['Movies', 'Music', 'Gaming', 'Books', 'Pop Culture'],
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex-1 overflow-y-auto pb-20 md:pb-0"
    >
      {/* Header */}
      <motion.section
        className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-slate-900 dark:to-slate-800 py-12 px-4"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Discover Topics
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Explore different categories and find what interests you
          </p>
        </div>
      </motion.section>

      {/* Categories Grid */}
      <section className="py-16 px-4 max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category, idx) => {
            const Icon = category.icon;
            const isSelected = selectedCategory === idx;

            return (
              <motion.button
                key={idx}
                onClick={() => setSelectedCategory(isSelected ? null : idx)}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`p-6 rounded-xl border-2 transition text-left ${
                  isSelected
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-blue-300 dark:hover:border-blue-600'
                }`}
              >
                <Icon
                  className={`mb-4 ${
                    isSelected ? 'text-blue-600' : 'text-gray-600 dark:text-gray-400'
                  }`}
                  size={32}
                />
                <h3 className="font-bold text-gray-900 dark:text-white mb-2">
                  {category.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {category.description}
                </p>

                {/* Topics */}
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{
                    height: isSelected ? 'auto' : 0,
                    opacity: isSelected ? 1 : 0,
                  }}
                  className="overflow-hidden"
                >
                  <div className="space-y-2 pt-4 border-t border-gray-200 dark:border-slate-700">
                    {category.topics.map((topic, topicIdx) => (
                      <motion.button
                        key={topicIdx}
                        onClick={(e) => {
                          e.stopPropagation();
                          createNewChat();
                        }}
                        className="w-full text-left px-3 py-2 rounded-lg bg-gray-100 dark:bg-slate-700 text-sm text-gray-700 dark:text-gray-300 hover:bg-blue-200 dark:hover:bg-blue-900/30 transition"
                        whileHover={{ x: 4 }}
                      >
                        → {topic}
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              </motion.button>
            );
          })}
        </div>
      </section>
    </motion.div>
  );
}
