Automation Challenge: Website Design Scoring & Reporting Tool
Description: Develop an automated system that by entering a URL, generate a comprehensive design assessment with scoring, visual documentation, and exportable reports that demonstrate design expertise and identify improvement opportunities.
Task:
1.    Use a website URL as the input 
2.    Automated Homepage Screenshot Capture and Cloud Storage 
       o    Upon valid input, capture a high-quality screenshot of the homepage.
       o    Save/upload the screenshot to a cloud service (e.g., Google Drive, Dropbox, S3). 
3.    Design Evaluation Engine 
       o    Analyze the captured homepage for key design principles:  
               Typography (legibility, font size/contrast/hierarchy)
               Color (harmony, accessibility)
               Modern Layout (structure, whitespace)
      o    The evaluation logic can rely on rule-based checks, computer vision, or any LLM or AI models
4.    Scoring Algorithm (0–100) with Weighted Criteria 
      o    Each design principle is weighted (e.g., Usability 30%, Mobile Responsiveness 20%...) and contributes to the final score.
      o    The scoring approach can combine rule-based, statistical, or even LLM-powered analysis for richer explanations. Expect a configuration file or constants for weights.
5.    Report Generation: Explanation & Recommendations 
       o    Create a PDF or shareable web report showing: 
                 The screenshot.
                 The overall score and category breakdowns.
                 A brief explanation of each area’s score.
                 Actionable, itemized improvement tips for low scores.
6.    Google Sheets Integration 
       o    Automatically log each evaluated site’s: 
                 URL, timestamp, score, and summary findings (bonus for adding screenshot thumbnails/links).
7. Share results
       o    The final deliverable must be a PDF document that includes either: (i) a URL linking to a recorded demonstration video showcasing the functionality and execution of the tool, or (ii) a direct URL to access               and run the automation.