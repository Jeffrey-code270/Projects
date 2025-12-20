import React from 'react'

export default function Hero() {
  return (
    <section id="about" className="py-20">
      <div className="grid md:grid-cols-2 gap-12 items-center">
        <div className="space-y-6">
          <div className="space-y-4">
            <h1 className="text-5xl font-bold leading-tight">
              Hi, I'm <span className="gradient-text">Jeffrey</span>
            </h1>
            <h2 className="text-2xl text-gray-300 font-light">
              DevOps Engineer & Full-Stack Developer
            </h2>
          </div>
          
          <p className="text-lg text-gray-400 leading-relaxed">
            Building scalable applications with modern technologies. Specialized in 
            <span className="text-blue-400 font-medium"> CI/CD pipelines</span>, 
            <span className="text-green-400 font-medium"> containerization</span>, and 
            <span className="text-purple-400 font-medium"> cloud deployment</span>.
          </p>
          
          <div className="flex gap-4 pt-4">
            <a href="#projects" className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-300 glow">
              View Projects
            </a>
            <a href="#contact" className="border border-gray-600 text-gray-300 px-6 py-3 rounded-lg font-medium hover:border-blue-500 hover:text-blue-400 transition-all duration-300">
              Contact Me
            </a>
          </div>
          
          <div className="flex gap-6 pt-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">3+</div>
              <div className="text-sm text-gray-500">Projects</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">5+</div>
              <div className="text-sm text-gray-500">Technologies</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-400">100%</div>
              <div className="text-sm text-gray-500">Automated</div>
            </div>
          </div>
        </div>
        
        <div className="flex justify-center">
          <div className="relative">
            <div className="w-80 h-80 bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl flex items-center justify-center shadow-2xl border border-gray-700 card-hover">
              <div className="text-center space-y-4">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto flex items-center justify-center text-2xl font-bold">
                  J
                </div>
                <div>
                  <div className="text-xl font-semibold">Jeffrey</div>
                  <div className="text-gray-400">DevOps Engineer</div>
                  <div className="text-sm text-gray-500 mt-2">Python • Docker • AWS</div>
                </div>
              </div>
            </div>
            <div className="absolute -top-4 -right-4 w-8 h-8 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    </section>
  )
}