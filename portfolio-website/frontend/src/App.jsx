import React from 'react'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Projects from './components/Projects'
import Contact from './components/Contact'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white">
      <Nav />
      <main className="flex-1 container mx-auto px-4 py-10">
        <Hero />
        <Projects />
        <Contact />
      </main>
      <footer className="bg-gray-800 border-t border-gray-700 py-6">
        <div className="container mx-auto text-center text-sm text-gray-400">
          © {new Date().getFullYear()} Jeffrey • DevOps Engineer & Full-Stack Developer
        </div>
      </footer>
    </div>
  )
}