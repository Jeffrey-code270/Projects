#!/usr/bin/env python3
from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Read the React components and create a simple HTML version
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeffrey - DevOps Engineer & Full-Stack Developer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .gradient-text { background: linear-gradient(to right, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: scale(1.05); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
        .glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
    </style>
</head>
<body class="bg-gray-900 text-white">
    <!-- Navigation -->
    <header class="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex items-center justify-between">
            <div class="text-2xl font-bold gradient-text">Jeffrey</div>
            <nav class="flex items-center space-x-6 text-sm">
                <a href="#about" class="text-gray-300 hover:text-blue-400 transition-colors duration-300">About</a>
                <a href="#projects" class="text-gray-300 hover:text-blue-400 transition-colors duration-300">Projects</a>
                <a href="#contact" class="text-gray-300 hover:text-blue-400 transition-colors duration-300">Contact</a>
                <a href="#" class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-300">Resume</a>
            </nav>
        </div>
    </header>

    <main class="container mx-auto px-4 py-10">
        <!-- Hero Section -->
        <section id="about" class="py-20">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="space-y-6">
                    <div class="space-y-4">
                        <h1 class="text-5xl font-bold leading-tight">
                            Hi, I'm <span class="gradient-text">Jeffrey</span>
                        </h1>
                        <h2 class="text-2xl text-gray-300 font-light">
                            DevOps Engineer & Full-Stack Developer
                        </h2>
                    </div>
                    
                    <p class="text-lg text-gray-400 leading-relaxed">
                        Building scalable applications with modern technologies. Specialized in 
                        <span class="text-blue-400 font-medium"> CI/CD pipelines</span>, 
                        <span class="text-green-400 font-medium"> containerization</span>, and 
                        <span class="text-purple-400 font-medium"> cloud deployment</span>.
                    </p>
                    
                    <div class="flex gap-4 pt-4">
                        <a href="#projects" class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-300 glow">
                            View Projects
                        </a>
                        <a href="#contact" class="border border-gray-600 text-gray-300 px-6 py-3 rounded-lg font-medium hover:border-blue-500 hover:text-blue-400 transition-all duration-300">
                            Contact Me
                        </a>
                    </div>
                    
                    <div class="flex gap-6 pt-6">
                        <div class="text-center">
                            <div class="text-2xl font-bold text-blue-400">3+</div>
                            <div class="text-sm text-gray-500">Projects</div>
                        </div>
                        <div class="text-center">
                            <div class="text-2xl font-bold text-green-400">5+</div>
                            <div class="text-sm text-gray-500">Technologies</div>
                        </div>
                        <div class="text-center">
                            <div class="text-2xl font-bold text-purple-400">100%</div>
                            <div class="text-sm text-gray-500">Automated</div>
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-center">
                    <div class="relative">
                        <div class="w-80 h-80 bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl flex items-center justify-center shadow-2xl border border-gray-700 card-hover">
                            <div class="text-center space-y-4">
                                <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto flex items-center justify-center text-2xl font-bold">
                                    J
                                </div>
                                <div>
                                    <div class="text-xl font-semibold">Jeffrey</div>
                                    <div class="text-gray-400">DevOps Engineer</div>
                                    <div class="text-sm text-gray-500 mt-2">Python • Docker • AWS</div>
                                </div>
                            </div>
                        </div>
                        <div class="absolute -top-4 -right-4 w-8 h-8 bg-green-500 rounded-full animate-pulse"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Projects Section -->
        <section id="projects" class="py-20">
            <div class="text-center mb-12">
                <h2 class="text-4xl font-bold mb-4">
                    Featured <span class="gradient-text">Projects</span>
                </h2>
                <p class="text-gray-400 text-lg max-w-2xl mx-auto">
                    Showcasing DevOps automation, full-stack development, and modern cloud technologies
                </p>
            </div>
            
            <div class="grid md:grid-cols-2 gap-8">
                <!-- Project 1 -->
                <div class="bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 card-hover group">
                    <div class="flex items-start justify-between mb-4">
                        <h3 class="font-bold text-xl text-white group-hover:text-blue-400 transition-colors duration-300">
                            PDF Processing DevOps Pipeline
                        </h3>
                        <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    </div>
                    
                    <p class="text-gray-400 leading-relaxed mb-4">
                        Automated document processing with CI/CD, Docker containerization, and AWS deployment. Features keyword extraction, PostgreSQL storage, and real-time monitoring.
                    </p>
                    
                    <div class="flex flex-wrap gap-2 mb-4">
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">Python</span>
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">Docker</span>
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">AWS</span>
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">PostgreSQL</span>
                    </div>
                    
                    <a href="https://github.com/Jeffrey-code270/Projects/tree/main/pdf-analysis-project" target="_blank" class="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-medium transition-colors duration-300">
                        View Project →
                    </a>
                </div>

                <!-- Project 2 -->
                <div class="bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700 card-hover group">
                    <div class="flex items-start justify-between mb-4">
                        <h3 class="font-bold text-xl text-white group-hover:text-blue-400 transition-colors duration-300">
                            Portfolio Website
                        </h3>
                        <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    </div>
                    
                    <p class="text-gray-400 leading-relaxed mb-4">
                        Modern full-stack web application with React frontend and Node.js backend. Features responsive design, contact forms, and project showcase.
                    </p>
                    
                    <div class="flex flex-wrap gap-2 mb-4">
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">React</span>
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">Node.js</span>
                        <span class="px-3 py-1 bg-gray-700 text-gray-300 text-xs rounded-full border border-gray-600">Tailwind CSS</span>
                    </div>
                    
                    <a href="https://github.com/Jeffrey-code270/Projects/tree/main/portfolio-website" target="_blank" class="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 font-medium transition-colors duration-300">
                        View Project →
                    </a>
                </div>
            </div>
        </section>

        <!-- Contact Section -->
        <section id="contact" class="py-20">
            <div class="text-center mb-12">
                <h2 class="text-4xl font-bold mb-4">
                    Let's <span class="gradient-text">Connect</span>
                </h2>
                <p class="text-gray-400 text-lg">
                    Ready to discuss DevOps solutions or collaboration opportunities?
                </p>
            </div>

            <div class="grid md:grid-cols-2 gap-12 items-start max-w-4xl mx-auto">
                <!-- Contact Info -->
                <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                    <h3 class="text-xl font-semibold mb-4 text-white">Get in Touch</h3>
                    <div class="space-y-4">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center">📧</div>
                            <div>
                                <div class="text-gray-400 text-sm">Email</div>
                                <div class="text-white">jeffrin1304@gmail.com</div>
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">💼</div>
                            <div>
                                <div class="text-gray-400 text-sm">LinkedIn</div>
                                <a href="https://www.linkedin.com/in/jeffrin-jeyasingh" target="_blank" class="text-blue-400 hover:text-blue-300 transition-colors duration-300">
                                    jeffrin-jeyasingh
                                </a>
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center">🐙</div>
                            <div>
                                <div class="text-gray-400 text-sm">GitHub</div>
                                <a href="https://github.com/Jeffrey-code270" target="_blank" class="text-blue-400 hover:text-blue-300 transition-colors duration-300">
                                    Jeffrey-code270
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Contact Form -->
                <div class="bg-gray-800 p-6 rounded-xl border border-gray-700">
                    <form class="space-y-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-300 mb-2">Name</label>
                            <input type="text" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300" placeholder="Your name">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                            <input type="email" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300" placeholder="your.email@example.com">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-300 mb-2">Message</label>
                            <textarea rows="5" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors duration-300 resize-none" placeholder="Tell me about your project or opportunity..."></textarea>
                        </div>
                        
                        <button type="submit" class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-300 glow">
                            Send Message
                        </button>
                    </form>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 border-t border-gray-700 py-6">
        <div class="container mx-auto text-center text-sm text-gray-400">
            © 2024 Jeffrey • DevOps Engineer & Full-Stack Developer
        </div>
    </footer>
</body>
</html>
"""

@app.route('/')
def portfolio():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🌐 Starting portfolio website at http://localhost:3000")
    print("🎨 Dark theme portfolio with modern design!")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=3000, debug=False)