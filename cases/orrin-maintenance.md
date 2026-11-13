# Orrin Manufacturing: predicting machine failures

## Prompt (read aloud)

Orrin Manufacturing makes industrial pumps. They want to use AI to
predict machine failures on their production line. They have three
years of sensor data and no failure labels. What do you propose?

## Facts to reveal only when asked

- **Scale.** 40 machining centers on two lines.
- **Failures.** A few dozen unplanned downtime events last year;
  each stops a line for several hours.
- **Maintenance today.** Fixed calendar schedule. Technicians log
  every repair in a maintenance system: date, machine, free text.
- **Sensors.** Vibration, temperature and spindle load every
  second. The historian keeps only hourly averages beyond 90 days.
- **Real goal.** The plant manager wants fewer missed delivery
  dates. Downtime is one cause; material shortages are another.
- **People.** The maintenance lead distrusts "black box"
  predictions and wants explanations.

## Change of facts (minute 25)

"The plant manager says budget only covers one line this year."

## Watch for

- Asks how failures are recorded and finds labels in the repair
  log.
- Notices the loss of second-level data after 90 days and
  proposes changing retention now.
- Names the base-rate problem: few positives, many false alarms.
- Questions whether downtime is the main cause of missed dates.
- Proposes explainable rules and a study before a learned model;
  alerts reviewed by the maintenance lead.
- Baseline: the calendar schedule. Metrics: unplanned downtime
  hours and false alarms per week.

## Common weak moves

- Unsupervised anomaly detection or deep learning in minute two.
- Promises a prediction accuracy without discussing rare events.
- Ignores the maintenance team.
