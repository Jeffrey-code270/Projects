import React, { useState } from 'react'
import axios from 'axios'

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [status, setStatus] = useState(null)

  function handleChange(e) {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus('sending')
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '/api'
      const res = await axios.post(`${apiUrl}/contact`, form)
      if (res.status === 200) {
        setStatus('sent')
        setForm({ name: '', email: '', message: '' })
      } else {
        setStatus('error')
      }
    } catch (err) {
      console.error(err)
      setStatus('error')
    }
  }

  return (
    <section id="contact" className="py-20">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">
          Let's <span className="gradient-text">Connect</span>
        </h2>
        <p className="text-gray-400 text-lg">
          Ready to discuss DevOps solutions or collaboration opportunities?
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-12 items-start">
        {/* Contact Info */}
        <div className="space-y-8">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h3 className="text-xl font-semibold mb-4 text-white">Get in Touch</h3>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">
                  📧
                </div>
                <div>
                  <div className="text-gray-400 text-sm">Email</div>
                  <div className="text-white">jeffrin1304@gmail.com</div>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                  💼
                </div>
                <div>
                  <div className="text-gray-400 text-sm">LinkedIn</div>
                  <a href="https://www.linkedin.com/in/jeffrin-jeyasingh" target="_blank" rel="noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors duration-300">
                    jeffrin-jeyasingh
                  </a>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center">
                  🐙
                </div>
                <div>
                  <div className="text-gray-400 text-sm">GitHub</div>
                  <a href="https://github.com/Jeffrey-code270" target="_blank" rel="noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors duration-300">
                    Jeffrey-code270
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Contact Form */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Name</label>
              <input 
                name="name" 
                value={form.name} 
                onChange={handleChange} 
                required 
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300" 
                placeholder="Your name"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input 
                name="email" 
                type="email" 
                value={form.email} 
                onChange={handleChange} 
                required 
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300" 
                placeholder="your.email@example.com"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Message</label>
              <textarea 
                name="message" 
                value={form.message} 
                onChange={handleChange} 
                required 
                rows="5"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300 resize-none" 
                placeholder="Tell me about your project or opportunity..."
              />
            </div>
            
            <div className="flex items-center gap-4">
              <button 
                type="submit" 
                disabled={status === 'sending'}
                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed glow"
              >
                {status === 'sending' ? 'Sending...' : 'Send Message'}
              </button>
              
              {status === 'sent' && (
                <span className="text-green-400 font-medium">✅ Message sent successfully!</span>
              )}
              {status === 'error' && (
                <span className="text-red-400 font-medium">❌ Something went wrong. Try again.</span>
              )}
            </div>
          </form>
        </div>
      </div>
    </section>
  )
}