import React from 'react'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Projects from './components/Projects'
import Contact from './components/Contact'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 container mx-auto px-4 py-10">
        <Hero />
        <Projects />
        <Contact />
      </main>
      <footer className="bg-white border-t py-4">
        <div className="container mx-auto text-center text-sm text-gray-600">
          © {new Date().getFullYear()} Jeffrin Jeyasingh • Built with React & Tailwind
        </div>
      </footer>
    </div>
  )
}