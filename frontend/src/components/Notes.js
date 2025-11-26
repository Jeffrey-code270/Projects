import React, { useState, useEffect } from 'react';
import { notes, user as userAPI } from '../services/api';

const Notes = ({ user, onLogout, onUserUpdate, theme, onThemeChange }) => {
  const [notesList, setNotesList] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [search, setSearch] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [newUsername, setNewUsername] = useState(user.username);
  const [tags, setTags] = useState('');
  const [color, setColor] = useState('#ffffff');
  const [filter, setFilter] = useState('all');
  const [stats, setStats] = useState({});
  const [analytics, setAnalytics] = useState({});
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [autoSave, setAutoSave] = useState(null);

  useEffect(() => {
    fetchNotes();
    fetchStats();
  }, [search, filter]);

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        setTitle('');
        setContent('');
        setTags('');
        setColor('#ffffff');
        setEditingId(null);
      }
      if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        if (title && content) {
          handleSubmit(e);
        }
      }
      if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="text"]');
        if (searchInput) searchInput.focus();
      }
    };
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [title, content]);

  const fetchNotes = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (filter === 'favorites') params.favorite = 'true';
      
      const response = await notes.getAll(params);
      setNotesList(response.data);
    } catch (error) {
      console.error('Error fetching notes:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await notes.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await notes.getAnalytics();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const handleShare = async (id, isPublic) => {
    try {
      const response = await notes.share(id, !isPublic);
      if (response.data.shareId) {
        const shareUrl = window.location.origin + '/shared/' + response.data.shareId;
        navigator.clipboard.writeText(shareUrl);
        alert('Share link copied to clipboard!');
      }
      fetchNotes();
    } catch (error) {
      alert('Error sharing note');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const noteData = {
        title,
        content,
        tags: tags.split(',').map(tag => tag.trim()).filter(tag => tag),
        color
      };
      
      if (editingId) {
        await notes.update(editingId, noteData);
        setEditingId(null);
      } else {
        await notes.create(noteData);
      }
      
      setTitle('');
      setContent('');
      setTags('');
      setColor('#ffffff');
      fetchNotes();
      fetchStats();
    } catch (error) {
      alert('Error saving note');
    }
  };

  const handleEdit = (note) => {
    setTitle(note.title);
    setContent(note.content);
    setTags(note.tags ? note.tags.join(', ') : '');
    setColor(note.color || '#ffffff');
    setEditingId(note._id);
  };

  const handlePin = async (id, isPinned) => {
    try {
      await notes.pin(id, !isPinned);
      fetchNotes();
      fetchStats();
    } catch (error) {
      alert('Error updating pin status');
    }
  };

  const handleFavorite = async (id, isFavorite) => {
    try {
      await notes.favorite(id, !isFavorite);
      fetchNotes();
      fetchStats();
    } catch (error) {
      alert('Error updating favorite status');
    }
  };

  const exportNotes = () => {
    const dataStr = JSON.stringify(notesList, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'smartnotes-export.json';
    link.click();
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        await notes.delete(id);
        fetchNotes();
        fetchStats();
      } catch (error) {
        alert('Error deleting note');
      }
    }
  };

  const handleUsernameUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await userAPI.updateUsername(newUsername);
      onUserUpdate(response.data.user);
      setShowSettings(false);
      alert('Username updated successfully!');
    } catch (error) {
      alert('Error: ' + (error.response?.data?.message || error.message));
    }
  };

  const containerStyle = {
    minHeight: '100vh',
    background: 'var(--bg-secondary)',
    padding: '20px'
  };

  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: 'var(--bg-card)',
    padding: '20px',
    borderRadius: '15px',
    boxShadow: '0 5px 15px var(--shadow)',
    marginBottom: '20px'
  };

  const inputStyle = {
    width: '100%',
    padding: '15px',
    margin: '10px 0',
    border: '2px solid var(--border)',
    borderRadius: '10px',
    fontSize: '16px',
    background: 'var(--bg-card)',
    color: 'var(--text-primary)',
    transition: 'all 0.3s ease'
  };

  const buttonStyle = {
    padding: '12px 24px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: 'bold',
    cursor: 'pointer',
    margin: '5px',
    transition: 'all 0.3s ease'
  };

  const noteCardStyle = {
    background: 'var(--bg-card)',
    padding: '20px',
    margin: '15px 0',
    borderRadius: '12px',
    boxShadow: '0 3px 10px var(--shadow)',
    transition: 'all 0.3s ease'
  };

  return (
    <div style={containerStyle} className="fade-in">
      <div style={headerStyle}>
        <h1 style={{ color: 'var(--text-primary)', margin: 0 }}>📝 {user.username}'s Notes</h1>
        <div className="dropdown">
          <div 
            onClick={() => setShowDropdown(!showDropdown)}
            style={{
              display: 'flex',
              alignItems: 'center',
              cursor: 'pointer',
              padding: '10px 15px',
              background: 'var(--border)',
              borderRadius: '25px',
              transition: 'all 0.3s ease'
            }}
          >
            <span style={{ marginRight: '8px' }}>👤</span>
            <span style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>{user.username}</span>
            <span style={{ marginLeft: '8px', fontSize: '12px' }}>▼</span>
          </div>
          {showDropdown && (
            <div className="dropdown-content" style={{ background: 'var(--bg-card)' }}>
              <button 
                onClick={() => { setShowSettings(true); setShowDropdown(false); }}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: 'none',
                  border: 'none',
                  textAlign: 'left',
                  cursor: 'pointer',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  transition: 'background 0.2s ease'
                }}
              >
                ⚙️ Settings
              </button>
              <button 
                onClick={() => onThemeChange(theme === 'light' ? 'dark' : 'light')}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: 'none',
                  border: 'none',
                  textAlign: 'left',
                  cursor: 'pointer',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  transition: 'background 0.2s ease'
                }}
              >
                {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
              </button>
              <button 
                onClick={onLogout}
                style={{
                  width: '100%',
                  padding: '12px',
                  background: 'none',
                  border: 'none',
                  textAlign: 'left',
                  cursor: 'pointer',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  transition: 'background 0.2s ease'
                }}
              >
                🚪 Logout
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div style={{ background: 'var(--bg-card)', padding: '20px', borderRadius: '15px', boxShadow: '0 5px 15px var(--shadow)', marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
          <div style={{ background: 'var(--border)', padding: '10px', borderRadius: '8px', fontSize: '14px' }}>
            📊 Total: {stats.totalNotes || 0}
          </div>
          <div style={{ background: 'var(--border)', padding: '10px', borderRadius: '8px', fontSize: '14px' }}>
            📌 Pinned: {stats.pinnedNotes || 0}
          </div>
          <div style={{ background: 'var(--border)', padding: '10px', borderRadius: '8px', fontSize: '14px' }}>
            ⭐ Favorites: {stats.favoriteNotes || 0}
          </div>
          <div style={{ background: 'var(--border)', padding: '10px', borderRadius: '8px', fontSize: '14px' }}>
            🏷️ Tags: {stats.totalTags || 0}
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
          <select value={filter} onChange={(e) => setFilter(e.target.value)} style={{ ...inputStyle, width: 'auto', margin: 0 }}>
            <option value="all">📄 All Notes</option>
            <option value="favorites">⭐ Favorites</option>
          </select>
          <button onClick={exportNotes} style={{ ...buttonStyle, background: '#17a2b8' }}>
            📥 Export
          </button>
          <button onClick={() => { setShowAnalytics(true); fetchAnalytics(); }} style={{ ...buttonStyle, background: '#6f42c1' }}>
            📈 Analytics
          </button>
        </div>
        
        <input
          type="text"
          placeholder="🔍 Search notes... (Ctrl+N: New, Ctrl+S: Save, Ctrl+F: Focus)"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={inputStyle}
        />
        
        <div style={{ display: 'flex', gap: '10px', marginTop: '15px', flexWrap: 'wrap' }}>
          {['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff'].map(colorOption => (
            <button
              key={colorOption}
              onClick={() => setColor(colorOption)}
              style={{
                width: '30px',
                height: '30px',
                backgroundColor: colorOption,
                border: color === colorOption ? '3px solid #333' : '2px solid #ddd',
                borderRadius: '50%',
                cursor: 'pointer',
                transition: 'transform 0.2s ease'
              }}
              title={'Set note color to ' + colorOption}
            />
          ))}
          <button
            onClick={() => setColor('#ffffff')}
            style={{
              width: '30px',
              height: '30px',
              backgroundColor: '#ffffff',
              border: '2px solid #333',
              borderRadius: '50%',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '12px'
            }}
            title="Reset to white"
          >
            ✖️
          </button>
        </div>

        <form onSubmit={handleSubmit} className="bounce">
          <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <input
              type="text"
              placeholder="📝 Note title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              style={{ ...inputStyle, flex: 1, margin: 0 }}
            />
            <input
              type="color"
              value={color}
              onChange={(e) => setColor(e.target.value)}
              style={{ width: '50px', height: '50px', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
              title="Note color"
            />
          </div>
          <input
            type="text"
            placeholder="🏷️ Tags (comma separated)"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            style={inputStyle}
          />
          <textarea
            placeholder="✍️ Write your note here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            rows="4"
            style={{ ...inputStyle, resize: 'vertical' }}
          />
          <button 
            type="submit" 
            style={buttonStyle}
          >
            {editingId ? '✅ Update Note' : '➕ Add Note'}
          </button>
          {editingId && (
            <button 
              type="button" 
              onClick={() => { setEditingId(null); setTitle(''); setContent(''); setTags(''); setColor('#ffffff'); }}
              style={{ ...buttonStyle, background: '#6c757d' }}
            >
              ❌ Cancel
            </button>
          )}
        </form>
      </div>

      <div>
        {notesList.map((note, index) => (
          <div 
            key={note._id} 
            className="note-card slide-in" 
            style={{ 
              ...noteCardStyle, 
              animationDelay: (index * 0.1) + 's',
              background: note.color || 'var(--bg-card)',
              border: note.isPinned ? '3px solid #ffc107' : 'none'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
              <h3 style={{ color: 'var(--text-primary)', margin: 0, flex: 1 }}>
                {note.isPinned && '📌 '}{note.title}
              </h3>
              <div style={{ display: 'flex', gap: '5px' }}>
                <button 
                  onClick={() => handlePin(note._id, note.isPinned)}
                  style={{ 
                    background: 'none', 
                    border: 'none', 
                    fontSize: '16px', 
                    cursor: 'pointer',
                    opacity: note.isPinned ? 1 : 0.5
                  }}
                  title={note.isPinned ? 'Unpin' : 'Pin'}
                >
                  📌
                </button>
                <button 
                  onClick={() => handleFavorite(note._id, note.isFavorite)}
                  style={{ 
                    background: 'none', 
                    border: 'none', 
                    fontSize: '16px', 
                    cursor: 'pointer',
                    opacity: note.isFavorite ? 1 : 0.5
                  }}
                  title={note.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                >
                  ⭐
                </button>
                <button 
                  onClick={() => handleShare(note._id, note.isPublic)}
                  style={{ 
                    background: 'none', 
                    border: 'none', 
                    fontSize: '16px', 
                    cursor: 'pointer',
                    opacity: note.isPublic ? 1 : 0.5
                  }}
                  title={note.isPublic ? 'Make private' : 'Share note'}
                >
                  🔗
                </button>
              </div>
            </div>
            
            {note.tags && note.tags.length > 0 && (
              <div style={{ marginBottom: '10px' }}>
                {note.tags.map((tag, i) => (
                  <span 
                    key={i} 
                    style={{ 
                      background: 'var(--border)', 
                      padding: '2px 8px', 
                      borderRadius: '12px', 
                      fontSize: '12px', 
                      marginRight: '5px',
                      color: 'var(--text-secondary)'
                    }}
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}
            
            <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '15px' }}>
              {note.content.length > 150 ? note.content.substring(0, 150) + '...' : note.content}
            </p>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <small style={{ color: 'var(--text-muted)' }}>
                  📅 {new Date(note.updatedAt).toLocaleDateString()}
                </small>
                <small style={{ color: 'var(--text-muted)', marginLeft: '10px' }}>
                  📝 {note.content.split(' ').length} words
                </small>
              </div>
              <div>
                <button 
                  onClick={() => handleEdit(note)}
                  style={{ ...buttonStyle, background: '#28a745', padding: '6px 12px', fontSize: '12px' }}
                >
                  ✏️ Edit
                </button>
                <button 
                  onClick={() => handleDelete(note._id)}
                  style={{ ...buttonStyle, background: '#dc3545', padding: '6px 12px', fontSize: '12px' }}
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {showSettings && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'var(--bg-card)',
            padding: '30px',
            borderRadius: '15px',
            boxShadow: '0 15px 35px var(--shadow)',
            maxWidth: '400px',
            width: '90%'
          }} className="bounce">
            <h3 style={{ marginBottom: '20px', color: 'var(--text-primary)' }}>⚙️ Settings</h3>
            <form onSubmit={handleUsernameUpdate}>
              <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>Username:</label>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                required
                style={inputStyle}
              />
              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                <button type="submit" style={buttonStyle}>
                  ✅ Update
                </button>
                <button 
                  type="button" 
                  onClick={() => { setShowSettings(false); setNewUsername(user.username); }}
                  style={{ ...buttonStyle, background: '#6c757d' }}
                >
                  ❌ Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showAnalytics && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'var(--bg-card)',
            padding: '30px',
            borderRadius: '15px',
            boxShadow: '0 15px 35px var(--shadow)',
            maxWidth: '500px',
            width: '90%',
            maxHeight: '80vh',
            overflow: 'auto'
          }} className="bounce">
            <h3 style={{ marginBottom: '20px', color: 'var(--text-primary)' }}>📈 Analytics Dashboard</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '15px', marginBottom: '20px' }}>
              <div style={{ background: 'var(--border)', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{analytics.totalWords || 0}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Total Words</div>
              </div>
              <div style={{ background: 'var(--border)', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{analytics.avgWordsPerNote || 0}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Avg Words per Note</div>
              </div>
              <div style={{ background: 'var(--border)', padding: '15px', borderRadius: '8px', textAlign: 'center' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{analytics.notesThisWeek || 0}</div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>This Week</div>
              </div>
            </div>
            
            {analytics.topTags && analytics.topTags.length > 0 && (
              <div style={{ marginBottom: '20px' }}>
                <h4 style={{ color: 'var(--text-primary)', marginBottom: '10px' }}>Top Tags</h4>
                {analytics.topTags.map((tag, i) => (
                  <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0' }}>
                    <span style={{ color: 'var(--text-secondary)' }}>#{tag.tag}</span>
                    <span style={{ color: 'var(--text-primary)', fontWeight: 'bold' }}>{tag.count}</span>
                  </div>
                ))}
              </div>
            )}
            
            <button 
              onClick={() => setShowAnalytics(false)}
              style={{ ...buttonStyle, width: '100%' }}
            >
              ❌ Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notes;