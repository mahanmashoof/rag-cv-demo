import { useState, useEffect } from "react";

export default function App() {
  const [questions, setQuestions] = useState<string[]>([]);
  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState("");
  const [sources, setSources] = useState<(string | { source: string })[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch questions from backend on mount
  useEffect(() => {
    fetch("http://localhost:8000/questions")
      .then((res) => res.json())
      .then((data) => setQuestions(data.questions))
      .catch((err) => console.error("Failed to load questions:", err));
  }, []);

  async function ask(question: string) {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      setAnswer(data.answer);
      setConfidence(data.confidence);
      setSources(data.sources);
    } finally {
      setLoading(false);
    }
  }

  const getConfidenceColor = (conf: string) => {
    if (conf === "High") return "#10b981";
    if (conf === "Medium") return "#f59e0b";
    return "#ef4444";
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        padding: "20px",
      }}
    >
      <div
        style={{
          maxWidth: "800px",
          margin: "0 auto",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: "40px",
            color: "white",
          }}
        >
          <h1
            style={{
              fontSize: "clamp(2rem, 5vw, 3rem)",
              marginBottom: "10px",
              fontWeight: "700",
            }}
          >
            🤖 CV RAG Demo
          </h1>
          <p style={{ opacity: 0.9, fontSize: "1.1rem" }}>
            Ask questions about our candidates
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gap: "12px",
            marginBottom: "30px",
          }}
        >
          {questions.map((q, index) => (
            <button
              key={index}
              onClick={() => ask(q)}
              disabled={loading}
              style={{
                background: "white",
                border: "none",
                borderRadius: "12px",
                padding: "16px 20px",
                fontSize: "1rem",
                fontWeight: "500",
                color: "#1f2937",
                cursor: loading ? "not-allowed" : "pointer",
                transition: "all 0.2s",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                textAlign: "left",
                opacity: loading ? 0.6 : 1,
              }}
              onMouseEnter={(e) => {
                if (!loading) {
                  e.currentTarget.style.transform = "translateY(-2px)";
                  e.currentTarget.style.boxShadow =
                    "0 6px 12px rgba(0,0,0,0.15)";
                }
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)";
              }}
            >
              💬 {q}
            </button>
          ))}
        </div>

        {loading && (
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              padding: "40px",
              textAlign: "center",
              boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                width: "40px",
                height: "40px",
                border: "4px solid #f3f4f6",
                borderTopColor: "#667eea",
                borderRadius: "50%",
                animation: "spin 1s linear infinite",
              }}
            />
            <p style={{ marginTop: "20px", color: "#6b7280" }}>
              Searching CVs...
            </p>
          </div>
        )}

        {answer && !loading && (
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              padding: "30px",
              boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "20px",
              }}
            >
              <h3
                style={{
                  margin: 0,
                  fontSize: "1.5rem",
                  color: "#1f2937",
                }}
              >
                ✨ Answer
              </h3>
              <span
                style={{
                  padding: "4px 12px",
                  borderRadius: "20px",
                  fontSize: "0.875rem",
                  fontWeight: "600",
                  background: getConfidenceColor(confidence),
                  color: "white",
                }}
              >
                {confidence}
              </span>
            </div>

            <p
              style={{
                fontSize: "1.1rem",
                lineHeight: "1.7",
                color: "#374151",
                marginBottom: "25px",
              }}
            >
              {answer}
            </p>

            {sources.length > 0 && (
              <div
                style={{
                  borderTop: "2px solid #e5e7eb",
                  paddingTop: "20px",
                }}
              >
                <h4
                  style={{
                    fontSize: "1rem",
                    color: "#6b7280",
                    marginBottom: "12px",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                  }}
                >
                  📄 Sources
                </h4>
                <div
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "8px",
                  }}
                >
                  {sources.map((s, index) => (
                    <span
                      key={index}
                      style={{
                        padding: "6px 14px",
                        background: "#f3f4f6",
                        borderRadius: "8px",
                        fontSize: "0.875rem",
                        color: "#374151",
                        fontWeight: "500",
                      }}
                    >
                      {typeof s === "string" ? s : s.source}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
