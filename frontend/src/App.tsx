// New App with routing
import React from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import MapPage from './pages/MapPage';
import DonationsPage from './pages/DonationsPage';
import PostDonationPage from './pages/PostDonationPage';
import StatsPage from './pages/StatsPage';

function BottomNav() {
  const navItems = [
    { to: '/map', label: 'Map' },
    { to: '/donations', label: 'Donations' },
    { to: '/post', label: 'Post' },
    { to: '/stats', label: 'Stats' },
  ];
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around p-2">
      {navItems.map((item) => (
        <Link key={item.to} to={item.to} className="text-sm text-gray-700">
          {item.label}
        </Link>
      ))}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen pb-12">
        <Routes>
          <Route path="/" element={<Navigate replace to="/map" />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/donations" element={<DonationsPage />} />
          <Route path="/post" element={<PostDonationPage />} />
          <Route path="/stats" element={<StatsPage />} />
        </Routes>
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;
