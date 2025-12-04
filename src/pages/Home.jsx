import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sparkles, Zap, BookOpen, TrendingUp } from 'lucide-react';
import { useChat } from '../context/ChatContext';

export default function Home() {
  const navigate = useNavigate();
  const { createNewChat } = useChat();

  const handleNewChat = () => {
    const newChat = createNewChat();
    navigate(`/chat/${newChat.id}`);
  };

  const features = [
    {
      icon: Sparkles,
      title: 'Smart Responses',
      description: 'Get intelligent and context-aware answers to your questions',
    },
    {
      icon: Zap,
      title: 'Fast Processing',
      description: 'Instant responses powered by advanced AI technology',
    },
    {
      icon: BookOpen,
      title: 'Knowledge Base',
      description: 'Access to comprehensive information across multiple domains',
    },
    {
      icon: TrendingUp,
      title: 'Learning Insights',
      description: 'Get personalized insights based on your interactions',
    },
  ];

  const examplePrompts = [
    'Explain quantum computing in simple terms',
    'How to build a scalable REST API',
    'Best practices for web design',
    'Machine learning fundamentals',
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex-1 overflow-y-auto pb-20 md:pb-0"
    >
      {/* Hero Section */}
      <motion.section
        className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-slate-900 dark:to-slate-800 py-12 md:py-20 px-4"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            className="text-6xl md:text-7xl mb-6"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            ✨
          </motion.div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to <span className="bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">PromptGenius</span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
            Your AI-powered assistant for any question. Ask anything and get intelligent, nuanced responses.
          </p>
          <motion.button
            onClick={handleNewChat}
            className="px-8 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold hover:from-blue-600 hover:to-cyan-600 transition text-lg"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Start Chatting Now
          </motion.button>
        </div>
      </motion.section>

      {/* Features Grid */}
      <section className="py-16 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
          Powerful Features
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="p-6 rounded-xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-blue-600 transition"
              >
                <Icon className="text-blue-500 mb-4" size={32} />
                <h3 className="font-bold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Example Prompts */}
      <section className="py-16 px-4 bg-gray-50 dark:bg-slate-900">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Example Prompts
          </h2>
          <div className="grid md:grid-cols-2 gap-4 max-w-2xl mx-auto">
            {examplePrompts.map((prompt, idx) => (
              <motion.button
                key={idx}
                initial={{ opacity: 0, x: idx % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                onClick={handleNewChat}
                className="p-4 rounded-lg bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-left hover:border-blue-300 dark:hover:border-blue-600 transition"
              >
                <p className="text-gray-700 dark:text-gray-300 font-medium">
                  {prompt}
                </p>
              </motion.button>
            ))}
          </div>
        </div>
      </section>
    </motion.div>
  );
}
