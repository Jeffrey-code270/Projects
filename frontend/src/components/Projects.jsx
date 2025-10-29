import React, { useEffect, useState } from 'react'
import axios from 'axios'

function Card({ project }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h3 className="font-semibold text-lg">{project.title}</h3>
      <p className="text-sm text-gray-600 mt-2">{project.description}</p>
      <div className="mt-3 text-xs text-gray-500">Tech: {project.tech.join(', ')}</div>
      {project.link && (
        <a href={project.link} target="_blank" rel="noreferrer" className="inline-block mt-3 text-blue-600 text-sm">Live / Repo</a>
      )}
    </div>
  )
}

export default function Projects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    axios.get(`${apiUrl}/projects`)
      .then(res => {
        if (!mounted) return
        setProjects(res.data)
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false))
    return () => { mounted = false }
  }, [])

  return (
    <section id="projects" className="py-10">
      <h2 className="text-2xl font-bold mb-6">Projects</h2>
      {loading ? (
        <div>Loading projects...</div>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {projects.map(p => (
            <Card key={p.id} project={p} />
          ))}
        </div>
      )}
    </section>
  )
}
