import React from 'react'

export default function Nav() {
  return (
    <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="text-2xl font-bold gradient-text">Jeffrey</div>
        <nav className="flex items-center space-x-6 text-sm">
          <a href="#about" className="text-gray-300 hover:text-blue-400 transition-colors duration-300">About</a>
          <a href="#projects" className="text-gray-300 hover:text-blue-400 transition-colors duration-300">Projects</a>
          <a href="#contact" className="text-gray-300 hover:text-blue-400 transition-colors duration-300">Contact</a>
          <a href="/resume.pdf" target="_blank" rel="noreferrer" className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300">
            Resume
          </a>
        </nav>
      </div>
    </header>
  )
}