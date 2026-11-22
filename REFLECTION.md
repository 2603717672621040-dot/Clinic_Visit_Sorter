# CLINIQ - Project Reflection

Developing CLINIQ was a valuable learning experience because it helped me understand how artificial intelligence can be used to solve a practical problem. The main aim of my project was to develop a smart clinic management application that helps organise student visits according to their urgency. Instead of allowing routine requests to occupy the entire queue, the system helps the clinic staff identify visits that may require earlier attention.

During development, I learned how to connect Python, Streamlit and the Google Gemini API. I divided the application into separate backend modules to make the code easier to understand and maintain. I also created a dashboard to display visit information, priority summaries, appointments and API performance.

One important part of this project was prompt engineering. I designed a structured prompt using five sections: AUTHORITY, EXEMPLAR, CONSTRAINT, RUBRIC and METADATA. These sections define the AI's role, provide examples, explain restrictions, describe classification rules and specify the required JSON format. I learned that clear instructions and examples are important when asking an AI model to produce structured results.

I faced several challenges during development. These included Python indentation errors, dependency installation problems, API failures and GitHub setup issues. I solved them step by step by checking error messages, testing individual modules and correcting the code. I also learned the importance of using a backup AI model and a fallback process when API requests fail.

Testing was another important learning experience. I used normal test cases and red-team test cases to check how the system handled different student complaints and potentially unsafe inputs. I also added validation to check the AI response format. API monitoring helped me understand request latency, token usage, successful requests, failed requests and estimated costs.

Safety was a major consideration throughout the project. CLINIQ is only an administrative queue-support tool. It does not diagnose illnesses, prescribe medicines, recommend treatments or remove students from the queue. A qualified nurse must review every visit and make all medical decisions. Student notes are treated as untrusted data so that instructions inside them cannot override the system's safety rules.

Through this project, I improved my Python programming, debugging, API integration, prompt engineering, testing and GitHub skills. In the future, I would like to improve response speed, expand Tamil and Tanglish testing, strengthen error handling and improve the reporting dashboard.

Overall, CLINIQ taught me that building an AI application is not only about getting an AI response. It also requires careful design, testing, monitoring, safety restrictions and human supervision.
