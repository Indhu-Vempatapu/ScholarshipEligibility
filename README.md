## 🎓 Scholarship Eligibility Expert System

## 📘 Introduction

Scholarships are financial aid awards designed to support students in pursuing their education without the burden of excessive costs. They are typically awarded based on academic achievement, financial need, or specific personal, social, or cultural characteristics.

## Common Scholarship Types:
- Merit-Based Scholarships
  
   Awarded based on academic excellence, test scores, or exceptional talents in areas like arts, sports, or research.

- Need-Based Scholarships

   Granted to students from low-income families who demonstrate financial need.

- International Student Scholarships
  
   For students applying from outside the host country, often with specific academic or standardized test requirements.

- Underrepresented Group Scholarships
  
   Aimed at supporting minorities, women in STEM, first-generation college students, or those with disabilities.

- Location-Specific Scholarships

   Available to residents of specific regions or countries.

- Subject-Specific Scholarships

   Based on the applicant’s chosen field of study (e.g., engineering, medicine, AI, etc.).

- Institution-Specific Scholarships

   Offered by specific universities, colleges, or organizations to students joining their institution.

- Funding-Based Scholarships

   Scholarships may vary based on the type of funding—full, partial, renewable, or one-time support.

## 💡 What I’ve Built

As part of my AI project challenge, I developed a Scholarship Eligibility Expert System that:

- Uses backward chaining to infer eligibility for various types of scholarships.

- Supports a wide range of scholarships: merit-based, need-based, underrepresented groups, international students, and more.

- Includes fuzzy scoring logic to calculate a confidence percentage.

- Is presented through an interactive Gradio web UI.

- Dynamically reveals questions based on selected scholarship types.

- Checks all necessary eligibility conditions and provides clear feedback.

## 🚀 How It Works
### 🎯 Step-by-step Functionality
- Select Scholarship Types:
  
  The user selects from multiple scholarship categories like:

  - Merit-based (Academic, Artistic, Athletic, Research)

  - Need-based

  - International

  - Underrepresented (Minorities, Disability, Women in STEM, First-gen)

  - Location/Subject/Institution-specific

  - Funding preference

- Answer Dynamic Questions:
 
   Based on the selected types, relevant fields appear (like GPA, income, research status, etc.). Tooltips or labels guide the user for each input.

- Run Evaluation:
  
  Upon clicking “Evaluate”, the Expert System:

   - Processes facts using Experta (backward chaining).

   - Applies rules to determine eligibility.

   - Calculates a confidence score (out of 100%).

- Result Displayed:
  The final output shows:

   - Eligible scholarship types.

   - If ineligible, with a 0% score.

   - A confidence percentage, showing how strong the eligibility is.

## 🧠 Technologies & Tools Used

- Python - Core programming language
- Experta	- Rule engine for backward chaining
- Gradio - Web UI framework
- Fuzzy Logic	- Confidence score calculation




