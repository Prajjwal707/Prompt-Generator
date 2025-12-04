import React, { createContext, useContext, useState, useCallback } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [chats, setChats] = useState(() => {
    const saved = localStorage.getItem('chats');
    return saved ? JSON.parse(saved) : [];
  });

  const [currentChatId, setCurrentChatId] = useState(() => {
    const saved = localStorage.getItem('currentChatId');
    return saved || null;
  });

  const [activeTaskType, setActiveTaskType] = useState(null);

  const getCurrentChat = () => chats.find(chat => chat.id === currentChatId) || null;

  const createNewChat = useCallback(() => {
    const newChat = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      taskType: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
    setActiveTaskType(null);
    localStorage.setItem('currentChatId', newChat.id);
    return newChat;
  }, []);

  const addMessage = useCallback((message) => {
    setChats(prev => {
      const updated = prev.map(chat => 
        chat.id === currentChatId
          ? {
              ...chat,
              messages: [...chat.messages, { ...message, id: Date.now().toString() }],
              updatedAt: new Date().toISOString(),
              title: chat.messages.length === 0 ? message.content.substring(0, 50) : chat.title,
              taskType: activeTaskType || chat.taskType,
            }
          : chat
      );
      localStorage.setItem('chats', JSON.stringify(updated));
      return updated;
    });
  }, [currentChatId, activeTaskType]);

  const deleteChat = useCallback((chatId) => {
    setChats(prev => {
      const updated = prev.filter(chat => chat.id !== chatId);
      localStorage.setItem('chats', JSON.stringify(updated));
      if (currentChatId === chatId) {
        const nextChat = updated[0];
        setCurrentChatId(nextChat?.id || null);
        localStorage.setItem('currentChatId', nextChat?.id || '');
      }
      return updated;
    });
  }, [currentChatId]);

  const updateChatTitle = useCallback((chatId, title) => {
    setChats(prev => {
      const updated = prev.map(chat =>
        chat.id === chatId ? { ...chat, title } : chat
      );
      localStorage.setItem('chats', JSON.stringify(updated));
      return updated;
    });
  }, []);

  const loadChat = useCallback((chatId) => {
    setCurrentChatId(chatId);
    localStorage.setItem('currentChatId', chatId);
  }, []);

  return (
    <ChatContext.Provider value={{
      chats,
      currentChatId,
      activeTaskType,
      getCurrentChat,
      createNewChat,
      addMessage,
      deleteChat,
      updateChatTitle,
      loadChat,
      setActiveTaskType,
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);
