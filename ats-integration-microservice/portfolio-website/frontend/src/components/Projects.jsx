import React, { useEffect, useState } from 'react'
import axios from 'axios'

function Card({ project }) {
  return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 card-hover group">
      <div className="flex items-start justify-between mb-4">
        <h3 className="font-bold text-xl text-white group-hover:text-blue-400 transition-colors duration-300">
          {project.title}
        </h3>
        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
      </div>
      
      <p className="text-gray-400 leading-relaxed mb-4">{project.description}</p>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {project.tech.map((tech, index) => (
          <span key={index} className="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">
            {tech}
          </span>
        ))}
      </div>
      
      {project.link && (
        <a 
          href={project.link} 
          target="_blank" 
          rel="noreferrer" 
          className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-medium transition-colors duration-300"
        >
          View Project →
        </a>
      )}
    </div>
  )
}

export default function Projects() {
  const [projects, setProjects] = useState([
    {
      id: 1,
      title: "PDF Processing DevOps Pipeline",
      description: "Automated document processing with CI/CD, Docker containerization, and AWS deployment. Features keyword extraction, PostgreSQL storage, and real-time monitoring.",
      tech: ["Python", "Docker", "AWS", "PostgreSQL", "GitHub Actions", "NLTK"],
      link: "https://github.com/Jeffrey-code270/Projects/tree/main/pdf-analysis-project"
    },
    {
      id: 2,
      title: "Portfolio Website",
      description: "Modern full-stack web application with React frontend and Node.js backend. Features responsive design, contact forms, and project showcase.",
      tech: ["React", "Node.js", "Express", "MongoDB", "Tailwind CSS"],
      link: "https://github.com/Jeffrey-code270/Projects/tree/main/portfolio-website"
    }
  ])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Try to fetch from API, fallback to static data
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    axios.get(`${apiUrl}/projects`)
      .then(res => {
        if (res.data && res.data.length > 0) {
          setProjects(res.data)
        }
      })
      .catch(() => {
        // Use static data if API fails
        console.log('Using static project data')
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <section id="projects" className="py-20">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">
          Featured <span className="gradient-text">Projects</span>
        </h2>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          Showcasing DevOps automation, full-stack development, and modern cloud technologies
        </p>
      </div>
      
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading projects...</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-8">
          {projects.map(p => (
            <Card key={p.id} project={p} />
          ))}
        </div>
      )}
    </section>
  )
}