const express = require('express');
const openai = require('openai');

const app = express();
const port = process.env.PORT || 3000;

openai.apiKey = openai.apiKey = process.env.OPENAI_API_KEY;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.post('/chat', async (req, res) => {
  const { prompt } = req.body;

  const response = await openai.completion.create({
    prompt,
    model: "chatbot",
    max_tokens: 1024,
    temperature: 0.5,
  });

  res.send(response.choices[0].text);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
