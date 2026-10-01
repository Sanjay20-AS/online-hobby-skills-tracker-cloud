
import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function api(path, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {};

  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  const response = await fetch(API + path, {
    ...options,
    headers: headers,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
  const message =
    typeof data.detail === "string"
      ? data.detail
      : JSON.stringify(data.detail);

  throw new Error(message || "Request failed");
}

  return data;
}

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");

  const [form, setForm] = useState({
    email: "",
    password: "",
    username: "",
  });

  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      const data = await api(
        mode === "login"
          ? "/api/auth/login"
          : "/api/auth/register",
        {
          method: "POST",
          body: JSON.stringify(form),
        }
      );

      localStorage.setItem("token", data.access_token);
      onLogin(data.user);
    } catch (error) {
      setError(error.message);
    }
  }

  return (
    <div className="auth">
      <div className="auth-card">
        <h1>HobbyTrack ☁️</h1>

        <p>Track skills. Build habits. Share progress.</p>

        <form onSubmit={submit}>
          {mode === "register" && (
            <input
              placeholder="Username"
              value={form.username}
              onChange={(e) =>
                setForm({
                  ...form,
                  username: e.target.value,
                })
              }
            />
          )}

          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) =>
              setForm({
                ...form,
                email: e.target.value,
              })
            }
          />

          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) =>
              setForm({
                ...form,
                password: e.target.value,
              })
            }
          />

          {error && <div className="error">{error}</div>}

          <button type="submit">
            {mode === "login" ? "Login" : "Create account"}
          </button>
        </form>

        <button
          type="button"
          className="link"
          onClick={() =>
            setMode(
              mode === "login"
                ? "register"
                : "login"
            )
          }
        >
          {mode === "login"
            ? "Create a new account"
            : "Already have an account?"}
        </button>
      </div>
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState("dashboard");

  useEffect(() => {
    if (localStorage.getItem("token")) {
      api("/api/auth/me")
        .then(setUser)
        .catch(() => {
          localStorage.removeItem("token");
        });
    }
  }, []);

  if (!user) {
    return <Auth onLogin={setUser} />;
  }

  function logout() {
    localStorage.removeItem("token");
    setUser(null);
  }

  const navigationItems = [
    "dashboard",
    "skills",
    "goals",
    "practice",
    "community",
    "analytics",
  ];

  return (
    <div className="app">
      <aside>
        <h2>HobbyTrack</h2>

        {navigationItems.map((item) => (
          <button
            key={item}
            className={tab === item ? "active" : ""}
            onClick={() => setTab(item)}
          >
            {item.charAt(0).toUpperCase() +
              item.slice(1)}
          </button>
        ))}

        <button onClick={logout}>Logout</button>
      </aside>

      <main>
        <header>
          <div>
            <small>Welcome back</small>
            <h1>{user.username} 👋</h1>
          </div>

          <span className="pill">Cloud-ready</span>
        </header>

        {tab === "dashboard" && <Dashboard />}
        {tab === "skills" && <Skills />}
        {tab === "goals" && <Goals />}
        {tab === "practice" && <Practice />}
        {tab === "community" && <Community />}
        {tab === "analytics" && <Analytics />}
      </main>
    </div>
  );
}

function Dashboard() {
  const [data, setData] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    api("/api/analytics/overview")
      .then(setData)
      .catch(console.error);

    api("/api/posts/feed")
      .then(setPosts)
      .catch(console.error);
  }, []);

  if (!data) {
    return <p>Loading...</p>;
  }

  const cards = [
    ["Skills", data.skills],
    ["Active goals", data.active_goals],
    ["Practice hours", data.practice_hours],
    ["Posts", data.posts],
  ];

  return (
    <>
      <div className="cards">
        {cards.map((item) => (
          <div className="card" key={item[0]}>
            <small>{item[0]}</small>
            <strong>{item[1]}</strong>
          </div>
        ))}
      </div>

      <section className="panel">
        <h2>Recent community activity</h2>

        {posts.slice(0, 3).map((post) => (
          <article className="post" key={post.id}>
            <b>@{post.username}</b>
            <p>{post.content}</p>

            <small>
              ❤️ {post.likes} · 💬 {post.comments}
            </small>
          </article>
        ))}
      </section>
    </>
  );
}

function Skills() {
  const [items, setItems] = useState([]);

  const [name, setName] = useState("");
  const [category, setCategory] = useState("Programming");
  const [currentLevel, setCurrentLevel] = useState("Beginner");
  const [targetLevel, setTargetLevel] = useState("Intermediate");
  const [description, setDescription] = useState("");

  function load() {
    api("/api/skills")
      .then(setItems)
      .catch(console.error);
  }

  useEffect(() => {
    load();
  }, []);

  async function add(e) {
    e.preventDefault();

    if (!name.trim()) {
      alert("Please enter a skill name.");
      return;
    }

    try {
      await api("/api/skills", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          category: category,
          current_level: currentLevel,
          target_level: targetLevel,
          description: description.trim(),
        }),
      });

      setName("");
      setCategory("Programming");
      setCurrentLevel("Beginner");
      setTargetLevel("Intermediate");
      setDescription("");

      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  async function deleteSkill(id) {
    if (!window.confirm("Delete this skill?")) {
      return;
    }

    try {
      await api("/api/skills/" + id, {
        method: "DELETE",
      });

      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  return (
    <section>
      <div className="panel">
        <h2>My Skills</h2>

        <form onSubmit={add}>
          <label>Skill Name</label>

          <input
            type="text"
            placeholder="e.g. Java"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <label>Category</label>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="Programming">Programming</option>
            <option value="AI/ML">AI / ML</option>
            <option value="Web Development">Web Development</option>
            <option value="Database">Database</option>
            <option value="Cloud">Cloud</option>
            <option value="Data Science">Data Science</option>
            <option value="Other">Other</option>
          </select>

          <label>Current Level</label>

          <select
            value={currentLevel}
            onChange={(e) => setCurrentLevel(e.target.value)}
          >
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>

          <label>Target Level</label>

          <select
            value={targetLevel}
            onChange={(e) => setTargetLevel(e.target.value)}
          >
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>

          <label>Description</label>

          <textarea
            placeholder="What do you want to learn?"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="3"
          />

          <button type="submit">Add Skill</button>
        </form>
      </div>

      {items.map((skill) => (
        <div className="panel" key={skill.id}>
          <div className="row">
            <h3>{skill.name}</h3>

            <button
              type="button"
              onClick={() => deleteSkill(skill.id)}
            >
              Delete
            </button>
          </div>

          <p>
            <b>Category:</b> {skill.category}
          </p>

          <p>
            <b>Current Level:</b> {skill.current_level}
          </p>

          <p>
            <b>Target Level:</b> {skill.target_level}
          </p>

          <p>
            {skill.description ||
              "Keep practicing to reach your target level."}
          </p>
        </div>
      ))}
    </section>
  );
}

function Goals() {
  const [items, setItems] = useState([]);

  const [title, setTitle] = useState("");
  const [targetValue, setTargetValue] = useState(100);
  const [currentValue, setCurrentValue] = useState(0);

  function load() {
    api("/api/goals")
      .then(setItems)
      .catch(console.error);
  }

  useEffect(() => {
    load();
  }, []);

  async function add(e) {
    e.preventDefault();

    if (!title.trim()) {
      alert("Please enter a goal title.");
      return;
    }

    if (Number(targetValue) <= 0) {
      alert("Target must be greater than 0.");
      return;
    }

    if (Number(currentValue) < 0) {
      alert("Current progress cannot be negative.");
      return;
    }

    try {
      await api("/api/goals", {
        method: "POST",
        body: JSON.stringify({
          title: title.trim(),
          target_value: Number(targetValue),
          current_value: Number(currentValue),
        }),
      });

      setTitle("");
      setTargetValue(100);
      setCurrentValue(0);

      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  return (
    <section>
      <div className="panel">
        <h2>Learning Goals</h2>

        <form onSubmit={add}>

          <label>Goal Title</label>
          <input
            type="text"
            placeholder="e.g. Improve Java DSA Skills"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <label>Target</label>
          <input
            type="number"
            min="1"
            placeholder="e.g. 100"
            value={targetValue}
            onChange={(e) => setTargetValue(e.target.value)}
          />

          <label>Current Progress</label>
          <input
            type="number"
            min="0"
            placeholder="e.g. 40"
            value={currentValue}
            onChange={(e) => setCurrentValue(e.target.value)}
          />

          <button type="submit">Add Goal</button>

        </form>
      </div>

      {items.map((goal) => {
        const target = Number(goal.target_value) || 1;
        const current = Number(goal.current_value) || 0;

        const percentage = Math.min(
          100,
          Math.round((current / target) * 100)
        );

        return (
          <div className="panel" key={goal.id}>

            <div className="row">
              <h3>{goal.title}</h3>
              <b>{percentage}%</b>
            </div>

            <p>
              Progress: {current} / {target}
            </p>

            <div className="progress">
              <span
                style={{
                  width: percentage + "%",
                }}
              />
            </div>

            <p>
              {goal.description ||
                "Keep practicing and update your progress."}
            </p>

          </div>
        );
      })}
    </section>
  );
}
function Practice() {
  const [items, setItems] = useState([]);
  const [activity, setActivity] = useState("");
  const [minutes, setMinutes] = useState(30);

  function load() {
    api("/api/practice")
      .then(setItems)
      .catch(console.error);
  }

  useEffect(() => {
    load();
  }, []);

  async function add(e) {
    e.preventDefault();

    if (!activity.trim()) {
      return;
    }

    try {
      await api("/api/practice", {
        method: "POST",
        body: JSON.stringify({
          activity: activity,
          duration_minutes: Number(minutes),
          practice_date: new Date()
            .toISOString()
            .slice(0, 10),
          notes: "",
        }),
      });

      setActivity("");
      load();
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <section>
      <div className="panel">
        <h2>Practice Session</h2>

        <form className="inline" onSubmit={add}>
          <input
            placeholder="What did you practice?"
            value={activity}
            onChange={(e) =>
              setActivity(e.target.value)
            }
          />

          <input
            type="number"
            min="1"
            value={minutes}
            onChange={(e) =>
              setMinutes(e.target.value)
            }
          />

          <button type="submit">Record</button>
        </form>
      </div>

      {items.map((item) => (
        <div className="post" key={item.id}>
          <b>{item.activity}</b>

          <p>
            {item.duration_minutes} minutes ·{" "}
            {item.practice_date}
          </p>
        </div>
      ))}
    </section>
  );
}

function Community() {
  const [posts, setPosts] = useState([]);
  const [content, setContent] = useState("");

  const [comments, setComments] = useState({});
  const [commentText, setCommentText] = useState({});
  const [openComments, setOpenComments] = useState({});

  function load() {
    api("/api/posts/feed")
      .then(setPosts)
      .catch(console.error);
  }

  useEffect(() => {
    load();
  }, []);

  async function add(e) {
    e.preventDefault();

    if (!content.trim()) {
      return;
    }

    try {
      await api("/api/posts", {
        method: "POST",
        body: JSON.stringify({
          content: content.trim(),
        }),
      });

      setContent("");
      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  async function like(id) {
    try {
      await api("/api/posts/" + id + "/like", {
        method: "POST",
      });

      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  async function loadComments(postId) {
    try {
      const data = await api(
        "/api/posts/" + postId + "/comments"
      );

      setComments((previous) => ({
        ...previous,
        [postId]: data,
      }));

      setOpenComments((previous) => ({
        ...previous,
        [postId]: true,
      }));
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  function toggleComments(postId) {
    if (openComments[postId]) {
      setOpenComments((previous) => ({
        ...previous,
        [postId]: false,
      }));
    } else {
      loadComments(postId);
    }
  }

  async function addComment(postId) {
    const text = commentText[postId] || "";

    if (!text.trim()) {
      return;
    }

    try {
      await api("/api/posts/" + postId + "/comments", {
        method: "POST",
        body: JSON.stringify({
          content: text.trim(),
        }),
      });

      setCommentText((previous) => ({
        ...previous,
        [postId]: "",
      }));

      await loadComments(postId);
      load();
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  }

  return (
    <section>
      <div className="panel">
        <h2>Community Feed</h2>

        <form onSubmit={add}>
          <textarea
            placeholder="Share a learning achievement..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />

          <button type="submit">
            Share Achievement
          </button>
        </form>
      </div>

      {posts.map((post) => (
        <article className="post" key={post.id}>
          <b>@{post.username}</b>

          <p>{post.content}</p>

          <button
            className="secondary"
            onClick={() => like(post.id)}
          >
            {post.liked ? "💔 Unlike" : "❤️ Like"}{" "}
            {post.likes}
          </button>

          <button
            className="secondary"
            onClick={() => toggleComments(post.id)}
          >
            💬 {post.comments} Comments
          </button>

          {openComments[post.id] && (
            <div className="comments">
              <h4>Comments</h4>

              {(comments[post.id] || []).map((comment) => (
                <div className="comment" key={comment.id}>
                  <b>@{comment.username}</b>
                  <p>{comment.content}</p>
                </div>
              ))}

              {(comments[post.id] || []).length === 0 && (
                <p>No comments yet. Be the first to comment!</p>
              )}

              <div className="inline">
                <input
                  type="text"
                  placeholder="Write a comment..."
                  value={commentText[post.id] || ""}
                  onChange={(e) =>
                    setCommentText((previous) => ({
                      ...previous,
                      [post.id]: e.target.value,
                    }))
                  }
                />

                <button
                  type="button"
                  onClick={() => addComment(post.id)}
                >
                  Comment
                </button>
              </div>
            </div>
          )}
        </article>
      ))}
    </section>
  );
}
function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api("/api/analytics/overview")
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return <p>Loading...</p>;
  }

  const cards = [
    ["Practice hours", data.practice_hours],
    ["Practice minutes", data.practice_minutes],
    ["Skills", data.skills],
    ["Goals", data.goals],
  ];

  return (
    <section>
      <h2>Personal Analytics</h2>

      <div className="cards">
        {cards.map((item) => (
          <div className="card" key={item[0]}>
            <small>{item[0]}</small>
            <strong>{item[1]}</strong>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Cloud data model</h3>

        <p>
          Your dashboard is generated from
          user-specific database records through REST
          APIs. The backend is stateless and persistent
          data lives outside the application instance.
        </p>
      </div>
    </section>
  );
}

createRoot(document.getElementById("root")).render(
  <App />
);


