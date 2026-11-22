# CLINIQ - AI Decision Journal

## 1. Project Goal

CLINIQ was developed to help organise student clinic visits
according to administrative urgency. The AI supports queue
organisation and does not replace the clinic nurse.

## 2. Choice of AI Models

Decision:
Use Google Gemini as the AI service.

Implementation:
- Primary model: gemini-3.8-flash
- Backup model: gemini-3.5-flash-lite

Reason:
The application needs to process short student complaints
and return structured classifications. A backup model helps
handle primary-model failures.

## 3. Prompt Engineering

Decision:
Use a structured five-role prompt framework.

The prompt contains:
- AUTHORITY: Defines the AI's limited administrative role.
- EXEMPLAR: Provides examples of expected classifications.
- CONSTRAINT: Defines safety and output restrictions.
- RUBRIC: Explains categories and urgency levels.
- METADATA: Defines the required JSON output format.

Reason:
A structured prompt makes the task clearer and helps
produce consistent, predictable responses.

## 4. Output Validation

Decision:
Require exactly three JSON fields:
category, priority and summary.

The summary must contain no more than 12 words.

Reason:
Structured output makes it easier for the backend to
validate AI responses and display them in the dashboard.

## 5. Urgency Classification

Decision:
Use three administrative priority levels:

- see_now
- today
- routine

Warning signs such as chest pain, difficulty breathing,
fainting and heavy bleeding must receive immediate
nurse-review priority.

Reason:
Potentially urgent complaints should not be placed behind
routine administrative requests.

## 6. Handling Untrusted Student Notes

Decision:
Treat student-provided notes as data, not instructions.

Reason:
A student note must not be allowed to change the AI's
safety rules or override the classification instructions.

## 7. Error Handling and Fallback

Decision:
Retry an invalid AI response once and use a backup model
when the primary model fails.

If AI processing remains unsuccessful, use a conservative
fallback and retain the visit for nurse review.

Reason:
API failures must not cause a student visit to disappear
from the queue.

## 8. Human Oversight

Decision:
Keep the qualified nurse responsible for all medical
decisions.

The AI must never diagnose, prescribe treatment or remove
a student from the queue.

Reason:
The system is an administrative support tool, not a
medical decision-maker.

## 9. Monitoring and Evaluation

Decision:
Record API attempts, model names, latency, success or
failure, token usage and estimated cost.

Use normal test cases and red-team test cases to evaluate
the classification workflow.

Reason:
Monitoring helps identify failures, delays and areas
that require improvement.

## 10. Future Improvements

Possible improvements include:
- Improve reliability during API outages.
- Expand Tamil and Tanglish test coverage.
- Improve response speed.
- Add more adversarial test cases.
- Improve monitoring and reporting.
- Evaluate performance with carefully controlled,
  privacy-protected test data.

## Final Reflection

The main design principle of CLINIQ is that AI can assist
with organising clinic visits, but human professionals
must remain responsible for medical decisions.
