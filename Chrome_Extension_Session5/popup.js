document.getElementById("sendBtn").addEventListener("click", async () => {
  const query = document.getElementById("queryInput").value;
  const output = document.getElementById("output");
  output.textContent = "⏳ Solving...";

  try {
    const response = await fetch("http://localhost:8000/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query })
    });

    const data = await response.json();

    if (data.error) {
      output.textContent = "❌ Error: " + data.error;
    } else {
      const logSteps = (data.log || []).map((step, idx) => `${idx + 1}. ${step}`).join("\n");
      output.textContent = `✅ ${data.result}\n\n🧠 Log:\n${logSteps}`;
    }
  } catch (err) {
    output.textContent = "❌ Request failed. Make sure the FastAPI server is running.";
    console.error(err);
  }
});
