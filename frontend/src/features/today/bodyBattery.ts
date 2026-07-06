import type { BodyBatteryWindow } from '../../api/types';

/**
 * Extract the most recent body battery level from /summary's body_battery list.
 *
 * The Garmin API returns body battery as a list of time-window objects, each
 * containing a bodyBatteryStatList array. This flattens all samples across
 * windows and returns the level from the sample with the latest endGMT.
 *
 * @param bbList - body_battery array from the summary response
 * @returns latest recorded level, or null when no samples exist
 */
export function latestBodyBattery(bbList: BodyBatteryWindow[] | undefined): number | null {
  if (!bbList || bbList.length === 0) {
    return null;
  }

  const all = bbList.flatMap((w) => w.bodyBatteryStatList ?? []);

  if (all.length === 0) {
    return null;
  }

  const latest = all.reduce((a, b) => ((b.endGMT ?? '') > (a.endGMT ?? '') ? b : a));

  return latest.bodyBatteryLevel ?? null;
}
