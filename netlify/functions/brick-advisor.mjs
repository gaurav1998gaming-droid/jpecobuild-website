const systemPrompt = `You are JP Ecobuild Creations' website assistant. You may only answer questions about fly ash bricks: choosing and using them, their properties, estimating quantities, and ordering fly ash bricks from JP Ecobuild in Muradnagar/Ghaziabad. If a user asks about anything else, politely say you can only help with fly ash bricks and invite a related question.

Keep answers concise, practical, and specific to fly ash bricks. Do not recommend other brick types or unrelated products. Never invent prices, stock, delivery promises, certifications, test results, or exact product specifications. The website mentions 9 x 4.5 x 3 inches as the calculator's assumed brick size; clarify that this is an estimate and ask the customer to confirm the actual product size with JP Ecobuild. For current price, availability, delivery, or project-specific engineering advice, direct the user to call +91 81719 59076 or WhatsApp https://wa.me/918171959076. Do not claim to be a human or to have checked live inventory.`;

function jsonResponse(statusCode, body) {
  return new Response(JSON.stringify(body), {
    status: statusCode,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    }
  });
}

export default async (request) => {
  if (request.method !== "POST") {
    return jsonResponse(405, { error: "Method not allowed." });
  }

  const apiKey = process.env.GLM_API_KEY;
  if (!apiKey) {
    return jsonResponse(503, { error: "The assistant has not been configured yet. Add GLM_API_KEY in Netlify." });
  }

  let payload;
  try {
    payload = await request.json();
  } catch {
    return jsonResponse(400, { error: "Please send a valid chat message." });
  }

  if (!Array.isArray(payload.messages) || payload.messages.length === 0 || payload.messages.length > 8) {
    return jsonResponse(400, { error: "Please send a valid chat history." });
  }

  const messages = [];
  for (const item of payload.messages) {
    if (!item || !["user", "assistant"].includes(item.role) || typeof item.content !== "string") {
      return jsonResponse(400, { error: "Please send a valid chat history." });
    }

    const content = item.content.trim();
    if (!content || content.length > 1200) {
      return jsonResponse(400, { error: "Messages must be between 1 and 1,200 characters." });
    }
    messages.push({ role: item.role, content });
  }

  if (messages.at(-1).role !== "user") {
    return jsonResponse(400, { error: "Please send a user message." });
  }

  try {
    const glmResponse = await fetch("https://api.z.ai/api/paas/v4/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: process.env.GLM_MODEL || "glm-5.3",
        messages: [{ role: "system", content: systemPrompt }, ...messages],
        max_tokens: 350,
        temperature: 0.3
      })
    });

    if (!glmResponse.ok) {
      console.error("GLM request failed with status", glmResponse.status);
      const errorByStatus = {
        400: "GLM rejected the request. Check that GLM_MODEL names a model available to your account.",
        401: "GLM rejected the API key. Confirm it is active and is a Standard API key.",
        403: "GLM denied API access. Check that your account and API permissions allow this model.",
        404: "GLM could not find the API endpoint or model. Verify the model name; GLM Coding Plan keys require their dedicated endpoint.",
        429: "The GLM API quota or rate limit was reached. Check your Z.AI account usage and limits."
      };
      const error = errorByStatus[glmResponse.status]
        || `GLM returned HTTP ${glmResponse.status}. Check the Netlify Function logs and Z.AI service status.`;
      return jsonResponse(502, { error });
    }

    const data = await glmResponse.json();
    const reply = data.choices?.[0]?.message?.content?.trim();
    if (!reply) {
      console.error("GLM returned a successful response without a chat message");
      return jsonResponse(502, { error: "GLM returned an unexpected response. Check the selected model and the Netlify Function logs." });
    }

    return jsonResponse(200, { reply });
  } catch (error) {
    console.error("Fly ash advisor request failed", error);
    return jsonResponse(502, { error: "The assistant is temporarily unavailable. Please try again." });
  }
};