const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

// 🦅 AHMAD RDX PRIVATE CONFIG
const HF_TOKEN = "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"; 
const MODEL_URL = "https://api-inference.huggingface.co/models/SG161222/RealVisXL_V4.0";

app.get('/api/rdx-edit', async (req, res) => {
    const { prompt, imageUrl } = req.query;

    if (!prompt || !imageUrl) {
        return res.status(400).json({ error: "Prompt aur ImageUrl lazmi hain ustad!" });
    }

    try {
        // 🎭 Heavy Generative Prompt Engineering
        const finalPrompt = `Professional 3D name art. The name "${prompt}" in 3D glowing gold letters. Background and vibe inspired by: ${imageUrl}. Cinematic lighting, 8k, realistic textures.`;

        const response = await axios({
            url: MODEL_URL,
            method: "POST",
            headers: { "Authorization": `Bearer ${HF_TOKEN}` },
            data: JSON.stringify({ inputs: finalPrompt }),
            responseType: "arraybuffer",
            timeout: 120000
        });

        res.set('Content-Type', 'image/png');
        res.send(response.data);

    } catch (error) {
        console.error(error.message);
        if (error.response && error.response.status === 503) {
            res.status(503).json({ error: "AI Engine is waking up. Please retry in 30 seconds." });
        } else {
            res.status(500).json({ error: "Internal Server Error" });
        }
    }
});

app.listen(PORT, () => console.log(`🦅 Ahmad RDX API is live on port ${PORT}`));
