import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import TopSearch from './components/TopSearch';
import ChatWindow from './components/ChatWindow';
import Home from './pages/Home';
import Discover from './pages/Discover';
import Search from './pages/Search';

export default function AppRouter() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-white dark:bg-slate-950">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <main className="flex-1 flex flex-col overflow-hidden md:mb-0 mb-16">
          <TopSearch />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/discover" element={<Discover />} />
            <Route path="/search" element={<Search />} />
            <Route path="/chat/:chatId" element={<ChatWindow />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
