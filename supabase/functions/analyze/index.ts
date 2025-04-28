import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { Groq } from "npm:groq-sdk";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

function extractJsonFromString(string: string) {
  if (typeof string === "string" && string.trim().startsWith("FINAL_JSON:")) {
    string = string.trim().slice("FINAL_JSON:".length).trim();
  }

  try {
    const start = string.indexOf("{");
    const end = string.lastIndexOf("}") + 1;
    if (start !== -1 && end !== 0) {
      const jsonStr = string.slice(start, end);
      return JSON.parse(jsonStr);
    }
    console.log(`Warning: Could not find valid JSON structure in string: ${string}`);
    return null;
  } catch (e) {
    console.error("JSON extraction error:", e);
    return null;
  }
}

async function analyzeResume(jobDescription: string, resumeText: string) {
  const groqClient = new Groq({
    apiKey: Deno.env.get("GROQ_API_KEY"),
  });

  const prompt = `
Tu es Anto, un recruteur IA expert. À partir de la description de poste et du CV ci-dessous :

- Analyse et donne-moi uniquement ce JSON au format suivant :
{
  "overall_score": <0-100>,
  "skills_match": <0-100>,
  "experience_match": <0-100>,
  "education_match": <0-100>,
  "short_explanation": "explication naturelle en français sur la pertinence ou non du candidat en quelques phrases"
}

Aucune explication supplémentaire, juste le JSON valide.

---

Description du poste:
${jobDescription}

CV:
${resumeText}
`;

  try {
    const response = await groqClient.chat.completions.create({
      model: "llama3-70b-8192",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.2,
      max_tokens: 800,
    });

    const rawContent = response.choices[0].message.content.trim();
    return extractJsonFromString(rawContent);
  } catch (e) {
    console.error("Analysis error:", e);
    return null;
  }
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { job_description, files } = await req.json();

    if (!job_description || !files || !Array.isArray(files)) {
      return new Response(
        JSON.stringify({ error: "Invalid request format" }),
        {
          status: 400,
          headers: {
            "Content-Type": "application/json",
            ...corsHeaders,
          },
        }
      );
    }

    const results = await Promise.all(
      files.map(async (file) => {
        try {
          const analysis = await analyzeResume(job_description, file.content);
          
          if (!analysis) {
            return {
              filename: file.name,
              error: "Could not analyze this CV",
              score: 0,
              skills: 0,
              experience: 0,
              education: 0,
              explanation: "",
            };
          }

          return {
            filename: file.name,
            score: analysis.overall_score,
            skills: analysis.skills_match,
            experience: analysis.experience_match,
            education: analysis.education_match,
            explanation: analysis.short_explanation,
          };
        } catch (e) {
          return {
            filename: file.name,
            error: "Error analyzing this CV",
            score: 0,
            skills: 0,
            experience: 0,
            education: 0,
            explanation: "",
          };
        }
      })
    );

    const candidates = results.filter((r) => !r.error);
    const errors = results.filter((r) => r.error);

    return new Response(
      JSON.stringify({ candidates, errors }),
      {
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: "Internal server error" }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      }
    );
  }
});