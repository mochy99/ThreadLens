
import { useEffect, useState } from "react";
import {
  MessageSquare,
  CheckCircle,
  AlertCircle,
  Clock,
  RefreshCw,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getAnalytics,
  getTopics,
  getPosts,
  type Analytics,
  type Topic,
  type Discussion,
} from "./services/api";

import "./App.css";
import IssueAnalyzer from "./components/IssueAnalyzer";

function App() {
  const [analytics, setAnalytics] =
    useState<Analytics | null>(null);
    const [selectedPost, setSelectedPost] =
  useState<Discussion | null>(null);

  const [topics, setTopics] = useState<Topic[]>([]);
  const [posts, setPosts] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadDashboard() {
    setLoading(true);
    setError(null);

    try {
      const [stats, topicData, postData] =
        await Promise.all([
          getAnalytics(),
          getTopics(),
          getPosts(),
        ]);

      setAnalytics(stats);
      setTopics(topicData);
      setPosts(postData);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        Loading ThreadLens dashboard...
      </div>
    );
  }

  if (error || !analytics) {
    return (
      <div className="loading">
        <p>{error || "No analytics available"}</p>
        <button onClick={loadDashboard}>Retry</button>
      </div>
    );
  }

  const cards = [
    {
      label: "Total Discussions",
      value: analytics.total_posts,
      icon: MessageSquare,
    },
    {
      label: "Resolved",
      value: analytics.resolved,
      icon: CheckCircle,
    },
    {
      label: "Unresolved",
      value: analytics.unresolved,
      icon: AlertCircle,
    },
    {
      label: "In Progress",
      value: analytics.in_progress,
      icon: Clock,
    },
  ];

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>ThreadLens</h2>
        <p>Discussion Intelligence</p>

        <nav>
          <a className="active" href="#overview">
            Overview
          </a>
          <a href="#topics">Topics</a>
          <a href="#discussions">Discussions</a>
        </nav>
      </aside>

      <main className="main">
        <header className="header" id="overview">
          <div>
            <h1>Discussion Overview</h1>
            <p>
              AI-powered educational discussion analytics
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={loadDashboard}
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </header>

        <section className="stats-grid">
          {cards.map((card) => {
            const Icon = card.icon;

            return (
              <div className="stat-card" key={card.label}>
                <div className="stat-header">
                  <span>{card.label}</span>
                  <Icon size={22} />
                </div>

                <h2>{card.value}</h2>
              </div>
            );
          })}
        </section>

        <section className="chart-section" id="topics">
          <div className="section-heading">
            <h2>Discussion Topics</h2>
            <span>
              Resolution Rate: {analytics.resolution_rate}%
            </span>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topics}>
                <XAxis dataKey="topic" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar
                  dataKey="count"
                  fill="#6366f1"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section
          className="discussions-section"
          id="discussions"
        >
          <h2>Recent Discussions</h2>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Discussion</th>
                  <th>Course</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>

              <tbody>
                {posts.length === 0 ? (
                  <tr>
                    <td colSpan={4}>
                      No discussions found.
                    </td>
                  </tr>
                ) : (
                  posts.slice(0, 10).map((post) => (
                    <tr
                    key={post.id}
                    onClick={() => setSelectedPost(post)}
                    className="clickable-row"
                    tabIndex={0}
                    onKeyDown={(event) => {
                        if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        setSelectedPost(post);
                        }
                    }}
                    >
                      <td>{post.title}</td>
                      <td>{post.course}</td>
                      <td>
                        <span
                          className={`status ${post.status
                            .toLowerCase()
                            .replace(/\s+/g, "_")}`}
                        >
                          {post.status}
                        </span>
                      </td>
                      <td>
                        {post.created_at
                          ? new Date(
                              post.created_at
                            ).toLocaleDateString()
                          : "N/A"}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
            <IssueAnalyzer
            post={selectedPost}
            onClose={() => setSelectedPost(null)}
            />
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
