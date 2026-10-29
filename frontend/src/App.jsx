
import { useEffect, useState } from "react";
import {
  Plus,
  MessageSquare,
  FileText,
  Sparkles,
  GitCompareArrows,
  Paperclip,
  ArrowUp,
  PanelLeftClose,
  Search,
  Settings,
  ChevronDown,
  Bot,
  Menu,
  X,
  LoaderCircle,
  RefreshCw,
  Trash2,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const tools = [
  { id: "chat", label: "Ask PDFs", icon: MessageSquare },
  { id: "summary", label: "Summarize", icon: Sparkles },
  { id: "compare", label: "Compare", icon: GitCompareArrows },
];

export default function App() {
  const [activeTool, setActiveTool] = useState("chat");
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [documents, setDocuments] = useState([]);
  const [documentsLoading, setDocumentsLoading] = useState(false);
  const [documentsError, setDocumentsError] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");

  const titles = {
    chat: "What would you like to know?",
    summary: "Understand a document faster.",
    compare: "Compare two documents.",
  };

  const descriptions = {
    chat: "Ask questions and explore answers grounded in your PDF documents.",
    summary: "Turn a long PDF into a clear, structured summary.",
    compare: "Find similarities, differences, and important details across PDFs.",
  };

  // Load indexed documents when the dashboard opens.
  useEffect(() => {
    loadDocuments();
  }, []);

  async function loadDocuments() {
    setDocumentsLoading(true);
    setDocumentsError("");

    try {
      const response = await fetch(`${API_URL}/api/documents`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not load documents.");
      }

      setDocuments(data.documents || []);
    } catch (error) {
      setDocumentsError(error.message);
    } finally {
      setDocumentsLoading(false);
    }
  }

  function startNewChat() {
    setMessages([]);
    setPrompt("");
    setSelectedFile(null);
    setUploadStatus("");
    setActiveTool("chat");
  }

  async function submitPrompt(event) {
    event.preventDefault();

    const question = prompt.trim();

    if (!question || isLoading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: question },
    ]);

    setPrompt("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "The chat request failed.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer || "The backend returned an empty answer.",
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `Unable to get an answer: ${error.message}. Check that FastAPI and Ollama are running.`,
          error: true,
        },
      ]);

      console.error("Chat API error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  // Upload and index a PDF through FastAPI.
  async function uploadSelectedPdf(file) {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setUploadStatus("Please select a PDF file.");
      return;
    }

    setSelectedFile(file);
    setUploadStatus(`Uploading ${file.name}...`);
    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "PDF upload failed.");
      }

      setUploadStatus(data.message || `${file.name} indexed successfully.`);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.message || `${file.name} uploaded and indexed successfully.`,
        },
      ]);

      await loadDocuments();
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `PDF upload failed: ${error.message}`,
          error: true,
        },
      ]);

      console.error("PDF upload error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  // Delete a PDF from the indexed document collection.
  async function removeDocument(filename) {
    const confirmed = window.confirm(
      `Remove "${filename}" from the document index?`
    );

    if (!confirmed) return;

    try {
      const response = await fetch(
        `${API_URL}/api/documents/${encodeURIComponent(filename)}`,
        { method: "DELETE" }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not delete this document.");
      }

      setUploadStatus(data.message || `${filename} removed from the index.`);
      await loadDocuments();
    } catch (error) {
      setDocumentsError(error.message);
    }
  }

  return (
    <div className="app-shell">
      {sidebarOpen && (
        <aside className="sidebar">
          <div className="sidebar-top">
            <a
              className="brand"
              href="#"
              onClick={(event) => {
                event.preventDefault();
                startNewChat();
              }}
            >
              <span className="brand-mark">
                <Bot size={22} />
              </span>

              <span>
                DocuMind<span className="brand-accent"> AI</span>
              </span>
            </a>

            <button
              className="icon-button"
              onClick={() => setSidebarOpen(false)}
              aria-label="Close sidebar"
            >
              <PanelLeftClose size={19} />
            </button>
          </div>

          <button className="new-chat-button" onClick={startNewChat}>
            <Plus size={18} />
            <span>New chat</span>
            <span className="shortcut">Ctrl K</span>
          </button>

          <button
            className="sidebar-search"
            onClick={() =>
              document.querySelector(".prompt-input")?.focus()
            }
          >
            <Search size={17} />
            <span>Search conversations</span>
          </button>

          <div className="sidebar-section-label">WORKSPACE</div>

          <div className="sidebar-tools">
            {tools.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                className={`sidebar-item ${
                  activeTool === id ? "active" : ""
                }`}
                onClick={() => setActiveTool(id)}
              >
                <Icon size={18} />
                <span>{label}</span>
              </button>
            ))}
          </div>

          <div className="sidebar-section-label">
            DOCUMENTS ({documents.length})
          </div>

          <div className="document-actions">
            <button
              className="sidebar-item"
              onClick={loadDocuments}
              disabled={documentsLoading}
            >
              <RefreshCw
                size={17}
                className={documentsLoading ? "spin-icon" : ""}
              />
              <span>
                {documentsLoading ? "Refreshing..." : "Refresh documents"}
              </span>
            </button>
          </div>

          {documentsError && (
            <p className="empty-history">{documentsError}</p>
          )}

          {!documentsError &&
            documents.map((doc) => (
              <div className="document-row" key={doc.filename}>
                <FileText size={16} />

                <span className="document-name" title={doc.filename}>
                  {doc.filename}
                </span>

                <button
                  className="document-delete"
                  title={`Remove ${doc.filename} from index`}
                  aria-label={`Remove ${doc.filename}`}
                  onClick={() => removeDocument(doc.filename)}
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))}

          {!documentsLoading &&
            !documentsError &&
            documents.length === 0 && (
              <p className="empty-history">No indexed PDFs yet.</p>
            )}

          <div className="sidebar-section-label recent-label">
            RECENT
          </div>

          {messages.length > 0 ? (
            <button
              className="sidebar-item recent-item"
              onClick={() =>
                document
                  .querySelector(".conversation")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              <MessageSquare size={17} />

              <span>
                {messages.find((message) => message.role === "user")
                  ?.content.slice(0, 27) || "Recent activity"}
                …
              </span>
            </button>
          ) : (
            <p className="empty-history">
              Your conversations will appear here.
            </p>
          )}

          <div className="sidebar-bottom">
            <div className="profile-avatar">T</div>

            <div className="profile-copy">
              <strong>Personal workspace</strong>
              <span>Local AI assistant</span>
            </div>

            <Settings size={18} className="settings-icon" />
          </div>
        </aside>
      )}

      <main className="main-panel">
        <header className="topbar">
          <div className="topbar-left">
            {!sidebarOpen && (
              <button
                className="icon-button"
                onClick={() => setSidebarOpen(true)}
                aria-label="Open sidebar"
              >
                <Menu size={20} />
              </button>
            )}

            <span className="breadcrumb">Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <span className="breadcrumb-current">DocuMind AI</span>
            <ChevronDown size={15} className="breadcrumb-chevron" />
          </div>

          <div className="topbar-right">
            <span className="local-status">
              <span className="status-dot" />
              Local model
            </span>

            <button className="model-button">
              <Sparkles size={15} />
              DocuMind
              <ChevronDown size={14} />
            </button>
          </div>
        </header>

        <section
          className={`workspace ${
            messages.length ? "has-messages" : ""
          }`}
        >
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-orb">
                <Sparkles size={25} />
              </div>

              <div className="eyebrow">
                YOUR DOCUMENT INTELLIGENCE WORKSPACE
              </div>

              <h1>{titles[activeTool]}</h1>

              <p className="welcome-description">
                {descriptions[activeTool]}
              </p>

              <div className="tool-switcher">
                {tools.map(({ id, label, icon: Icon }) => (
                  <button
                    key={id}
                    className={`tool-pill ${
                      activeTool === id ? "selected" : ""
                    }`}
                    onClick={() => setActiveTool(id)}
                  >
                    <Icon size={17} />
                    {label}
                  </button>
                ))}
              </div>

              <div className="suggestion-grid">
                {[
                  {
                    icon: FileText,
                    title: "Explore a PDF",
                    text: "Ask questions about indexed documents.",
                  },
                  {
                    icon: Sparkles,
                    title: "Get a summary",
                    text: "Extract key points from a document.",
                  },
                  {
                    icon: GitCompareArrows,
                    title: "Compare files",
                    text: "Discover differences between PDFs.",
                  },
                ].map(({ icon: Icon, title, text }, index) => (
                  <button
                    key={title}
                    className="suggestion-card"
                    onClick={() => {
                      setActiveTool(["chat", "summary", "compare"][index]);

                      setPrompt(
                        [
                          "What are the key ideas in my documents?",
                          "Summarize the main points of my document.",
                          "Compare the key points in my documents.",
                        ][index]
                      );

                      setTimeout(
                        () =>
                          document
                            .querySelector(".prompt-input")
                            ?.focus(),
                        0
                      );
                    }}
                  >
                    <span className="suggestion-icon">
                      <Icon size={19} />
                    </span>

                    <strong>{title}</strong>
                    <span>{text}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="conversation">
              <div className="conversation-heading">
                <span className="conversation-icon">
                  <MessageSquare size={18} />
                </span>
                <span>Your conversation</span>
              </div>

              {messages.map((message, index) => (
                <div
                  className={`message-row ${message.role}`}
                  key={`${index}-${message.role}`}
                >
                  <div className="message-avatar">
                    {message.role === "user" ? (
                      "T"
                    ) : (
                      <Bot size={18} />
                    )}
                  </div>

                  <div className="message-content">
                    <span className="message-author">
                      {message.role === "user" ? "You" : "DocuMind AI"}
                    </span>

                    <p>{message.content}</p>

                    {message.sources?.length > 0 && (
                      <div className="source-list">
                        <strong>
                          <FileText size={15} />
                          Sources
                        </strong>

                        {message.sources.map((source, sourceIndex) => (
                          <details
                            key={`${source.source}-${source.page}-${sourceIndex}`}
                          >
                            <summary>
                              {source.source || "PDF"} · Page{" "}
                              {source.page ?? "Unknown"}
                            </summary>

                            <p>{source.text}</p>
                          </details>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="message-row assistant">
                  <div className="message-avatar">
                    <Bot size={18} />
                  </div>

                  <div className="message-content">
                    <span className="message-author">DocuMind AI</span>

                    <p className="loading-message">
                      <LoaderCircle size={16} />
                      Processing your request...
                    </p>
                  </div>
                </div>
              )}

              <div id="conversation-bottom" />
            </div>
          )}

          <div className="composer-wrap">
            {selectedFile && (
              <div className="attached-file">
                <FileText size={16} />
                <span>{selectedFile.name}</span>

                <button
                  onClick={() => setSelectedFile(null)}
                  aria-label="Clear selected file"
                >
                  <X size={15} />
                </button>
              </div>
            )}

            {uploadStatus && (
              <p className="upload-status">{uploadStatus}</p>
            )}

            <form className="composer" onSubmit={submitPrompt}>
              <label className="composer-attach" title="Upload and index a PDF">
                <Paperclip size={19} />

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  hidden
                  onChange={(event) => {
                    const file = event.target.files?.[0];

                    if (file) {
                      uploadSelectedPdf(file);
                    }

                    event.target.value = "";
                  }}
                />
              </label>

              <textarea
                className="prompt-input"
                placeholder={
                  activeTool === "chat"
                    ? "Ask anything about your indexed documents..."
                    : activeTool === "summary"
                    ? "Ask for a summary of an indexed PDF..."
                    : "Ask about differences between your documents..."
                }
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    event.currentTarget.form.requestSubmit();
                  }
                }}
                rows={1}
              />

              <button
                className={`send-button ${
                  prompt.trim() && !isLoading ? "ready" : ""
                }`}
                type="submit"
                disabled={!prompt.trim() || isLoading}
                aria-label="Send message"
              >
                {isLoading ? (
                  <LoaderCircle size={19} />
                ) : (
                  <ArrowUp size={19} />
                )}
              </button>
            </form>

            <div className="composer-footnote">
              <span>
                <Sparkles size={13} />
                Powered by your local AI pipeline
              </span>

              <span>AI can make mistakes. Verify important information.</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
