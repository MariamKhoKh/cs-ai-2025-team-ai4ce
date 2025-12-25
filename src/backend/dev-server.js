const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/api/feedback/:submissionId', (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  const submissionId = req.params.submissionId;
  if (!submissionId) return res.status(400).json({ error: 'missing submissionId' });

  res.json({
    submissionId,
    score: 85,
    correctedCode: "// corrected example code\nfunction example(){ return true; }",
    issues: [
      { title: "Missing edge-case handling", description: "Does not handle empty input", severity: "medium", line: 3 }
    ],
    strengths: ["Clear naming", "Modular functions"],
    recommendations: ["Add input validation", "Use hashmap to optimize"],
    explanation: "Your solution works for typical cases but fails on empty inputs. Add a guard clause at the top."
  });
});

app.get('/api/feedback', (req, res) => {
  const submissionId = req.query.submissionId || 'unknown';
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.json({ submissionId, score: 85, explanation: 'Use /api/feedback/:id or ?submissionId=...' });
});

app.listen(port, () => {
  console.log(`Dev server running at http://localhost:${port}`);
});
