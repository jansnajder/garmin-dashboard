# Garmin API Inventory

Generated offline from `backend/tools/snapshots/`.

## wellness.py

### get_all_day_events

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
list[2] of:
  - userProfilePk: int
  - deviceId: int
  - calendarDate: str
  - startTimestampGMT: str
  - endTimestampGMT: str
    ... (+5 more keys)
```
- **Sample:**

```json
[
  {
    "userProfilePk": 88136369,
    "deviceId": 3431878681,
    "calendarDate": "2026-07-03",
    "startTimestampGMT": "2026-07-03T05:20:00.0",
    "endTimestampGMT": "2026-07-03T05:39:00.0",
    "duration": 19,
    "activityType": "walking",
    "activitySubType": null,
    "startTimestampLocal": "2026-07-03T07:20:00.0",
    "endTimestampLocal": "2026-07-03T07:39:00.0"
  },
  {
    "userProf
... (truncated)
```

### get_all_day_stress

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+9 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "maxStressLevel": 74,
  "avgStressLevel": 21,
  "stressChartValueOffset": 1,
  "stressChartYAxisOrigin": -1,
  "stressValueDescriptorsDTOList":
... (truncated)
```

### get_body_battery

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
list[7] of:
  - date: str
  - charged: int
  - drained: int
  - startTimestampGMT: str
  - endTimestampGMT: str
    ... (+7 more keys)
```
- **Sample:**

```json
[
  {
    "date": "2026-06-27",
    "charged": 69,
    "drained": 55,
    "startTimestampGMT": "2026-06-26T22:00:00.0",
    "endTimestampGMT": "2026-06-27T22:00:00.0",
    "startTimestampLocal": "2026-06-27T00:00:00.0",
    "endTimestampLocal": "2026-06-28T00:00:00.0",
    "bodyBatteryValuesArray": [
      [
        1782511200000,
        25
      ],
      [
        1782536760000,
        90

... (truncated)
```

### get_body_battery_events

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
list[1] of:
  - event: dict
    - eventType: str
    - eventStartTimeGmt: str
    - timezoneOffset: int
    - durationInMilliseconds: int
    - bodyBatteryImpact: int
      ... (+2 more keys)
  - activityName: NoneType
  - activityType: NoneType
  - activityId: NoneType
  - averageStress: float
    ... (+4 more keys)
```
- **Sample:**

```json
[
  {
    "event": {
      "eventType": "SLEEP",
      "eventStartTimeGmt": "2026-07-02T20:52:30.0",
      "timezoneOffset": 7200000,
      "durationInMilliseconds": 28380000,
      "bodyBatteryImpact": 59,
      "feedbackType": "NONE",
      "shortFeedback": "NONE"
    },
    "activityName": null,
    "activityType": null,
    "activityId": null,
    "averageStress": 11.779874,
    "stressValueDe
... (truncated)
```

### get_daily_steps

- **Status:** data
- **Args:** `{"start": "2026-06-27", "end": "2026-07-03"}`
- **Shape:**

```
list[7] of:
  - calendarDate: str
  - totalSteps: int
  - totalDistance: int
  - stepGoal: int
```
- **Sample:**

```json
[
  {
    "calendarDate": "2026-06-27",
    "totalSteps": 13846,
    "totalDistance": 11654,
    "stepGoal": 7500
  },
  {
    "calendarDate": "2026-06-28",
    "totalSteps": 22641,
    "totalDistance": 23989,
    "stepGoal": 7500
  },
  {
    "calendarDate": "2026-06-29",
    "totalSteps": 11277,
    "totalDistance": 11464,
    "stepGoal": 7500
  },
  {
    "calendarDate": "2026-06-30",
    "tota
... (truncated)
```

### get_floors

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
- endTimestampLocal: str
- floorsValueDescriptorDTOList: list
  list[4] of:
    - index: int
    - key: str
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "floorsValueDescriptorDTOList": [
    {
      "index": 0,
      "key": "startTimeGMT"
    },
    {
      "index": 1,
      "key": "endTimeGMT"
    },
    {
      "index": 2,
      "key": "floorsAscended"

... (truncated)
```

### get_heart_rates

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+7 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "maxHeartRate": 96,
  "minHeartRate": 39,
  "restingHeartRate": 43,
  "lastSevenDaysAvgRestingHeartRate": 46,
  "heartRateValueDescriptors": [

... (truncated)
```

### get_hydration_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userId: int
- calendarDate: str
- valueInML: NoneType
- goalInML: float
- dailyAverageinML: NoneType
  ... (+3 more keys)
```
- **Sample:**

```json
{
  "userId": 88136369,
  "calendarDate": "2026-07-03",
  "valueInML": null,
  "goalInML": 2500.0,
  "dailyAverageinML": null,
  "lastEntryTimestampLocal": null,
  "sweatLossInML": null,
  "activityIntakeInML": null
}
```

### get_intensity_minutes_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+12 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "weeklyModerate": 26,
  "weeklyVigorous": 90,
  "weeklyTotal": 206,
  "weekGoal": 150,
  "dayOfGoalMet": "Tue",
  "startDayMinutes": 206,
  "en
... (truncated)
```

### get_lifestyle_logging_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- dailyLogsReport: list
  list[5] of:
    - behaviourId: int
    - measurementType: str
    - calendarDate: str
    - name: str
    - category: str
      ... (+2 more keys)
- completionStats: list
  list[7] of:
    - calendarDate: str
    - totalTracking: int
    - completedTracking: int
```
- **Sample:**

```json
{
  "dailyLogsReport": [
    {
      "behaviourId": 1,
      "measurementType": "QUANTITY",
      "calendarDate": "2026-07-03",
      "name": "Alcohol",
      "category": "LIFESTYLE",
      "details": [
        {
          "subTypeId": 1,
          "subTypeName": "BEER"
        },
        {
          "subTypeId": 2,
          "subTypeName": "WINE"
        },
        {
          "subTypeId": 3,

... (truncated)
```

### get_respiration_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+19 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "sleepStartTimestampGMT": "2026-07-02T20:52:30.0",
  "sleepEndTimestampGMT": "2026-07-03T04:45:30.0",
  "sleepStartTimestampLocal": "2026-07-02
... (truncated)
```

### get_rhr_day

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfileId: int
- statisticsStartDate: str
- statisticsEndDate: str
- allMetrics: dict
  - metricsMap: dict
    - WELLNESS_RESTING_HEART_RATE: list
      ...
- groupedMetrics: NoneType
```
- **Sample:**

```json
{
  "userProfileId": 88136369,
  "statisticsStartDate": "2026-07-03",
  "statisticsEndDate": "2026-07-03",
  "allMetrics": {
    "metricsMap": {
      "WELLNESS_RESTING_HEART_RATE": [
        {
          "value": 43.0,
          "calendarDate": "2026-07-03"
        }
      ]
    }
  },
  "groupedMetrics": null
}
```

### get_spo2_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+21 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "sleepStartTimestampGMT": "2026-07-02T20:52:30.0",
  "sleepEndTimestampGMT": "2026-07-03T04:45:30.0",
  "sleepStartTimestampLocal": "2026-07-02
... (truncated)
```

### get_stats

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfileId: int
- totalKilocalories: float
- activeKilocalories: float
- bmrKilocalories: float
- wellnessKilocalories: float
  ... (+89 more keys)
```
- **Sample:**

```json
{
  "userProfileId": 88136369,
  "totalKilocalories": 2184.0,
  "activeKilocalories": 73.0,
  "bmrKilocalories": 2111.0,
  "wellnessKilocalories": 2184.0,
  "burnedKilocalories": null,
  "consumedKilocalories": null,
  "remainingKilocalories": null,
  "totalSteps": 4870,
  "netCalorieGoal": null,
  "totalDistanceMeters": 4105,
  "wellnessDistanceMeters": 4105,
  "wellnessActiveKilocalories": 73.0,
... (truncated)
```

### get_stats_and_body

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfileId: int
- totalKilocalories: float
- activeKilocalories: float
- bmrKilocalories: float
- wellnessKilocalories: float
  ... (+100 more keys)
```
- **Sample:**

```json
{
  "userProfileId": 88136369,
  "totalKilocalories": 2184.0,
  "activeKilocalories": 73.0,
  "bmrKilocalories": 2111.0,
  "wellnessKilocalories": 2184.0,
  "burnedKilocalories": null,
  "consumedKilocalories": null,
  "remainingKilocalories": null,
  "totalSteps": 4870,
  "netCalorieGoal": null,
  "totalDistanceMeters": 4105,
  "wellnessDistanceMeters": 4105,
  "wellnessActiveKilocalories": 73.0,
... (truncated)
```

### get_steps_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
list[96] of:
  - startGMT: str
  - endGMT: str
  - steps: int
  - pushes: int
  - primaryActivityLevel: str
    ... (+1 more keys)
```
- **Sample:**

```json
[
  {
    "startGMT": "2026-07-02T22:00:00.0",
    "endGMT": "2026-07-02T22:15:00.0",
    "steps": 0,
    "pushes": 0,
    "primaryActivityLevel": "sleeping",
    "activityLevelConstant": true
  },
  {
    "startGMT": "2026-07-02T22:15:00.0",
    "endGMT": "2026-07-02T22:30:00.0",
    "steps": 0,
    "pushes": 0,
    "primaryActivityLevel": "sleeping",
    "activityLevelConstant": true
  },
  {

... (truncated)
```

### get_stress_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- startTimestampGMT: str
- endTimestampGMT: str
- startTimestampLocal: str
  ... (+9 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "startTimestampGMT": "2026-07-02T22:00:00.0",
  "endTimestampGMT": "2026-07-03T22:00:00.0",
  "startTimestampLocal": "2026-07-03T00:00:00.0",
  "endTimestampLocal": "2026-07-04T00:00:00.0",
  "maxStressLevel": 74,
  "avgStressLevel": 21,
  "stressChartValueOffset": 1,
  "stressChartYAxisOrigin": -1,
  "stressValueDescriptorsDTOList":
... (truncated)
```

### get_user_summary

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfileId: int
- totalKilocalories: float
- activeKilocalories: float
- bmrKilocalories: float
- wellnessKilocalories: float
  ... (+89 more keys)
```
- **Sample:**

```json
{
  "userProfileId": 88136369,
  "totalKilocalories": 2184.0,
  "activeKilocalories": 73.0,
  "bmrKilocalories": 2111.0,
  "wellnessKilocalories": 2184.0,
  "burnedKilocalories": null,
  "consumedKilocalories": null,
  "remainingKilocalories": null,
  "totalSteps": 4870,
  "netCalorieGoal": null,
  "totalDistanceMeters": 4105,
  "wellnessDistanceMeters": 4105,
  "wellnessActiveKilocalories": 73.0,
... (truncated)
```

### get_weekly_intensity_minutes

- **Status:** data
- **Args:** `{"start": "2026-06-27", "end": "2026-07-03"}`
- **Shape:**

```
list[2] of:
  - calendarDate: str
  - weeklyGoal: int
  - moderateValue: int
  - vigorousValue: int
```
- **Sample:**

```json
[
  {
    "calendarDate": "2026-06-22",
    "weeklyGoal": 150,
    "moderateValue": 21,
    "vigorousValue": 292
  },
  {
    "calendarDate": "2026-06-29",
    "weeklyGoal": 150,
    "moderateValue": 26,
    "vigorousValue": 90
  }
]
```

### get_weekly_steps

- **Status:** data
- **Args:** `{"end": "2026-07-03"}`
- **Shape:**

```
list[52] of:
  - calendarDate: str
  - values: dict
    - totalSteps: float
    - averageSteps: float
    - wellnessDataDaysCount: int
    - averageDistance: float
    - totalDistance: float
```
- **Sample:**

```json
[
  {
    "calendarDate": "2025-07-05",
    "values": {
      "totalSteps": 94778.0,
      "averageSteps": 13539.714285714286,
      "wellnessDataDaysCount": 7,
      "averageDistance": 12534.857142857143,
      "totalDistance": 87744.0
    }
  },
  {
    "calendarDate": "2025-07-12",
    "values": {
      "totalSteps": 83055.0,
      "averageSteps": 11865.0,
      "wellnessDataDaysCount": 7,

... (truncated)
```

### get_weekly_stress

- **Status:** data
- **Args:** `{"end": "2026-07-03"}`
- **Shape:**

```
list[52] of:
  - calendarDate: str
  - value: int
```
- **Sample:**

```json
[
  {
    "calendarDate": "2025-07-05",
    "value": 30
  },
  {
    "calendarDate": "2025-07-12",
    "value": 24
  },
  {
    "calendarDate": "2025-07-19",
    "value": 31
  },
  {
    "calendarDate": "2025-07-26",
    "value": 30
  },
  {
    "calendarDate": "2025-08-02",
    "value": 32
  },
  {
    "calendarDate": "2025-08-09",
    "value": 32
  },
  {
    "calendarDate": "2025-08-16",
    "v
... (truncated)
```

## sleep.py

### get_hrv_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePk: int
- hrvSummary: dict
  - calendarDate: str
  - weeklyAvg: int
  - lastNightAvg: int
  - lastNight5MinHigh: int
  - baseline: dict
    - lowUpper: int
    - balancedLow: int
    - balancedUpper: int
    - markerValue: float
    ... (+3 more keys)
- hrvReadings: list
  list[94] of:
    - hrvValue: int
    - readingTimeGMT: str
    - readingTimeLocal: str
- startTimestampGMT: str
- endTimestampGMT: str
  ... (+6 more keys)
```
- **Sample:**

```json
{
  "userProfilePk": 88136369,
  "hrvSummary": {
    "calendarDate": "2026-07-03",
    "weeklyAvg": 65,
    "lastNightAvg": 76,
    "lastNight5MinHigh": 122,
    "baseline": {
      "lowUpper": 47,
      "balancedLow": 51,
      "balancedUpper": 69,
      "markerValue": 0.6388855
    },
    "status": "BALANCED",
    "feedbackPhrase": "HRV_BALANCED_6",
    "createTimeStamp": "2026-07-03T04:57:28.29
... (truncated)
```

### get_sleep_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- dailySleepDTO: dict
  - id: int
  - userProfilePK: int
  - calendarDate: str
  - sleepTimeSeconds: int
  - napTimeSeconds: int
    ... (+32 more keys)
- sleepMovement: list
  list[593] of:
    - startGMT: str
    - endGMT: str
    - activityLevel: float
- remSleepData: bool
- sleepLevels: list
  list[19] of:
    - startGMT: str
    - endGMT: str
    - activityLevel: float
- sleepRestlessMoments: list
  list[39] of:
    - value: int
    - startGMT: int
  ... (+14 more keys)
```
- **Sample:**

```json
{
  "dailySleepDTO": {
    "id": 1783025550000,
    "userProfilePK": 88136369,
    "calendarDate": "2026-07-03",
    "sleepTimeSeconds": 27360,
    "napTimeSeconds": 0,
    "sleepWindowConfirmed": true,
    "sleepWindowConfirmationType": "enhanced_confirmed_final",
    "sleepStartTimestampGMT": 1783025550000,
    "sleepEndTimestampGMT": 1783053930000,
    "sleepStartTimestampLocal": 1783032750000,
... (truncated)
```

## body.py

### get_blood_pressure

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- from: str
- until: str
- measurementSummaries: list
- categoryStats: NoneType
```
- **Sample:**

```json
{
  "from": "2026-06-27",
  "until": "2026-07-03",
  "measurementSummaries": [],
  "categoryStats": null
}
```

### get_body_composition

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- startDate: str
- endDate: str
- dateWeightList: list
- totalAverage: dict
  - from: int
  - until: int
  - weight: NoneType
  - bmi: NoneType
  - bodyFat: NoneType
    ... (+6 more keys)
```
- **Sample:**

```json
{
  "startDate": "2026-06-27",
  "endDate": "2026-07-03",
  "dateWeightList": [],
  "totalAverage": {
    "from": 1782518400000,
    "until": 1783123199999,
    "weight": null,
    "bmi": null,
    "bodyFat": null,
    "bodyWater": null,
    "boneMass": null,
    "muscleMass": null,
    "physiqueRating": null,
    "visceralFat": null,
    "metabolicAge": null
  }
}
```

### get_daily_weigh_ins

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- startDate: str
- endDate: str
- dateWeightList: list
- totalAverage: dict
  - from: int
  - until: int
  - weight: NoneType
  - bmi: NoneType
  - bodyFat: NoneType
    ... (+6 more keys)
```
- **Sample:**

```json
{
  "startDate": "2026-07-03",
  "endDate": "2026-07-03",
  "dateWeightList": [],
  "totalAverage": {
    "from": 1783036800000,
    "until": 1783123199999,
    "weight": null,
    "bmi": null,
    "bodyFat": null,
    "bodyWater": null,
    "boneMass": null,
    "muscleMass": null,
    "physiqueRating": null,
    "visceralFat": null,
    "metabolicAge": null
  }
}
```

### get_fitnessage_data

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- chronologicalAge: int
- fitnessAge: float
- achievableFitnessAge: float
- previousFitnessAge: float
- components: dict
  - vigorousDaysAvg: dict
    - value: float
    - stale: bool
    - numOfWeeksForIm: int
  - rhr: dict
    - value: int
    - stale: bool
  - vigorousMinutesAvg: dict
    - value: float
    - stale: bool
    - numOfWeeksForIm: int
  - bmi: dict
    - value: float
    - stale: bool
    - lastMeasurementDate: str
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "chronologicalAge": 30,
  "fitnessAge": 20.04277078386025,
  "achievableFitnessAge": 22.714230001974546,
  "previousFitnessAge": 20.04277078386025,
  "components": {
    "vigorousDaysAvg": {
      "value": 3.8,
      "stale": false,
      "numOfWeeksForIm": 6
    },
    "rhr": {
      "value": 47,
      "stale": false
    },
    "vigorousMinutesAvg": {
      "value": 221.8,
      "stale": fals
... (truncated)
```

### get_weigh_ins

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- dailyWeightSummaries: list
- totalAverage: dict
  - from: int
  - until: int
  - weight: NoneType
  - bmi: NoneType
  - bodyFat: NoneType
    ... (+6 more keys)
- previousDateWeight: dict
  - samplePk: NoneType
  - date: NoneType
  - calendarDate: NoneType
  - weight: NoneType
  - bmi: NoneType
    ... (+10 more keys)
- nextDateWeight: dict
  - samplePk: NoneType
  - date: NoneType
  - calendarDate: NoneType
  - weight: NoneType
  - bmi: NoneType
    ... (+10 more keys)
```
- **Sample:**

```json
{
  "dailyWeightSummaries": [],
  "totalAverage": {
    "from": 1782518400000,
    "until": 1783123199999,
    "weight": null,
    "bmi": null,
    "bodyFat": null,
    "bodyWater": null,
    "boneMass": null,
    "muscleMass": null,
    "physiqueRating": null,
    "visceralFat": null,
    "metabolicAge": null
  },
  "previousDateWeight": {
    "samplePk": null,
    "date": null,
    "calendarDate
... (truncated)
```

## activities.py

### get_activities

- **Status:** data
- **Shape:**

```
list[20] of:
  - activityId: int
  - activityName: str
  - startTimeLocal: str
  - startTimeGMT: str
  - activityType: dict
    - typeId: int
    - typeKey: str
    - parentTypeId: int
    - isHidden: bool
    - restricted: bool
      ... (+1 more keys)
    ... (+79 more keys)
```
- **Sample:**

```json
[
  {
    "activityId": 23457031515,
    "activityName": "Pr\u017eno Ch\u016fze",
    "startTimeLocal": "2026-07-02 18:58:04",
    "startTimeGMT": "2026-07-02 16:58:04",
    "activityType": {
      "typeId": 9,
      "typeKey": "walking",
      "parentTypeId": 17,
      "isHidden": false,
      "restricted": false,
      "trimmable": true
    },
    "eventType": {
      "typeId": 9,
      "typeKey
... (truncated)
```

### get_activities_by_date

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
list[5] of:
  - activityId: int
  - activityName: str
  - startTimeLocal: str
  - startTimeGMT: str
  - activityType: dict
    - typeId: int
    - typeKey: str
    - parentTypeId: int
    - isHidden: bool
    - restricted: bool
      ... (+1 more keys)
    ... (+79 more keys)
```
- **Sample:**

```json
[
  {
    "activityId": 23457031515,
    "activityName": "Pr\u017eno Ch\u016fze",
    "startTimeLocal": "2026-07-02 18:58:04",
    "startTimeGMT": "2026-07-02 16:58:04",
    "activityType": {
      "typeId": 9,
      "typeKey": "walking",
      "parentTypeId": 17,
      "isHidden": false,
      "restricted": false,
      "trimmable": true
    },
    "eventType": {
      "typeId": 9,
      "typeKey
... (truncated)
```

### get_activities_fordate

- **Status:** data
- **Args:** `{"fordate": "2026-07-03"}`
- **Shape:**

```
- ActivitiesForDay: dict
  - requestUrl: str
  - statusCode: int
  - headers: dict
  - errorMessage: NoneType
  - payload: list
    ... (+1 more keys)
- AllDayHR: dict
  - requestUrl: str
  - statusCode: int
  - headers: dict
  - errorMessage: NoneType
  - payload: dict
    - userProfilePK: int
    - calendarDate: str
    - startTimestampGMT: str
    - endTimestampGMT: str
    - startTimestampLocal: str
      ... (+7 more keys)
    ... (+1 more keys)
- SleepTimes: dict
  - currentDaySleepEndTimeGMT: int
  - currentDaySleepStartTimeGMT: int
  - nextDaySleepEndTimeGMT: int
  - nextDaySleepStartTimeGMT: int
```
- **Sample:**

```json
{
  "ActivitiesForDay": {
    "requestUrl": "/activitylist-service/activities/fordailysummary/e5fdb018-6b61-4cd5-9690-9e61a93f426e",
    "statusCode": 200,
    "headers": {},
    "errorMessage": null,
    "payload": [],
    "successful": true
  },
  "AllDayHR": {
    "requestUrl": "/wellness-service/wellness/dailyHeartRate",
    "statusCode": 200,
    "headers": {},
    "errorMessage": null,
    "
... (truncated)
```

### get_activity

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- activityUUID: dict
  - uuid: str
- activityName: str
- userProfileId: int
- isMultiSportParent: bool
  ... (+7 more keys)
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "activityUUID": {
    "uuid": "d8598c8d-1df7-4b2e-9129-8fcca714abd9"
  },
  "activityName": "Pr\u017eno Ch\u016fze",
  "userProfileId": 88136369,
  "isMultiSportParent": false,
  "activityTypeDTO": {
    "typeId": 9,
    "typeKey": "walking",
    "parentTypeId": 17,
    "isHidden": false,
    "restricted": false,
    "trimmable": true
  },
  "eventTypeDTO": {
    "
... (truncated)
```

### get_activity_details

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- measurementCount: int
- metricsCount: int
- totalMetricsCount: int
- metricDescriptors: list
  list[15] of:
    - metricsIndex: int
    - key: str
    - unit: dict
      ...
  ... (+5 more keys)
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "measurementCount": 15,
  "metricsCount": 1297,
  "totalMetricsCount": 1297,
  "metricDescriptors": [
    {
      "metricsIndex": 0,
      "key": "directCaloriesBurnRate",
      "unit": {
        "id": 537,
        "key": "kcal/min",
        "factor": 69.78
      }
    },
    {
      "metricsIndex": 1,
      "key": "directDoubleCadence",
      "unit": {
        "id
... (truncated)
```

### get_activity_exercise_sets

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- exerciseSets: NoneType
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "exerciseSets": null
}
```

### get_activity_gear

- **Status:** empty
- **Args:** `{"activity_id": 23457031515}`

### get_activity_hr_in_timezones

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
list[5] of:
  - zoneNumber: int
  - secsInZone: float
  - zoneLowBoundary: int
```
- **Sample:**

```json
[
  {
    "zoneNumber": 1,
    "secsInZone": 0.0,
    "zoneLowBoundary": 109
  },
  {
    "zoneNumber": 2,
    "secsInZone": 0.0,
    "zoneLowBoundary": 142
  },
  {
    "zoneNumber": 3,
    "secsInZone": 0.0,
    "zoneLowBoundary": 158
  },
  {
    "zoneNumber": 4,
    "secsInZone": 0.0,
    "zoneLowBoundary": 169
  },
  {
    "zoneNumber": 5,
    "secsInZone": 0.0,
    "zoneLowBoundary": 178
  }
... (truncated)
```

### get_activity_power_in_timezones

- **Status:** empty
- **Args:** `{"activity_id": 23457031515}`

### get_activity_split_summaries

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- activityUUID: dict
  - uuid: str
- splitSummaries: list
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "activityUUID": {
    "uuid": "d8598c8d-1df7-4b2e-9129-8fcca714abd9"
  },
  "splitSummaries": []
}
```

### get_activity_splits

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- lapDTOs: list
  list[6] of:
    - startTimeGMT: str
    - startLatitude: float
    - startLongitude: float
    - distance: float
    - duration: float
      ... (+23 more keys)
- eventDTOs: list
  list[2] of:
    - startTimeGMT: str
    - startTimeGMTDoubleValue: float
    - sectionTypeDTO: dict
      ...
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "lapDTOs": [
    {
      "startTimeGMT": "2026-07-02T16:58:04.0",
      "startLatitude": 49.61420802399516,
      "startLongitude": 18.35413877852261,
      "distance": 1000.0,
      "duration": 1007.366,
      "movingDuration": 780.0,
      "elapsedDuration": 1007.366,
      "elevationGain": 10.87,
      "elevationLoss": 6.13,
      "maxElevation": 339.6,
      "m
... (truncated)
```

### get_activity_typed_splits

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- activityId: int
- activityUUID: dict
  - uuid: str
- splits: list
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "activityUUID": {
    "uuid": "d8598c8d-1df7-4b2e-9129-8fcca714abd9"
  },
  "splits": []
}
```

### get_activity_types

- **Status:** data
- **Shape:**

```
list[153] of:
  - typeId: int
  - typeKey: str
  - parentTypeId: int
  - isHidden: bool
  - restricted: bool
    ... (+1 more keys)
```
- **Sample:**

```json
[
  {
    "typeId": 1,
    "typeKey": "running",
    "parentTypeId": 17,
    "isHidden": false,
    "restricted": false,
    "trimmable": true
  },
  {
    "typeId": 2,
    "typeKey": "cycling",
    "parentTypeId": 17,
    "isHidden": false,
    "restricted": false,
    "trimmable": true
  },
  {
    "typeId": 3,
    "typeKey": "hiking",
    "parentTypeId": 17,
    "isHidden": false,
    "restrict
... (truncated)
```

### get_activity_weather

- **Status:** data
- **Args:** `{"activity_id": 23457031515}`
- **Shape:**

```
- issueDate: str
- temp: int
- apparentTemp: int
- dewPoint: int
- relativeHumidity: int
  ... (+8 more keys)
```
- **Sample:**

```json
{
  "issueDate": "2026-07-02T18:00:00.000+00:00",
  "temp": 58,
  "apparentTemp": 58,
  "dewPoint": 48,
  "relativeHumidity": 69,
  "windDirection": 10,
  "windDirectionCompassPoint": "n",
  "windSpeed": 8,
  "windGust": null,
  "latitude": 49.549998957663774,
  "longitude": 18.45000092871487,
  "weatherStationDTO": {
    "id": "11787",
    "name": "",
    "timezone": null
  },
  "weatherTypeDTO":
... (truncated)
```

### get_last_activity

- **Status:** data
- **Shape:**

```
- activityId: int
- activityName: str
- startTimeLocal: str
- startTimeGMT: str
- activityType: dict
  - typeId: int
  - typeKey: str
  - parentTypeId: int
  - isHidden: bool
  - restricted: bool
    ... (+1 more keys)
  ... (+79 more keys)
```
- **Sample:**

```json
{
  "activityId": 23457031515,
  "activityName": "Pr\u017eno Ch\u016fze",
  "startTimeLocal": "2026-07-02 18:58:04",
  "startTimeGMT": "2026-07-02 16:58:04",
  "activityType": {
    "typeId": 9,
    "typeKey": "walking",
    "parentTypeId": 17,
    "isHidden": false,
    "restricted": false,
    "trimmable": true
  },
  "eventType": {
    "typeId": 9,
    "typeKey": "uncategorized",
    "sortOrder
... (truncated)
```

### get_progress_summary_between_dates

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
list[1] of:
  - date: str
  - countOfActivities: int
  - stats: dict
    - running: dict
      ...
    - walking: dict
      ...
```
- **Sample:**

```json
[
  {
    "date": "2026-07-04",
    "countOfActivities": 1,
    "stats": {
      "running": {
        "distance": {
          "count": 4,
          "min": 664483.984375,
          "max": 1133053.02734375,
          "avg": 950182.4951171875,
          "sum": 3800729.98046875
        }
      },
      "walking": {
        "distance": {
          "count": 1,
          "min": 500447.021484375,

... (truncated)
```

## training.py

### get_adaptive_training_plan_by_id

- **Status:** data
- **Args:** `{"plan_id": 44769178}`
- **Shape:**

```
- trainingPlanId: int
- trainingPlanCategory: str
- trainingType: dict
  - typeId: int
  - typeKey: str
- trainingSubType: dict
  - subTypeId: int
  - subTypeKey: str
- trainingLevel: dict
  - levelId: int
  - levelKey: str
  ... (+27 more keys)
```
- **Sample:**

```json
{
  "trainingPlanId": 44769178,
  "trainingPlanCategory": "FBT_ADAPTIVE",
  "trainingType": {
    "typeId": 2,
    "typeKey": "Running"
  },
  "trainingSubType": {
    "subTypeId": 26,
    "subTypeKey": "GarminRunningCoachEventBased"
  },
  "trainingLevel": {
    "levelId": 3,
    "levelKey": "Intermediate"
  },
  "trainingVersion": {
    "versionId": 4,
    "versionName": "HeartRate"
  },
  "form
... (truncated)
```

### get_cycling_ftp

- **Status:** data
- **Shape:**

```
- userProfilePK: int
- version: int
- calendarDate: str
- isStale: bool
- sequence: int
  ... (+3 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "version": 1699459902503,
  "calendarDate": "2023-11-08T17:11:42.503",
  "isStale": true,
  "sequence": 1699459902503,
  "sport": "CYCLING",
  "functionalThresholdPower": 214,
  "biometricSourceType": "CHANGE_LOG"
}
```

### get_endurance_score

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- startDate: str
- endDate: str
- avg: int
- max: int
  ... (+2 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "startDate": "2026-06-27",
  "endDate": "2026-07-03",
  "avg": 7148,
  "max": 7174,
  "groupMap": {
    "2026-06-27": {
      "groupAverage": 7148,
      "groupMax": 7174,
      "enduranceContributorDTOList": [
        {
          "activityTypeId": 9,
          "group": null,
          "contribution": 3.6
        },
        {
          "activityTypeId": null,

... (truncated)
```

### get_goals

- **Status:** empty

### get_hill_score

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- startDate: str
- endDate: str
- periodAvgScore: dict
  - 2026-06-27: int
- maxScore: int
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "startDate": "2026-06-27",
  "endDate": "2026-07-03",
  "periodAvgScore": {
    "2026-06-27": 44
  },
  "maxScore": 44,
  "hillScoreDTOList": [
    {
      "userProfilePK": 88136369,
      "deviceId": 3431878681,
      "calendarDate": "2026-07-03",
      "strengthScore": 30,
      "enduranceScore": 20,
      "hillScoreClassificationId": 2,
      "overallScore": 44,
... (truncated)
```

### get_lactate_threshold

- **Status:** data
- **Shape:**

```
- speed_and_heart_rate: dict
  - userProfilePK: int
  - version: int
  - calendarDate: str
  - sequence: int
  - speed: float
    ... (+2 more keys)
- power: dict
  - userProfilePk: int
  - calendarDate: str
  - origin: str
  - sport: str
  - functionalThresholdPower: int
    ... (+5 more keys)
```
- **Sample:**

```json
{
  "speed_and_heart_rate": {
    "userProfilePK": 88136369,
    "version": 1782674632085,
    "calendarDate": "2026-06-28T21:23:51.953",
    "sequence": 1782674632085,
    "speed": 0.39722111000000004,
    "heartRate": 175,
    "heartRateCycling": 173
  },
  "power": {
    "userProfilePk": 88136369,
    "calendarDate": "2026-06-28T21:22:54.0",
    "origin": "power",
    "sport": "RUNNING",
    "f
... (truncated)
```

### get_max_metrics

- **Status:** empty
- **Args:** `{"cdate": "2026-07-03"}`

### get_morning_training_readiness

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userProfilePK: int
- calendarDate: str
- timestamp: str
- timestampLocal: str
- deviceId: int
  ... (+24 more keys)
```
- **Sample:**

```json
{
  "userProfilePK": 88136369,
  "calendarDate": "2026-07-03",
  "timestamp": "2026-07-03T04:56:12.0",
  "timestampLocal": "2026-07-03T06:56:12.0",
  "deviceId": 3431878681,
  "level": "HIGH",
  "feedbackLong": "HIGH_RT_HIGHEST_SS_AVAILABLE",
  "feedbackShort": "WELL_RECOVERED",
  "score": 80,
  "sleepScore": 81,
  "sleepScoreFactorPercent": 72,
  "sleepScoreFactorFeedback": "GOOD",
  "recoveryTim
... (truncated)
```

### get_personal_record

- **Status:** data
- **Shape:**

```
list[14] of:
  - id: int
  - typeId: int
  - status: str
  - activityId: int
  - activityName: str
    ... (+12 more keys)
```
- **Sample:**

```json
[
  {
    "id": 2869739938,
    "typeId": 1,
    "status": "ACCEPTED",
    "activityId": 22116014780,
    "activityName": "Fr\u00fddek-M\u00edstek B\u011bh",
    "activityType": "running",
    "activityStartDateTimeInGMT": 1773070510000,
    "actStartDateTimeInGMTFormatted": "2026-03-09T15:35:10.0",
    "activityStartDateTimeLocal": 1773074110000,
    "activityStartDateTimeLocalFormatted": "2026-0
... (truncated)
```

### get_race_predictions

- **Status:** data
- **Shape:**

```
- userId: int
- fromCalendarDate: NoneType
- toCalendarDate: NoneType
- calendarDate: str
- time5K: int
  ... (+3 more keys)
```
- **Sample:**

```json
{
  "userId": 88136369,
  "fromCalendarDate": null,
  "toCalendarDate": null,
  "calendarDate": "2026-07-04",
  "time5K": 1156,
  "time10K": 2450,
  "timeHalfMarathon": 5510,
  "timeMarathon": 12280
}
```

### get_running_tolerance

- **Status:** empty
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`

### get_scheduled_workout_by_id

- **Status:** skipped
- **Reason:** parent call for 'scheduled_workout_id' has not produced a value yet (empty/missing/unprobed)

### get_scheduled_workouts

- **Status:** data
- **Args:** `{"year": 2026, "month": 7}`
- **Shape:**

```
- startDayOfMonth: int
- numOfDaysInMonth: int
- numOfDaysInPrevMonth: int
- month: int
- year: int
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "startDayOfMonth": 3,
  "numOfDaysInMonth": 31,
  "numOfDaysInPrevMonth": 30,
  "month": 6,
  "year": 2026,
  "calendarItems": [
    {
      "id": null,
      "groupId": null,
      "trainingPlanId": null,
      "itemType": "event",
      "activityTypeId": 1,
      "wellnessActivityUuid": null,
      "title": "B\u011bhej lesy 2026 - B\u00edl\u00e1 - 20 km",
      "date": "2026-08-01",
      "d
... (truncated)
```

### get_training_plan_by_id

- **Status:** error
- **Args:** `{"plan_id": 44769178}`
- **Reason:** API call client error (400): API Error 400 - Not a phased plan.

### get_training_plans

- **Status:** data
- **Shape:**

```
- trainingPlanList: list
  list[1] of:
    - trainingPlanId: int
    - trainingPlanCategory: str
    - trainingType: dict
      ...
    - trainingSubType: dict
      ...
    - trainingLevel: dict
      ...
      ... (+27 more keys)
- searchFilter: dict
  - ownerId: int
  - ownerDisplayName: NoneType
  - trainingLevels: NoneType
  - trainingStatusList: list
  - trainingTypes: NoneType
    ... (+7 more keys)
```
- **Sample:**

```json
{
  "trainingPlanList": [
    {
      "trainingPlanId": 44769178,
      "trainingPlanCategory": "FBT_ADAPTIVE",
      "trainingType": {
        "typeId": 2,
        "typeKey": "Running"
      },
      "trainingSubType": {
        "subTypeId": 26,
        "subTypeKey": "GarminRunningCoachEventBased"
      },
      "trainingLevel": {
        "levelId": 3,
        "levelKey": "Intermediate"
      },

... (truncated)
```

### get_training_readiness

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
list[2] of:
  - userProfilePK: int
  - calendarDate: str
  - timestamp: str
  - timestampLocal: str
  - deviceId: int
    ... (+24 more keys)
```
- **Sample:**

```json
[
  {
    "userProfilePK": 88136369,
    "calendarDate": "2026-07-03",
    "timestamp": "2026-07-03T04:56:12.0",
    "timestampLocal": "2026-07-03T06:56:12.0",
    "deviceId": 3431878681,
    "level": "HIGH",
    "feedbackLong": "HIGH_RT_HIGHEST_SS_AVAILABLE",
    "feedbackShort": "WELL_RECOVERED",
    "score": 80,
    "sleepScore": 81,
    "sleepScoreFactorPercent": 72,
    "sleepScoreFactorFeedb
... (truncated)
```

### get_training_status

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- userId: int
- mostRecentVO2Max: dict
  - userId: int
  - generic: dict
    - calendarDate: str
    - vo2MaxPreciseValue: float
    - vo2MaxValue: float
    - fitnessAge: NoneType
    - fitnessAgeDescription: NoneType
      ... (+1 more keys)
  - cycling: NoneType
  - heatAltitudeAcclimation: dict
    - calendarDate: str
    - altitudeAcclimationDate: str
    - previousAltitudeAcclimationDate: str
    - heatAcclimationDate: str
    - previousHeatAcclimationDate: str
      ... (+11 more keys)
- mostRecentTrainingLoadBalance: dict
  - userId: int
  - metricsTrainingLoadBalanceDTOMap: dict
    - 3431878681: dict
      ...
  - recordedDevices: list
    list[1] of:
      ...
- mostRecentTrainingStatus: dict
  - userId: int
  - latestTrainingStatusData: dict
    - 3431878681: dict
      ...
  - recordedDevices: list
    list[1] of:
      ...
  - showSelector: bool
  - lastPrimarySyncDate: str
- heatAltitudeAcclimationDTO: NoneType
```
- **Sample:**

```json
{
  "userId": 88136369,
  "mostRecentVO2Max": {
    "userId": 88136369,
    "generic": {
      "calendarDate": "2026-06-30",
      "vo2MaxPreciseValue": 57.6,
      "vo2MaxValue": 58.0,
      "fitnessAge": null,
      "fitnessAgeDescription": null,
      "maxMetCategory": 0
    },
    "cycling": null,
    "heatAltitudeAcclimation": {
      "calendarDate": "2026-07-03",
      "altitudeAcclimationDa
... (truncated)
```

### get_workout_by_id

- **Status:** data
- **Args:** `{"workout_id": 754702537}`
- **Shape:**

```
- workoutId: int
- ownerId: int
- workoutName: str
- description: NoneType
- updatedDate: str
  ... (+28 more keys)
```
- **Sample:**

```json
{
  "workoutId": 754702537,
  "ownerId": 88136369,
  "workoutName": "5x800",
  "description": null,
  "updatedDate": "2023-10-04T16:19:56.0",
  "createdDate": "2023-10-04T16:19:26.0",
  "sportType": {
    "sportTypeId": 1,
    "sportTypeKey": "running",
    "displayOrder": 1
  },
  "subSportType": null,
  "trainingPlanId": null,
  "author": {
    "userProfilePk": 88136369,
    "displayName": "e5fd
... (truncated)
```

### get_workouts

- **Status:** data
- **Shape:**

```
list[50] of:
  - workoutId: int
  - ownerId: int
  - workoutName: str
  - description: NoneType
  - updateDate: str
    ... (+19 more keys)
```
- **Sample:**

```json
[
  {
    "workoutId": 754702537,
    "ownerId": 88136369,
    "workoutName": "5x800",
    "description": null,
    "updateDate": "2023-10-04T16:19:56.0",
    "createdDate": "2023-10-04T16:19:26.0",
    "sportType": {
      "sportTypeId": 1,
      "sportTypeKey": "running",
      "displayOrder": 1
    },
    "trainingPlanId": null,
    "author": {
      "userProfilePk": null,
      "displayName":
... (truncated)
```

## devices.py

### get_device_alarms

- **Status:** empty

### get_device_last_used

- **Status:** data
- **Shape:**

```
- userDeviceId: int
- userProfileNumber: int
- applicationNumber: int
- lastUsedDeviceApplicationKey: str
- lastUsedDeviceName: str
  ... (+3 more keys)
```
- **Sample:**

```json
{
  "userDeviceId": 3431878681,
  "userProfileNumber": 88136369,
  "applicationNumber": 36907,
  "lastUsedDeviceApplicationKey": "fenix7SapphireSolar",
  "lastUsedDeviceName": "fenix 7 Sapphire Solar",
  "lastUsedDeviceUploadTime": 1783182290000,
  "imageUrl": "https://static.garmincdn.com/en/products/010-02540-35/v/cf-sm-2x3-1606b295-d2f3-401d-a867-98c0034c8841.png",
  "released": true
}
```

### get_device_settings

- **Status:** data
- **Args:** `{"device_id": 3431878681}`
- **Shape:**

```
- deviceId: int
- timeFormat: str
- dateFormat: str
- measurementUnits: str
- allUnits: str
  ... (+130 more keys)
```
- **Sample:**

```json
{
  "deviceId": 3431878681,
  "timeFormat": "time_twenty_four_hr",
  "dateFormat": "date_day_month",
  "measurementUnits": "metric",
  "allUnits": "metric",
  "visibleScreens": null,
  "enabledScreens": {},
  "screenLists": null,
  "isVivohubEnabled": null,
  "alarms": [],
  "supportedAlarmModes": null,
  "multipleAlarmEnabled": true,
  "maxAlarm": null,
  "activityTracking": null,
  "keyTonesEnab
... (truncated)
```

### get_device_solar_data

- **Status:** data
- **Args:** `{"device_id": 3431878681, "startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- solarDailyDataDTOs: list
  list[7] of:
    - localConnectDate: str
    - userProfilePk: int
    - deviceId: int
    - solarInputReadings: list
      ...
    - totalActivityTimeGainedMs: int
```
- **Sample:**

```json
{
  "solarDailyDataDTOs": [
    {
      "localConnectDate": "2026-06-27",
      "userProfilePk": 88136369,
      "deviceId": 3431878681,
      "solarInputReadings": [
        {
          "readingTimestampLocal": "2026-06-27T00:01:00.0",
          "readingTimestampGmt": "2026-06-26T22:01:00.0",
          "solarUtilization": 0.0,
          "notChargingTooHot": false,
          "notChargingTooCold":
... (truncated)
```

### get_devices

- **Status:** data
- **Shape:**

```
list[2] of:
  - appSupport: bool
  - applicationKey: str
  - deviceTypePk: int
  - bestInClassVideoLink: NoneType
  - bluetoothClassicDevice: bool
    ... (+302 more keys)
```
- **Sample:**

```json
[
  {
    "appSupport": true,
    "applicationKey": "fenix7SapphireSolar",
    "deviceTypePk": 36907,
    "bestInClassVideoLink": null,
    "bluetoothClassicDevice": false,
    "bluetoothLowEnergyDevice": true,
    "deviceCategories": [
      "FITNESS",
      "WELLNESS",
      "GOLF",
      "OUTDOOR"
    ],
    "deviceEmbedVideoLink": null,
    "deviceSettingsFile": "RealTimeDeviceSettingsSolar_d9
... (truncated)
```

### get_primary_training_device

- **Status:** data
- **Shape:**

```
- PrimaryTrainingDevice: dict
  - deviceId: int
- WearableDevices: dict
  - deviceWeights: list
    list[1] of:
      ...
  - wearableDeviceCount: int
- TrainingStatusOnlyDevices: dict
  - deviceWeights: list
- PrimaryTrainingDevices: dict
  - deviceWeights: list
    list[1] of:
      ...
  - primaryTrainingDeviceCount: int
- RegisteredDevices: list
  list[2] of:
    - appSupport: bool
    - applicationKey: str
    - deviceTypePk: int
    - bestInClassVideoLink: NoneType
    - bluetoothClassicDevice: bool
      ... (+302 more keys)
```
- **Sample:**

```json
{
  "PrimaryTrainingDevice": {
    "deviceId": 3431878681
  },
  "WearableDevices": {
    "deviceWeights": [
      {
        "displayName": "fenix 7 Sapphire Solar",
        "deviceId": 3431878681,
        "imageUrl": "https://static.garmincdn.com/en/products/010-02540-35/v/cf-sm-2x3-1606b295-d2f3-401d-a867-98c0034c8841.png",
        "weight": 3,
        "primaryTrainingCapable": true,
        "lh
... (truncated)
```

### get_unit_system

- **Status:** data
- **Shape:**

```
str = 'metric'
```
- **Sample:**

```json
"metric"
```

## gear.py

### get_gear

- **Status:** data
- **Args:** `{"userProfileNumber": 88136369}`
- **Shape:**

```
list[10] of:
  - gearPk: int
  - uuid: str
  - userProfilePk: int
  - gearMakeName: str
  - gearModelName: str
    ... (+13 more keys)
```
- **Sample:**

```json
[
  {
    "gearPk": 26505217,
    "uuid": "2a83bc36fc894b549b9f7b573fc6e2d2",
    "userProfilePk": 88136369,
    "gearMakeName": "Other",
    "gearModelName": "Unknown Bike",
    "gearTypeName": "Bike",
    "gearStatusName": "active",
    "displayName": "",
    "customMakeModel": "Tana 29",
    "imageNameLarge": null,
    "imageNameMedium": null,
    "imageNameSmall": null,
    "dateBegin": "2021-
... (truncated)
```

### get_gear_activities

- **Status:** data
- **Args:** `{"gearUUID": "2a83bc36fc894b549b9f7b573fc6e2d2"}`
- **Shape:**

```
list[85] of:
  - activityId: int
  - activityName: str
  - startTimeLocal: str
  - startTimeGMT: str
  - activityType: dict
    - typeId: int
    - typeKey: str
    - parentTypeId: int
    - isHidden: bool
    - restricted: bool
      ... (+1 more keys)
    ... (+76 more keys)
```
- **Sample:**

```json
[
  {
    "activityId": 19094034777,
    "activityName": "Brno Cyklistika",
    "startTimeLocal": "2025-05-11 16:07:01",
    "startTimeGMT": "2025-05-11 14:07:01",
    "activityType": {
      "typeId": 2,
      "typeKey": "cycling",
      "parentTypeId": 17,
      "isHidden": false,
      "restricted": false,
      "trimmable": true
    },
    "eventType": {
      "typeId": 9,
      "typeKey": "un
... (truncated)
```

### get_gear_defaults

- **Status:** data
- **Args:** `{"userProfileNumber": 88136369}`
- **Shape:**

```
list[2] of:
  - uuid: str
  - activityTypePk: int
  - defaultGear: bool
```
- **Sample:**

```json
[
  {
    "uuid": "ff5ba50c6afc41078be5100d4650774b",
    "activityTypePk": 1,
    "defaultGear": true
  },
  {
    "uuid": "988d337f728341078475932044fd3591",
    "activityTypePk": 2,
    "defaultGear": true
  }
]
```

### get_gear_stats

- **Status:** data
- **Args:** `{"gearUUID": "2a83bc36fc894b549b9f7b573fc6e2d2"}`
- **Shape:**

```
- gearPk: int
- uuid: str
- createDate: int
- updateDate: int
- totalDistance: float
  ... (+3 more keys)
```
- **Sample:**

```json
{
  "gearPk": 26505217,
  "uuid": "2a83bc36fc894b549b9f7b573fc6e2d2",
  "createDate": 1622891024000,
  "updateDate": 1778093174000,
  "totalDistance": 2319148.6177282557,
  "totalActivities": 85,
  "isProcessing": false,
  "processing": false
}
```

## profile.py

### get_full_name

- **Status:** data
- **Shape:**

```
str = 'Jan Šnajder'
```
- **Sample:**

```json
"Jan \u0160najder"
```

### get_user_profile

- **Status:** data
- **Shape:**

```
- id: int
- userData: dict
  - gender: str
  - weight: float
  - height: float
  - timeFormat: str
  - birthDate: str
    ... (+36 more keys)
- userSleep: dict
  - sleepTime: int
  - defaultSleepTime: bool
  - wakeTime: int
  - defaultWakeTime: bool
- connectDate: NoneType
- sourceType: NoneType
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "id": 88136369,
  "userData": {
    "gender": "MALE",
    "weight": 72500.0,
    "height": 185.0,
    "timeFormat": "time_twenty_four_hr",
    "birthDate": "1995-08-02",
    "measurementSystem": "metric",
    "activityLevel": null,
    "handedness": "RIGHT",
    "powerFormat": {
      "formatId": 30,
      "formatKey": "watt",
      "minFraction": 0,
      "maxFraction": 0,
      "groupingUsed
... (truncated)
```

### get_userprofile_settings

- **Status:** data
- **Shape:**

```
- displayName: str
- preferredLocale: str
- measurementSystem: str
- firstDayOfWeek: dict
  - dayId: int
  - dayName: str
  - sortOrder: int
  - isPossibleFirstDay: bool
- numberFormat: str
  ... (+12 more keys)
```
- **Sample:**

```json
{
  "displayName": "e5fdb018-6b61-4cd5-9690-9e61a93f426e",
  "preferredLocale": "cs",
  "measurementSystem": "metric",
  "firstDayOfWeek": {
    "dayId": 3,
    "dayName": "monday",
    "sortOrder": 3,
    "isPossibleFirstDay": true
  },
  "numberFormat": "decimal_period",
  "timeFormat": {
    "formatId": 33,
    "formatKey": "time_twenty_four_hr",
    "minFraction": 0,
    "maxFraction": 0,

... (truncated)
```

## badges.py

### get_adhoc_challenges

- **Status:** data
- **Args:** `{"start": 1, "limit": 10}`
- **Shape:**

```
list[8] of:
  - socialChallengeStatusId: int
  - socialChallengeActivityTypeId: int
  - adHocChallengeName: str
  - adHocChallengeDesc: str
  - ownerUserProfileId: int
    ... (+12 more keys)
```
- **Sample:**

```json
[
  {
    "socialChallengeStatusId": 4,
    "socialChallengeActivityTypeId": 4,
    "adHocChallengeName": "Krokov\u00e1 v\u00fdzva",
    "adHocChallengeDesc": "Krokov\u00e1 v\u00fdzva",
    "ownerUserProfileId": 92602350,
    "uuid": "41277183B396447DBBAF2C35DB2183D6",
    "startDate": "2024-08-11T00:00:00.0",
    "endDate": "2024-08-17T23:59:59.0",
    "durationTypeId": 0,
    "userRanking": 1,

... (truncated)
```

### get_available_badge_challenges

- **Status:** data
- **Args:** `{"start": 1, "limit": 10}`
- **Shape:**

```
list[4] of:
  - uuid: str
  - badgeChallengeName: str
  - challengeCategoryId: int
  - badgeChallengeStatusId: int
  - startDate: str
    ... (+28 more keys)
```
- **Sample:**

```json
[
  {
    "uuid": "063388AB4F2C4FDDA840E39283BAFA6D",
    "badgeChallengeName": "July Swim Week",
    "challengeCategoryId": 3,
    "badgeChallengeStatusId": 1,
    "startDate": "2026-07-19T00:00:00.0",
    "endDate": "2026-07-25T23:59:59.0",
    "createDate": "2026-06-23T15:25:16.247",
    "updateDate": "2026-06-23T15:25:16.247",
    "badgeId": 3136,
    "badgeKey": "challenge_total_swim_1km_2026
... (truncated)
```

### get_available_badges

- **Status:** data
- **Shape:**

```
list[215] of:
  - badgeId: int
  - badgeKey: str
  - badgeName: str
  - badgeUuid: NoneType
  - badgeCategoryId: int
    ... (+29 more keys)
```
- **Sample:**

```json
[
  {
    "badgeId": 1046,
    "badgeKey": "activity_first_avenger_0704",
    "badgeName": "No, You Move",
    "badgeUuid": null,
    "badgeCategoryId": 1,
    "badgeDifficultyId": 1,
    "badgePoints": 1,
    "badgeTypeIds": [
      3,
      5
    ],
    "badgeSeriesId": 38,
    "badgeStartDate": "2019-07-04T00:00:00.0",
    "badgeEndDate": "2026-07-04T23:59:59.0",
    "userProfileId": null,

... (truncated)
```

### get_badge_challenges

- **Status:** data
- **Args:** `{"start": 1, "limit": 10}`
- **Shape:**

```
list[10] of:
  - uuid: str
  - badgeChallengeName: str
  - challengeCategoryId: int
  - badgeChallengeStatusId: int
  - startDate: str
    ... (+28 more keys)
```
- **Sample:**

```json
[
  {
    "uuid": "FFC37B12D8CE44E1B04BADE4556A9A3B",
    "badgeChallengeName": "August Step Month",
    "challengeCategoryId": 4,
    "badgeChallengeStatusId": 4,
    "startDate": "2020-08-01T00:00:00.0",
    "endDate": "2020-08-31T23:59:59.0",
    "createDate": "2020-07-31T18:24:32.557",
    "updateDate": "2020-07-31T18:25:56.647",
    "badgeId": 1199,
    "badgeKey": "challenge_total_steps_300k
... (truncated)
```

### get_earned_badges

- **Status:** data
- **Shape:**

```
list[395] of:
  - badgeId: int
  - badgeKey: str
  - badgeName: str
  - badgeUuid: str
  - badgeCategoryId: int
    ... (+29 more keys)
```
- **Sample:**

```json
[
  {
    "badgeId": 1822,
    "badgeKey": "sleep_30_days",
    "badgeName": "Sleep Savant",
    "badgeUuid": "E01402D037084967955D4A008FA98CB8",
    "badgeCategoryId": 7,
    "badgeDifficultyId": 1,
    "badgePoints": 1,
    "badgeTypeIds": [
      3,
      4
    ],
    "badgeSeriesId": null,
    "badgeStartDate": "2023-09-01T00:00:00.0",
    "badgeEndDate": null,
    "userProfileId": 88136369,

... (truncated)
```

### get_in_progress_badges

- **Status:** data
- **Shape:**

```
list[20] of:
  - badgeId: int
  - badgeKey: str
  - badgeName: str
  - badgeUuid: str
  - badgeCategoryId: int
    ... (+29 more keys)
```
- **Sample:**

```json
[
  {
    "badgeId": 1822,
    "badgeKey": "sleep_30_days",
    "badgeName": "Sleep Savant",
    "badgeUuid": "E01402D037084967955D4A008FA98CB8",
    "badgeCategoryId": 7,
    "badgeDifficultyId": 1,
    "badgePoints": 1,
    "badgeTypeIds": [
      3,
      4
    ],
    "badgeSeriesId": null,
    "badgeStartDate": "2023-09-01T00:00:00.0",
    "badgeEndDate": null,
    "userProfileId": 88136369,

... (truncated)
```

### get_inprogress_virtual_challenges

- **Status:** empty
- **Args:** `{"start": 1, "limit": 10}`

### get_non_completed_badge_challenges

- **Status:** data
- **Args:** `{"start": 1, "limit": 10}`
- **Shape:**

```
list[10] of:
  - uuid: str
  - badgeChallengeName: str
  - challengeCategoryId: int
  - badgeChallengeStatusId: int
  - startDate: str
    ... (+28 more keys)
```
- **Sample:**

```json
[
  {
    "uuid": "5C662F5387B8407481B2CC617348030A",
    "badgeChallengeName": "July Weekend 5K",
    "challengeCategoryId": 1,
    "badgeChallengeStatusId": 2,
    "startDate": "2026-07-03T00:00:00.0",
    "endDate": "2026-07-05T23:59:59.0",
    "createDate": "2026-06-23T15:25:16.237",
    "updateDate": "2026-06-23T15:25:16.237",
    "badgeId": 3135,
    "badgeKey": "challenge_run_5k_2026_07",

... (truncated)
```

## nutrition.py

### get_nutrition_daily_food_log

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- mealDate: str
- dayStartTime: str
- dayEndTime: str
- dailyViewType: str
- mealDetails: list
  ... (+1 more keys)
```
- **Sample:**

```json
{
  "mealDate": "2026-07-03",
  "dayStartTime": "07:00:00",
  "dayEndTime": "22:00:00",
  "dailyViewType": "TIMELINE_VIEW",
  "mealDetails": [],
  "loggedFoodsWithServingSizes": []
}
```

### get_nutrition_daily_meals

- **Status:** data
- **Args:** `{"cdate": "2026-07-03"}`
- **Shape:**

```
- meals: list
- dailyViewType: str
```
- **Sample:**

```json
{
  "meals": [],
  "dailyViewType": "TIMELINE_VIEW"
}
```

### get_nutrition_daily_settings

- **Status:** empty
- **Args:** `{"cdate": "2026-07-03"}`

## golf.py

### get_golf_scorecard

- **Status:** skipped
- **Reason:** parent call for 'scorecard_id' has not produced a value yet (empty/missing/unprobed)

### get_golf_shot_data

- **Status:** skipped
- **Reason:** parent call for 'scorecard_id' has not produced a value yet (empty/missing/unprobed)

### get_golf_summary

- **Status:** data
- **Shape:**

```
- pageNumber: int
- rowsPerPage: int
- totalRows: int
```
- **Sample:**

```json
{
  "pageNumber": 1,
  "rowsPerPage": 100,
  "totalRows": 0
}
```

## womens_health.py

### get_menstrual_calendar_data

- **Status:** data
- **Args:** `{"startdate": "2026-06-27", "enddate": "2026-07-03"}`
- **Shape:**

```
- cycleSummaries: list
- loggedSymptomDays: list
- loggedOvulationDays: list
- loggedNoteDays: list
```
- **Sample:**

```json
{
  "cycleSummaries": [],
  "loggedSymptomDays": [],
  "loggedOvulationDays": [],
  "loggedNoteDays": []
}
```

### get_menstrual_data_for_date

- **Status:** empty
- **Args:** `{"fordate": "2026-07-03"}`

### get_pregnancy_summary

- **Status:** empty
