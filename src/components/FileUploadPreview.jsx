import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { X, Download } from 'lucide-react';

export default function FileUploadPreview({ uploads, onRemove }) {
  const processedUploads = useMemo(() => {
    return uploads.map(upload => ({
      ...upload,
      id: `${upload.file?.name || 'file'}-${Math.random()}`,
    }));
  }, [uploads]);

  if (processedUploads.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex gap-2 mb-4 flex-wrap px-4"
    >
      {processedUploads.map((upload, idx) => (
        <motion.div
          key={upload.id}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          className="relative group"
        >
          {upload.type === 'image' ? (
            <div className="relative">
              <img
                src={upload.preview}
                alt="Preview"
                className="max-h-32 rounded-lg border border-gray-200 dark:border-slate-600"
              />
              <motion.button
                onClick={() => onRemove(idx)}
                className="absolute -top-2 -right-2 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition"
                whileHover={{ scale: 1.1 }}
              >
                <X size={14} />
              </motion.button>
            </div>
          ) : (
            <div className="bg-blue-100 dark:bg-blue-900/30 p-3 rounded-lg border border-blue-200 dark:border-blue-700 flex items-center gap-2 relative">
              <Download size={16} className="text-blue-600 dark:text-blue-400" />
              <span className="text-sm text-blue-700 dark:text-blue-300 max-w-xs truncate">
                {upload.name}
              </span>
              <motion.button
                onClick={() => onRemove(idx)}
                className="absolute -top-2 -right-2 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition"
                whileHover={{ scale: 1.1 }}
              >
                <X size={14} />
              </motion.button>
            </div>
          )}
        </motion.div>
      ))}
    </motion.div>
  );
}
