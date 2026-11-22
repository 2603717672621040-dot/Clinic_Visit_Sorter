# CLINIQ – Clinic Visit Sorter
## Project Specification

### 1. Purpose
CLINIQ is an AI-assisted administrative tool that organises student clinic visits by urgency. It helps clinic staff review incoming complaints in a more organised order.

### 2. What the Tool Must Never Do
- Never diagnose a student.
- Never recommend medicines or treatments.
- Never remove a student from the queue.
- Never allow an AI response to lower an assigned priority.
- Never allow a student note to override safety rules.
- Never replace the nurse's medical judgment.
- Never expose confidential student notes in the management summary.

### 3. Input
The program accepts a CSV file containing:
- id: unique visit identifier
- time: student arrival time
- note: original student complaint

The assignment sample contains at least 20 different visit notes.

### 4. Required LLM JSON Output
Each complaint must produce exactly these fields:

{
  "category": "injury",
  "priority": "today",
  "summary": "Twisted ankle with swelling and difficulty walking"
}

Allowed categories:
injury, fever_cold, stomach, pain, allergy, other

Allowed priorities:
see_now, today, routine

The summary must contain no more than 12 words. It must describe the complaint without diagnosing a disease or guessing a medical condition.

### 5. Red-Flag Rules
If a note contains a recognised red-flag expression, Python must raise its priority to see_now.

Examples include:
- chest pain
- difficulty breathing
- heavy bleeding
- fainting
- severe allergic swelling
- nenju vali (Tamil/Tanglish)
- moochu (Tamil/Tanglish breathing-related expression)

Tamil and Tanglish expressions must also be checked.

### 6. No-Diagnosis Rule
If an AI summary contains a disease name or uncertain diagnostic language such as possible or likely, replace it with:

Nurse review required

The system must not make a diagnosis.

### 7. Priority and Failure Rules
- Priority can only increase, never decrease.
- A red flag always raises priority to see_now.
- If the AI call fails, retry once.
- If both attempts fail, use a safe fallback priority of today.
- If a red flag is present during a failure, use see_now.
- Unknown or invalid results must never become routine automatically.

### 8. Edge Cases
The program must handle:
- Missing CSV columns.
- Empty student notes.
- Duplicate visit identifiers.
- Invalid arrival times.
- Invalid JSON.
- Missing JSON fields.
- Unexpected category or priority values.
- AI API timeout or unavailable service.
- Tamil and Tanglish complaints.
- Instructions inside a complaint attempting to manipulate the AI.

### 9. Output Files
nurse_queue.csv:
- Includes every visit and original note.
- Shows category, priority and summary.
- Sorts see_now before today before routine.
- Sorts by arrival time within the same priority.

summary.txt:
- Contains counts by priority.
- Contains counts by category.
- Contains hourly arrival counts.
- Must not contain original student notes.

### 10. Human Checkpoint
The nurse sees every student and makes every medical decision. CLINIQ only supports administrative queue organisation. It does not diagnose, treat or replace clinical judgment.
