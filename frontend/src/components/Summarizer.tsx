import { useEffect, useState } from "react";
import {
  getCourses,
  summarizeCourse,
  type CourseSummary,
} from "../services/api";
import "./Summarizer.css";

export default function Summarizer() {
  const [courses, setCourses] = useState<string[]>([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [summary, setSummary] = useState<CourseSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCourses()
      .then((data) => {
        setCourses(data);
        if (data.length > 0) {
          setSelectedCourse(data[0]);
        }
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  async function handleGenerate() {
    if (!selectedCourse) return;

    setLoading(true);
    setError(null);
    setSummary(null);

    try {
      const result = await summarizeCourse(selectedCourse);
      setSummary(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="summarizer-page">
      <div className="summarizer-header">
        <h1>AI Summarizer</h1>
        <p>
          Transform student discussions into actionable teaching insights.
        </p>
      </div>

      <div className="summarizer-controls">
        <label htmlFor="course-select">Select Course</label>

        <select
          id="course-select"
          value={selectedCourse}
          onChange={(event) => {
            setSelectedCourse(event.target.value);
            setSummary(null);
          }}
        >
          {courses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>

        <button
          onClick={handleGenerate}
          disabled={loading || !selectedCourse}
        >
          {loading ? "Generating..." : "Generate Summary"}
        </button>
      </div>

      {error && <p className="summarizer-error">{error}</p>}

      {loading && (
        <p className="summarizer-loading">
          Analyzing discussions with Llama 3.2. This may take a while...
        </p>
      )}

      {summary && (
        <div className="summarizer-results">
          <h2>{summary.course} — Course Summary</h2>

          <div className="summarizer-stats">
            <div className="summary-stat">
              <span>Total Discussions</span>
              <strong>{summary.statistics.total_discussions}</strong>
            </div>

            <div className="summary-stat">
              <span>Unresolved</span>
              <strong>{summary.statistics.unresolved}</strong>
            </div>

            <div className="summary-stat">
              <span>High Urgency (Analyzed)</span>
              <strong>
                {summary.statistics.high_urgency_analyzed}
              </strong>
            </div>
          </div>

          <div className="summary-section">
            <h3>AI Overview</h3>
            <p>{summary.insights.overview}</p>
          </div>

          <div className="summary-section">
            <h3>Common Topics</h3>

            {summary.statistics.common_topics.length === 0 ? (
              <p>No topics identified.</p>
            ) : (
              <ul>
                {summary.statistics.common_topics.map((item) => (
                  <li key={item.topic}>
                    {item.topic} — {item.count} discussions
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="summary-section">
            <h3>Key Student Challenges</h3>

            {summary.insights.key_challenges.length === 0 ? (
              <p>No AI-generated challenges available.</p>
            ) : (
              <ul>
                {summary.insights.key_challenges.map((challenge, index) => (
                  <li key={index}>{challenge}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="summary-section">
            <h3>Recommended Instructor Actions</h3>

            {summary.insights.recommended_actions.length === 0 ? (
              <p>No AI-generated recommendations available.</p>
            ) : (
              <ul>
                {summary.insights.recommended_actions.map((action, index) => (
                  <li key={index}>{action}</li>
                ))}
              </ul>
            )}
          </div>

          <p className="summary-footer">
            Analyzed {summary.statistics.analyzed_discussions} of{" "}
            {summary.statistics.total_discussions} discussions.
            {" "}Method: {summary.report_method}
          </p>
        </div>
      )}
    </div>
  );
}