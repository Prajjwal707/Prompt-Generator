import React from 'react';
import { motion } from 'framer-motion';
import { Code, Presentation, Image } from 'lucide-react';

const TASK_TYPES = [
  {
    id: 'website',
    label: 'Create Website Prompt',
    icon: Code,
    description: 'Generate prompts for website creation',
  },
  {
    id: 'ppt',
    label: 'Design PPT Prompt',
    icon: Presentation,
    description: 'Generate prompts for PowerPoint design',
  },
  {
    id: 'image',
    label: 'Edit Image Prompt',
    icon: Image,
    description: 'Generate prompts for image editing',
  },
];

export default function TaskTypeSelector({ selected, onSelect }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="mb-4 px-4 md:px-0"
    >
      <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-3 text-center">
        Choose a task type to get started:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {TASK_TYPES.map((task) => {
          const Icon = task.icon;
          const isSelected = selected === task.id;

          return (
            <motion.button
              key={task.id}
              onClick={() => onSelect(task.id)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`flex items-center gap-3 p-3 rounded-lg border-2 transition ${
                isSelected
                  ? 'border-blue-500 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/30 dark:to-cyan-900/30'
                  : 'border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-800 hover:border-blue-400 dark:hover:border-blue-500'
              }`}
            >
              <Icon
                size={20}
                className={isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'}
              />
              <div className="flex-1 text-left">
                <p className={`text-sm font-semibold ${isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'}`}>
                  {task.label}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  {task.description}
                </p>
              </div>
              {isSelected && (
                <motion.div
                  layoutId="taskSelector"
                  className="w-5 h-5 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center"
                >
                  <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </motion.div>
              )}
            </motion.button>
          );
        })}
      </div>
    </motion.div>
  );
}
