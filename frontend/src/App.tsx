import { ChangeEvent, useState } from "react";

export default function App() {
  const [prompt, setPrompt] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const sendPrompt = async (): Promise<void> => {
    if (!prompt.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data: { response: string } = await res.json();
      console.log("Response from agent:", data);
      setResponse(data.response);
    } catch (error) {
      console.error("Request failed:", error);
      setResponse("Error contacting the agent.");
    }

    setLoading(false);
  };

  const handlePromptChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(e.target.value);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-2xl shadow-lg rounded-lg p-6 space-y-4">
        <h1 className="text-xl font-semibold">Agent Chat Interface</h1>
        <textarea
          value={prompt}
          onChange={handlePromptChange}
          placeholder="Type your request..."
          rows={3}
          className="w-full p-3 border border-gray-300 rounded resize-none"
        />
        <button
          onClick={sendPrompt}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Thinking..." : "Send"}
        </button>

        {response && (
          <div className="bg-gray-100 p-4 rounded text-gray-800 whitespace-pre-wrap">
            <strong>Agent response:</strong>
            <br />
            {response}
          </div>
        )}
      </div>
    </div>
  );
}
