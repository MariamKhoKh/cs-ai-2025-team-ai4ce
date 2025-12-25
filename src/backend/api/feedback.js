module.exports = (req, res) => {
  // Vercel exposes route params as query when using api/[name].js
  // expect: GET /api/feedback/<submissionId>
  const submissionId = req.query.submissionId || (req.url || '').split('/').pop() || 'unknown';

  // Allow cross-origin calls from frontend (adjust origin in production)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  return res.status(200).json({
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
};
