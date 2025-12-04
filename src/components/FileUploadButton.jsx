import React, { useRef } from 'react';
import { motion } from 'framer-motion';
import { Paperclip } from 'lucide-react';

export default function FileUploadButton({ onFileSelect }) {
  const inputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        onFileSelect({
          file,
          name: file.name,
          size: file.size,
          type: file.type,
          preview: event.target.result.substring(0, 100),
        });
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        onChange={handleFileChange}
        className="hidden"
      />
      <motion.button
        onClick={() => inputRef.current?.click()}
        className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-800 text-gray-600 dark:text-gray-400 transition"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Paperclip size={20} />
      </motion.button>
    </>
  );
}
