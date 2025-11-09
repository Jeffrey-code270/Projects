import React from 'react'

export default function Hero() {
  return (
    <section id="about" className="py-12">
      <div className="grid md:grid-cols-2 gap-8 items-center">
        <div>
          <h1 className="text-4xl font-extrabold mb-4">Hi, I’m <span className="text-blue-600">Jeffrin</span></h1>
          <p className="text-lg text-gray-700 mb-6">MCA student and aspiring Full-Stack Developer. I build scalable web applications using React, Node.js and Python. Experienced with Docker, AWS and CI/CD.</p>
          <div className="flex gap-3">
            <a href="#projects" className="inline-block bg-blue-600 text-white px-4 py-2 rounded">View Projects</a>
            <a href="mailto:jeffrin1304@gmail.com" className="inline-block border border-blue-600 px-4 py-2 rounded">Contact Me</a>
          </div>
        </div>
        <div className="flex justify-center">
          <div className="w-64 h-64 bg-gradient-to-br from-blue-100 to-white rounded-lg flex items-center justify-center shadow-md">
            <div className="text-center">
              <div className="text-sm text-gray-500">Profile</div>
              <div className="mt-2 font-semibold">Jeffrin Jeyasingh</div>
              <div className="text-xs text-gray-500">Full Stack Developer</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}