/**
 * Hand-written response shapes for the untyped PoC composite endpoints.
 *
 * Only the fields the Today view actually reads are declared - the backend
 * responses carry many more Garmin fields untouched. Phase 9 replaces these
 * with types generated from typed Pydantic response models via
 * openapi-typescript; until then every field stays optional since these are
 * partial views into an otherwise-untyped payload.
 */

export interface BodyBatterySample {
  endGMT?: string;
  bodyBatteryLevel?: number;
}

export interface BodyBatteryWindow {
  bodyBatteryStatList?: BodyBatterySample[];
}

export interface SummaryResponse {
  stats?: {
    totalSteps?: number;
    dailyStepGoal?: number;
    restingHeartRate?: number;
  };
  body_battery?: BodyBatteryWindow[];
}

export interface SleepResponse {
  dailySleepDTO?: {
    deepSleepSeconds?: number;
    lightSleepSeconds?: number;
    remSleepSeconds?: number;
    awakeSleepSeconds?: number;
    sleepScores?: { overall?: { value?: number } };
  };
  sleepScore?: number;
}

export type HeartRateSample = [number, number | null];

export interface HeartRateResponse {
  heartRateValues?: HeartRateSample[];
  heartRateValuesArray?: HeartRateSample[];
}

export interface HrvReading {
  startTimestampGMT?: string;
  startTimestampLocal?: string;
  hrvValue?: number | null;
}

export interface HrvResponse {
  hrvSummary?: {
    lastNight?: number;
    status?: string;
    weeklyAvg?: number;
  };
  hrvReadings?: HrvReading[];
}

export interface Activity {
  startTimeLocal?: string;
  startTimeGMT?: string;
  activityName?: string;
  name?: string;
  typeKey?: string;
  duration?: number;
  distanceMeters?: number;
  averageHR?: number;
  calories?: number;
}

export type ActivitiesResponse = Activity[];

export interface AccountSummary {
  slug: string;
  email: string;
  display_name: string;
  last_used: string | null;
}

export interface AuthStatus {
  active: string | null;
}
