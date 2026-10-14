
import { useEffect, useState } from "react";
import {
  X,
  BrainCircuit,
  AlertTriangle,
  CheckCircle2,
  Tag,
  LoaderCircle,
} from "lucide-react";

import {
  analyzePost,
  type AnalysisResult,
  type Discussion,
} from "../services/api";

import "./IssueAnalyzer.css";

interface IssueAnalyzerProps {
  post: Discussion | null;
  onClose: () => void;
}

export default function IssueAnalyzer({
  post,
  onClose,
}: IssueAnalyzerProps) {
  const [analysis, setAnalysis] =
    useState<AnalysisResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!post) {
      return;
    }

    let cancelled = false;

    async function loadAnalysis() {
      setLoading(true);
      setAnalysis(null);
      setError(null);

      try {
        const result = await analyzePost(post!.id);

        if (!cancelled) {
          setAnalysis(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Analysis failed"
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAnalysis();

    return () => {
      cancelled = true;
    };
  }, [post]);

  if (!post) {
    return null;
  }

  return (
    <div
      className="analyzer-overlay"
      onClick={onClose}
    >
      <aside
        className="analyzer-panel"
        role="dialog"
        aria-modal="true"
        aria-label="Discussion analysis"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="analyzer-header">
          <div>
            <span className="analyzer-eyebrow">
              THREADLENS ANALYZER
            </span>
            <h2>Discussion Insights</h2>
          </div>

          <button
            className="analyzer-close"
            onClick={onClose}
            aria-label="Close analyzer"
          >
            <X size={20} />
          </button>
        </header>

        <div className="analyzer-body">
          <section className="analyzer-original">
            <p className="analyzer-course">
              {post.course}
            </p>

            <h3>{post.title}</h3>
            <p>{post.content}</p>
          </section>

          {loading && (
            <div className="analyzer-loading">
              <LoaderCircle
                className="analyzer-spinner"
                size={24}
              />
              Analyzing discussion...
            </div>
          )}

          {error && (
            <div className="analyzer-error">
              {error}
            </div>
          )}

          {analysis && (
            <>
              <section className="analyzer-section">
                <h3>
                  <BrainCircuit size={18} />
                  Discussion Summary
                  <h3>AI Explanation</h3>
                <p>{analysis.reasoning}</p>
                </h3>

                <p>{analysis.summary}</p>
              </section>

              <div className="analyzer-metrics">
                <section className="analyzer-metric">
                  <span>Topic</span>
                  <strong>{analysis.topic}</strong>
                </section>

                <section className="analyzer-metric">
                  <span>Urgency</span>
                  <strong
                    className={`urgency-${analysis.urgency}`}
                  >
                    <AlertTriangle size={16} />
                    {analysis.urgency}
                  </strong>
                </section>

                <section className="analyzer-metric">
                  <span>Status</span>
                  <strong>
                    <CheckCircle2 size={16} />
                    {analysis.status}
                  </strong>
                </section>
              </div>

              <section className="analyzer-section">
                <h3>
                  <Tag size={18} />
                  Extracted Keywords
                </h3>

                <div className="analyzer-keywords">
                  {analysis.keywords.map((keyword) => (
                    <span key={keyword}>
                      {keyword}
                    </span>
                  ))}
                </div>
              </section>

              <div className="analyzer-method">
                Analysis method: {analysis.analysis_method}
              </div>
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
