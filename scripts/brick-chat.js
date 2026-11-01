const chatForm = document.getElementById("brickChatForm");
const chatInput = document.getElementById("brickChatInput");
const chatMessages = document.getElementById("brickChatMessages");
const chatStatus = document.getElementById("brickChatStatus");
const chatSend = document.getElementById("brickChatSend");
const chatHistory = [];

function addChatMessage(role, text) {
  const message = document.createElement("p");
  message.className = `brick-chat-message ${role}`;
  message.textContent = text;
  chatMessages.append(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendChatMessage(text) {
  const message = text.trim();
  if (!message || chatSend.disabled) return;

  addChatMessage("user", message);
  chatHistory.push({ role: "user", content: message });
  chatInput.value = "";
  chatSend.disabled = true;
  chatStatus.dataset.state = "loading";
  chatStatus.textContent = "Thinking about your fly ash brick question...";

  try {
    if (window.location.protocol === "file:") {
      throw new Error("This local file preview cannot connect to the AI. Open the site through Netlify Dev or use the deployed Netlify site.");
    }

    const response = await fetch("/.netlify/functions/brick-advisor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: chatHistory.slice(-8) })
    });
    const result = await response.json().catch(() => null);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("The chat service is not deployed yet. Deploy the Netlify Function and configure GLM_API_KEY in Netlify.");
      }
      throw new Error(result?.error || "The assistant is unavailable right now.");
    }

    if (typeof result?.reply !== "string" || !result.reply.trim()) {
      throw new Error("The assistant is unavailable right now. Please try again later.");
    }

    addChatMessage("assistant", result.reply);
    chatHistory.push({ role: "assistant", content: result.reply });
    chatStatus.textContent = "For current prices and availability, contact JP Ecobuild.";
  } catch (error) {
    chatHistory.pop();
    const message = error instanceof TypeError
      ? "Chat is available on the published website. Please try again later."
      : error.message || "Sorry, I could not answer just now. Please try again.";
    addChatMessage("assistant", message);
    chatStatus.textContent = "Check your connection or try again later.";
    chatStatus.dataset.state = "error";
  } finally {
    chatSend.disabled = false;
    chatInput.focus();
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendChatMessage(chatInput.value);
});

document.querySelectorAll(".brick-chat-prompts [data-prompt]").forEach((button) => {
  button.addEventListener("click", () => sendChatMessage(button.dataset.prompt));
});

chatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});