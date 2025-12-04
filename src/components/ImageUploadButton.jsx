import React, { useRef } from 'react';
import { motion } from 'framer-motion';
import { Image, X } from 'lucide-react';

export default function ImageUploadButton({ onImageSelect }) {
  const inputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        onImageSelect({
          file,
          preview: event.target.result,
          type: 'image',
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
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
      <motion.button
        onClick={() => inputRef.current?.click()}
        className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-800 text-gray-600 dark:text-gray-400 transition"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Image size={20} />
      </motion.button>
    </>
  );
}
