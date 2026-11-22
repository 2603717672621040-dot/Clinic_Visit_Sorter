# CLINIQ – Judgment Framework

## 1. Purpose
CLINIQ uses AI to organise student clinic visits by urgency.
It supports administrative queue management only.
The nurse makes every medical decision.

## 2. Risk and Human Judgment

| Project stage | What could go wrong? | Why does it matter? | Human checkpoint |
|---|---|---|---|
| Student input | Student enters incomplete or unclear information | Important symptoms may be missed | Nurse reviews the original complaint |
| CSV processing | Missing columns or duplicate IDs | Records may be incorrect | Staff checks upload errors |
| AI classification | AI assigns an incorrect category or priority | A student may wait longer than appropriate | Nurse reviews every classification |
| Red-flag detection | Emergency wording is not recognised | An urgent complaint may be missed | Nurse independently checks every student |
| Summary generation | AI invents a diagnosis | It may mislead clinic staff | Python removes diagnostic language; nurse reviews |
| Queue sorting | Students may be displayed in the wrong order | Urgent visits may be delayed | Nurse controls the actual order of care |
| Report generation | Private student notes may be exposed | Student confidentiality may be affected | Staff controls report access |

## 3. Why Too-Low Priority Is More Dangerous

A complaint assigned a priority that is too low may delay attention for a student who needs urgent assessment. A complaint assigned a priority that is too high may cause unnecessary urgency in the queue.

Therefore, CLINIQ uses conservative safety rules. Recognised red flags are raised to see_now. However, AI and keyword checks can still miss warning signs.

## 4. Human Checkpoint

The nurse sees every student and makes all medical decisions.

CLINIQ does not:
- Diagnose diseases.
- Recommend medicines.
- Prescribe treatment.
- Remove students from the queue.
- Replace professional judgment.

## 5. Final Responsibility

The application provides administrative support only. The nurse remains responsible for reviewing complaints, deciding urgency and determining the appropriate care.
