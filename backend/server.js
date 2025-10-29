
const express = require('express')
const cors = require('cors')
const path = require('path')
const nodemailer = require('nodemailer')
const mongoose = require('mongoose')
const Contact = require('./models/Contact')
require('dotenv').config()

const app = express()
const PORT = process.env.PORT || 3001

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/portfolio')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err))

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
}))
app.use(express.json())

// simple in-memory projects list - replace with DB later
const projects = [
  {
    id: 1,
    title: 'Automated Document Processing Pipeline',
    description: 'Extracts text from PDFs, analyzes keywords and stores results in PostgreSQL. Deployed on AWS with CI/CD.',
    tech: ['Python', 'Docker', 'AWS', 'PostgreSQL'],
    link: ''
  },
  {
    id: 2,
    title: 'VibraSpeak',
    description: 'Android app for visually impaired users; shape detection with TTS & vibration feedback.',
    tech: ['Java', 'Android', 'Computer Vision'],
    link: ''
  },
  {
    id: 3,
    title: 'Portfolio Website',
    description: 'Full-stack portfolio website with contact form and MongoDB integration. Built with React, Node.js, and Tailwind CSS.',
    tech: ['React', 'Node.js', 'MongoDB', 'Tailwind CSS'],
    link: 'https://github.com/Jeffrey-code270/Projects'
  }
]

app.get('/api/projects', (req, res) => {
  res.json(projects)
})

app.post('/api/contact', async (req, res) => {
  const { name, email, message } = req.body
  if (!name || !email || !message) return res.status(400).json({ error: 'Missing fields' })

  try {
    const contact = new Contact({ name, email, message })
    await contact.save()
    return res.json({ status: 'ok' })
  } catch (err) {
    console.error('Database error', err)
    return res.status(500).json({ error: 'Failed to save contact' })
  }
})

// Serve static frontend build in production (optional)
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '..', 'frontend', 'dist')))
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'frontend', 'dist', 'index.html'))
  })
}

app.listen(PORT, () => console.log(`Server running on port ${PORT}`))