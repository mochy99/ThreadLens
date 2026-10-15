
const API_URL = "http://127.0.0.1:8000";

export interface Analytics {
  total_posts: number;
  resolved: number;
  unresolved: number;
  in_progress: number;
  unknown: number;
  resolution_rate: number;
}

export interface Topic {
  topic: string;
  count: number;
}

export interface Discussion {
  id: string | number;
  title: string;
  content: string;
  course: string;
  status: string;
  tags: string[];
  created_at: string;
}

export async function getAnalytics(): Promise<Analytics> {
  const response = await fetch(`${API_URL}/api/analytics`);

  if (!response.ok) {
    throw new Error("Failed to fetch analytics");
  }

  return response.json();
}

export async function getTopics(): Promise<Topic[]> {
  const response = await fetch(
    `${API_URL}/api/analytics/topics`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch topics");
  }

  const data = await response.json();
  return data.topics;
}

export async function getPosts(): Promise<Discussion[]> {
  const response = await fetch(
    `${API_URL}/api/posts?limit=100`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch discussions");
  }

  const data = await response.json();
  return data.posts;
}

export interface AnalysisResult {
  post_id: string | number;
  summary: string;
  topic: string;
  urgency: "low" | "medium" | "high";
  status: string;
  keywords: string[];
  analysis_method: string;
}

export async function analyzePost(
  postId: string | number
): Promise<AnalysisResult> {
  const response = await fetch(
    `${API_URL}/api/analyze/${encodeURIComponent(postId)}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to analyze discussion (${response.status})`
    );
  }

  return response.json();
}


export interface AnalysisResult {
  post_id: string | number;
  summary: string;
  topic: string;
  urgency: "low" | "medium" | "high";
  status: string;
  keywords: string[];
  reasoning?: string;
  analysis_method: string;
}
export interface TopicCount {
  topic: string;
  count: number;
}

export interface CourseSummary {
  course: string;
  generated_at: string;
  statistics: {
    total_discussions: number;
    unresolved: number;
    resolved: number;
    analyzed_discussions: number;
    high_urgency_analyzed: number;
    common_topics: TopicCount[];
  };
  insights: {
    overview: string;
    key_challenges: string[];
    recommended_actions: string[];
  };
  report_method: string;
}

export async function getCourses(): Promise<string[]> {
  const response = await fetch(`${API_URL}/api/summarizer/courses`);

  if (!response.ok) {
    throw new Error("Failed to load courses");
  }

  const data: { courses: string[] } = await response.json();
  return data.courses;
}

export async function summarizeCourse(
  course: string
): Promise<CourseSummary> {
  const response = await fetch(
    `${API_URL}/api/summarizer/${encodeURIComponent(course)}`
  );

  if (!response.ok) {
    throw new Error("Failed to generate course summary");
  }

  return response.json();
}