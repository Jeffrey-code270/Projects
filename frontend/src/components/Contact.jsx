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
    <section id="contact" className="py-10">
      <h2 className="text-2xl font-bold mb-4">Contact Me</h2>
      <div className="mb-4">
        <a href="https://www.linkedin.com/in/jeffrin-jeyasingh" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">LinkedIn: www.linkedin.com/in/jeffrin-jeyasingh</a>
      </div>
      <div className="max-w-xl">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm">Name</label>
            <input name="name" value={form.name} onChange={handleChange} required className="w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label className="block text-sm">Email</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} required className="w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label className="block text-sm">Message</label>
            <textarea name="message" value={form.message} onChange={handleChange} required className="w-full border rounded px-3 py-2 h-28" />
          </div>
          <div>
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Send Message</button>
            {status === 'sending' && <span className="ml-3 text-sm text-gray-500">Sending...</span>}
            {status === 'sent' && <span className="ml-3 text-sm text-green-600">Message sent — thanks!</span>}
            {status === 'error' && <span className="ml-3 text-sm text-red-600">Something went wrong.</span>}
          </div>
        </form>
      </div>
    </section>
  )
}
