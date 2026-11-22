# CLINIQ - API Cost and Latency Report

## 1. Purpose

CLINIQ uses the Google Gemini API to classify student clinic
complaints for administrative queue organisation.

This report records API usage, request latency, token consumption
and estimated API cost.

## 2. Recorded Performance

Measurement date: 22 November 2026

| Metric | Recorded Result |
|---|---:|
| Total API attempts | 30 |
| Successful requests | 11 |
| Failed requests | 19 |
| Overall average latency | 18.487 seconds |
| Successful average latency | 25.123 seconds |
| Successful median latency | 1.023 seconds |
| Failed average latency | 14.646 seconds |
| Failed median latency | 3.592 seconds |
| Input tokens | 5,911 |
| Output tokens | 349 |
| Estimated paid-tier cost | $0.005742 |

These measurements represent the recorded log for one date,
not a long-term performance benchmark.

## 3. Models Used

Primary model: gemini-3.8-flash

Backup model: gemini-3.5-flash-lite

The application attempts the primary model and uses the backup
model when the primary model fails. If both models fail, the
application uses its conservative fallback classification.

The recorded results show that the backup model successfully
handled requests when primary-model attempts failed.

## 4. API Calls Per Day

The recorded usage contains 30 API attempts on 22 November 2026.

This includes successful and failed attempts. A failed attempt
may be followed by a retry or a backup-model request.

The actual number of API calls depends on the number of student
visits, retries and model availability.

## 5. Cost Estimation

The application records token usage and calculates an estimated
paid-tier equivalent using the following configured assumptions:

Input token rate: USD 0.75 per million tokens
Output token rate: USD 3.75 per million tokens

Calculation:

Estimated cost =
(Input tokens x input rate + Output tokens x output rate)
divided by 1,000,000.

Recorded estimated cost for the 30 attempts:
USD 0.005742.

This is an estimated paid-tier equivalent based on the
application's configured rates. It is not an actual invoice.
Actual provider prices and free-tier eligibility may differ.

## 6. Daily Cost Estimation

A daily forecast can be calculated using:

Estimated daily cost =
Average estimated cost per successful request
x Expected successful requests per day.

The actual daily cost depends on token usage, model selection,
retries, provider pricing and free-tier limits.

The recorded amount above is for one day's logged activity,
not a prediction of future daily expenditure.

## 7. Latency Analysis

The successful-request average was 25.123 seconds, while the
median was 1.023 seconds.

This difference indicates that a small number of unusually
slow requests increased the average.

The overall average of 18.487 seconds includes failed attempts.
The backup model also recorded successful responses.

## 8. Monitoring and Limitations

CLINIQ stores API request timestamps, model names, latency,
success or failure status, token counts and estimated cost.

The Clinic Reports dashboard displays API performance and
cost information.

Measurements depend on available provider usage metadata.
They do not represent a clinical safety or accuracy assessment.

## 9. Conclusion

API monitoring helps identify model failures, slow requests
and estimated usage costs. The backup model and conservative
fallback help the application continue handling visits when
API requests fail.

All classifications remain administrative support only.
A qualified nurse must review every visit and make all
medical decisions.
