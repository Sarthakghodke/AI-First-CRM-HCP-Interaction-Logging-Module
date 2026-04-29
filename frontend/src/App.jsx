import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/agent/chat",
        {
          message,
        }
      );

      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div
      style={{
        padding: "40px",
        fontFamily: "Arial",
      }}
    >
      <h1>AI-First CRM HCP Module</h1>

      <textarea
        rows="6"
        cols="60"
        placeholder="Enter interaction..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <br />
      <br />

      <button onClick={sendMessage}>
        Send to AI Agent
      </button>

      <h3>AI Response:</h3>

      <div
        style={{
          border: "1px solid gray",
          padding: "20px",
          width: "500px",
          minHeight: "100px",
        }}
      >
        {response}
      </div>
    </div>
  );
}

export default App;