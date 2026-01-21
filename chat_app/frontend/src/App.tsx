import React, { useState, useEffect, useRef } from 'react';
import { Send, FileText, Download, MessageSquare, Terminal, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) { }
    }
    return ''; // use external default escaping
  }
});

interface FileInfo {
  name: string;
  path: string;
  size: number;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  reasoning?: string;
  status?: string;
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get('/api/files');
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    const assistantMsg: ChatMessage = { role: 'assistant', content: '', reasoning: '', status: 'starting' };
    setMessages(prev => [...prev, assistantMsg]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) return;

      let currentReasoning = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'reasoning') {
                currentReasoning += data.content;
                setMessages(prev => {
                  const last = [...prev];
                  last[last.length - 1] = {
                    ...last[last.length - 1],
                    reasoning: currentReasoning,
                    status: 'reasoning'
                  };
                  return last;
                });
              } else if (data.type === 'content') {
                setMessages(prev => {
                  const last = [...prev];
                  last[last.length - 1] = {
                    ...last[last.length - 1],
                    content: data.content,
                  };
                  return last;
                });
              } else if (data.type === 'error') {
                setMessages(prev => {
                  const last = [...prev];
                  last[last.length - 1] = {
                    ...last[last.length - 1],
                    content: `Error: ${data.content}`,
                    status: 'error'
                  };
                  return last;
                });
              } else if (data.type === 'status' && data.content === 'completed') {
                setMessages(prev => {
                  const last = [...prev];
                  last[last.length - 1] = {
                    ...last[last.length - 1],
                    status: 'completed'
                  };
                  return last;
                });
                fetchFiles();
              } else if (data.type === 'done') {
                setIsLoading(false);
              }
            } catch (e) {
              // Ignore parse errors for incomplete JSON
            }
          }
        }
      }
    } catch (error) {
      console.error('Error in chat:', error);
      setIsLoading(false);
    }
  };

  const downloadFile = (path: string) => {
    window.open(`/api/files/${path}`, '_blank');
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileText size={20} color="#6366f1" />
            <h2 style={{ fontSize: '1.25rem' }}>Workspace</h2>
          </div>
          <button onClick={fetchFiles} style={{ marginTop: '1rem', background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <RefreshCw size={14} /> Refresh
          </button>
        </div>
        <div className="file-list">
          {files.map((file, i) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              key={file.path}
              className="file-item"
              onClick={() => downloadFile(file.path)}
            >
              <FileText size={18} color="#94a3b8" />
              <div className="file-info">
                <div className="file-name">{file.name}</div>
                <div className="file-size">{(file.size / 1024).toFixed(1)} KB</div>
              </div>
              <Download size={14} color="#94a3b8" style={{ marginLeft: 'auto' }} />
            </motion.div>
          ))}
          {files.length === 0 && (
            <div style={{ textAlign: 'center', color: '#64748b', marginTop: '2rem', fontSize: '0.875rem' }}>
              No files generated yet
            </div>
          )}
        </div>
      </div>

      {/* Main Chat */}
      <div className="main-content">
        <div className="chat-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ width: '40px', height: '40px', background: '#6366f1', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Terminal color="white" size={24} />
            </div>
            <div>
              <h1 style={{ fontSize: '1.125rem' }}>MetaGPT Reimagined</h1>
              <div style={{ fontSize: '0.75rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                <div style={{ width: '6px', height: '6px', background: '#10b981', borderRadius: '50%' }}></div>
                System Online
              </div>
            </div>
          </div>
        </div>

        <div className="messages-container">
          <AnimatePresence>
            {messages.length === 0 && (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: '#64748b' }}>
                <MessageSquare size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                <p>Start a new project with MetaGPT</p>
                <p style={{ fontSize: '0.875rem' }}>e.g., "Design a simple snake game in Python"</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={i}
                className={`message ${msg.role}`}
              >
                <div className="message-bubble">
                  {msg.role === 'assistant' && msg.reasoning && (
                    <div className="reasoning-panel">
                      <div className="reasoning-title">
                        <Terminal size={12} style={{ marginRight: '0.25rem' }} />
                        Execution Reasoning
                      </div>
                      <div className="reasoning-content">{msg.reasoning}</div>
                    </div>
                  )}
                  <div className="markdown-body" dangerouslySetInnerHTML={{ __html: md.render(msg.content || (msg.status === 'reasoning' ? 'Analyzing and executing...' : '')) }} />
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              placeholder="What do you want to build today?"
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <button
              className="send-button"
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? <RefreshCw className="animate-spin" size={20} /> : <Send size={20} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
