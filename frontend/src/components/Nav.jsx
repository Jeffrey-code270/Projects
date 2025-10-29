import React from 'react'

export default function Nav() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="text-2xl font-semibold">Jeffrin</div>
        <nav className="space-x-4 text-sm text-gray-700">
          <a href="#about" className="hover:underline">About</a>
          <a href="#projects" className="hover:underline">Projects</a>
          <a href="#contact" className="hover:underline">Contact</a>
          <a href="/resume.pdf" target="_blank" rel="noreferrer" className="ml-4 inline-block bg-blue-600 text-white px-3 py-1 rounded">Resume</a>
        </nav>
      </div>
    </header>
  )
}
