// @ts-check

// Chart.js is loaded as a browser global via <script> tag
const Chart = /** @type {any} */ (/** @type {any} */ (window).Chart);

/**
 * Assert that an element with the given id exists and return it.
 * Throws at runtime if the element is missing, which catches HTML/JS mismatches early.
 *
 * @template {HTMLElement} T
 * @param {string} id
 * @returns {T}
 */
function getEl(id) {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Element #${id} not found`);
  return /** @type {T} */ (el);
}

/**
 * Fetch a URL and parse the response body as JSON.
 *
 * @param {string} url
 * @returns {Promise<any>}
 * @throws {Error} on non-2xx response
 */
async function fetchJSON(url) {
  const resp = await fetch(url);

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`${resp.status}: ${text}`);
  }

  return resp.json();
}

/**
 * Return today's date as an ISO 8601 string (YYYY-MM-DD).
 *
 * @returns {string}
 */
function todayISO() {
  const d = new Date();
  return d.toISOString().slice(0, 10);
}

/**
 * Format a duration in seconds as a human-readable string (e.g. "1h 23m").
 *
 * @param {number} seconds
 * @returns {string}
 */
function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);

  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

/**
 * Replace a card value element's content with a shimmer skeleton while data loads.
 *
 * @param {string} id - element id
 */
function setLoading(id) {
  getEl(id).innerHTML = '<span class="skeleton"></span>';
}

/**
 * Set a card value element's text content, falling back to '--' for null/undefined.
 *
 * @param {string} id - element id
 * @param {string | number | null | undefined} value
 */
function setCardValue(id, value) {
  getEl(id).textContent = value != null ? String(value) : '--';
}

/**
 * Mark a card value element as errored: shows '--' and stores the error message
 * in the title attribute (visible on hover).
 *
 * @param {string} id - element id
 * @param {string} msg - error message
 */
function setCardError(id, msg) {
  const el = getEl(id);
  el.textContent = '--';
  el.title = msg;
  el.classList.add('error-text');
}

/**
 * Replace a chart canvas with an error message paragraph.
 * Called when a fetch fails and the chart cannot be rendered.
 *
 * @param {string} canvasId - id of the canvas element to replace
 * @param {string} msg - error message to display
 */
function showChartError(canvasId, msg) {
  const canvas = getEl(canvasId);
  const wrap = canvas.parentElement;
  canvas.remove();
  const p = document.createElement('p');
  p.className = 'chart-error';
  p.textContent = `No data: ${msg}`;
  wrap?.appendChild(p);
}

/**
 * Extract the most recent body battery level from the /summary body_battery list.
 *
 * The Garmin API returns body battery as a list of time-window objects, each
 * containing a bodyBatteryStatList array. This function flattens all samples,
 * sorts by endGMT descending, and returns the latest recorded level.
 *
 * @param {any[]} bbList - body_battery array from /summary response
 * @returns {number | null}
 */
function latestBodyBattery(bbList) {
  if (!Array.isArray(bbList) || bbList.length === 0) return null;

  const all = bbList.flatMap((b) => b.bodyBatteryStatList ?? []);

  if (all.length === 0) return null;

  all.sort((a, b) => (b.endGMT ?? '').localeCompare(a.endGMT ?? ''));

  return all[0].bodyBatteryLevel ?? null;
}

/**
 * Convert a Garmin HRV status string (e.g. "BALANCED") to title case.
 *
 * @param {string} status
 * @returns {string}
 */
function formatHrvStatus(status) {
  if (!status) return '';

  return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
}

/**
 * Fetch summary, sleep and HRV data and populate the five stat cards.
 * Each endpoint is fetched concurrently; a failure in one does not affect the others.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD)
 * @returns {Promise<void>}
 */
async function renderStats(date) {
  ['val-steps', 'val-sleep', 'val-bb', 'val-hr', 'val-hrv'].forEach(setLoading);

  const [summaryResult, sleepResult, hrvResult] = await Promise.allSettled([
    fetchJSON(`/summary?date=${date}`),
    fetchJSON(`/sleep-data?date=${date}`),
    fetchJSON(`/hrv?date=${date}`),
  ]);

  if (summaryResult.status === 'fulfilled') {
    const { stats, body_battery } = summaryResult.value;

    const steps = stats?.totalSteps;
    setCardValue('val-steps', steps != null ? steps.toLocaleString() : null);

    const goal = stats?.dailyStepGoal;
    getEl('val-steps-goal').textContent = goal ? `/ ${goal.toLocaleString()} goal` : '';

    setCardValue('val-hr', stats?.restingHeartRate);

    const bb = latestBodyBattery(body_battery);
    setCardValue('val-bb', bb);
  } else {
    ['val-steps', 'val-hr', 'val-bb'].forEach((id) => setCardError(id, summaryResult.reason.message));
  }

  if (sleepResult.status === 'fulfilled') {
    const dto = sleepResult.value?.dailySleepDTO ?? sleepResult.value;
    const score = dto?.sleepScores?.overall?.value ?? dto?.sleepScore ?? null;
    setCardValue('val-sleep', score);
  } else {
    setCardError('val-sleep', sleepResult.reason.message);
  }

  if (hrvResult.status === 'fulfilled') {
    const hrv = hrvResult.value;
    setCardValue('val-hrv', hrv?.hrvSummary?.lastNight);
    getEl('val-hrv-status').textContent = formatHrvStatus(hrv?.hrvSummary?.status ?? '');
  } else {
    setCardError('val-hrv', hrvResult.reason.message);
  }
}

/**
 * Fetch intraday heart rate data and render a time-series line chart.
 *
 * The Garmin API returns heartRateValues as [[timestamp_ms, bpm], ...].
 * Null bpm entries (gaps in tracking) are filtered out before plotting.
 * The full response is logged to the console on first load because the
 * field name has varied across Garmin firmware versions.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD)
 * @returns {Promise<void>}
 */
async function renderHRChart(date) {
  let data;

  try {
    data = await fetchJSON(`/heart-rate?date=${date}`);
  } catch (e) {
    showChartError('chart-hr', e instanceof Error ? e.message : String(e));
    return;
  }

  // Log full response on first load - the Garmin API structure can vary
  console.log('[heart-rate]', data);

  const rawValues = data.heartRateValues ?? data.heartRateValuesArray ?? [];

  const points = rawValues
    .filter((/** @type {any} */ entry) => Array.isArray(entry) && entry[1] !== null && entry[1] > 0)
    .map((/** @type {[number, number]} */ [ts, bpm]) => ({ x: new Date(ts), y: bpm }));

  if (points.length === 0) {
    showChartError('chart-hr', 'No intraday data');
    return;
  }

  new Chart(getEl('chart-hr'), {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Heart Rate',
          data: points,
          borderColor: '#4d9de0',
          backgroundColor: 'rgba(77,157,224,0.1)',
          borderWidth: 1.5,
          pointRadius: 0,
          tension: 0.2,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      parsing: false,
      scales: {
        x: {
          type: 'time',
          time: { unit: 'hour', displayFormats: { hour: 'HH:mm' } },
          grid: { color: '#2e3347' },
          ticks: { color: '#7b82a0', maxTicksLimit: 8 },
        },
        y: {
          grid: { color: '#2e3347' },
          ticks: { color: '#7b82a0' },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (/** @type {any} */ ctx) => `${ctx.parsed.y} bpm` } },
      },
    },
  });
}

/**
 * Fetch sleep data and render a horizontal stacked bar chart of stage durations.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD)
 * @returns {Promise<void>}
 */
async function renderSleepChart(date) {
  let data;

  try {
    data = await fetchJSON(`/sleep-data?date=${date}`);
  } catch (e) {
    showChartError('chart-sleep', e instanceof Error ? e.message : String(e));
    return;
  }

  const dto = data?.dailySleepDTO ?? data;
  const toMin = (/** @type {number | null | undefined} */ s) => Math.round((s ?? 0) / 60);

  const stages = [
    { label: 'Deep', value: toMin(dto?.deepSleepSeconds), color: '#4d9de0' },
    { label: 'Light', value: toMin(dto?.lightSleepSeconds), color: '#7b82a0' },
    { label: 'REM', value: toMin(dto?.remSleepSeconds), color: '#9b59b6' },
    { label: 'Awake', value: toMin(dto?.awakeSleepSeconds), color: '#e07070' },
  ];

  if (stages.every((s) => s.value === 0)) {
    showChartError('chart-sleep', 'No sleep stage data');
    return;
  }

  new Chart(getEl('chart-sleep'), {
    type: 'bar',
    data: {
      labels: [''],
      datasets: stages.map((s) => ({
        label: s.label,
        data: [s.value],
        backgroundColor: s.color,
      })),
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true,
          grid: { color: '#2e3347' },
          ticks: { color: '#7b82a0', callback: (/** @type {any} */ v) => `${v}m` },
        },
        y: { stacked: true, display: false },
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#e8eaf0', boxWidth: 12, padding: 12 },
        },
        tooltip: {
          callbacks: { label: (/** @type {any} */ ctx) => `${ctx.dataset.label}: ${ctx.parsed.x}m` },
        },
      },
    },
  });
}

/**
 * Fetch HRV data and render a line chart of nightly readings with a 7-day average reference line.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD)
 * @returns {Promise<void>}
 */
async function renderHRVChart(date) {
  let data;

  try {
    data = await fetchJSON(`/hrv?date=${date}`);
  } catch (e) {
    showChartError('chart-hrv', e instanceof Error ? e.message : String(e));
    return;
  }

  const readings = data?.hrvReadings ?? [];
  const points = readings.filter((/** @type {any} */ r) => r.hrvValue != null);

  if (points.length === 0) {
    showChartError('chart-hrv', 'No HRV readings');
    return;
  }

  const labels = points.map((/** @type {any} */ r) => {
    const d = new Date(r.startTimestampGMT ?? r.startTimestampLocal ?? '');
    return isNaN(d.getTime()) ? '' : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  });

  const weeklyAvg = data?.hrvSummary?.weeklyAvg;

  new Chart(getEl('chart-hrv'), {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'HRV',
          data: points.map((/** @type {any} */ r) => r.hrvValue),
          borderColor: '#4caf7d',
          backgroundColor: 'rgba(76,175,125,0.1)',
          borderWidth: 2,
          pointRadius: 4,
          tension: 0.3,
          fill: true,
        },
        ...(weeklyAvg != null
          ? [
              {
                label: '7-day avg',
                data: points.map(() => weeklyAvg),
                borderColor: '#7b82a0',
                borderDash: [4, 4],
                borderWidth: 1,
                pointRadius: 0,
                fill: false,
              },
            ]
          : []),
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { color: '#2e3347' },
          ticks: { color: '#7b82a0', maxTicksLimit: 7 },
        },
        y: {
          grid: { color: '#2e3347' },
          ticks: { color: '#7b82a0' },
          title: { display: true, text: 'ms', color: '#7b82a0' },
        },
      },
      plugins: {
        legend: { labels: { color: '#e8eaf0', boxWidth: 12 } },
      },
    },
  });
}

/**
 * Fetch recent activities and render them as a table.
 *
 * @returns {Promise<void>}
 */
async function renderActivities() {
  const tbody = getEl('activities-body');
  tbody.innerHTML = '<tr><td colspan="6" style="color:var(--text-muted)">Loading...</td></tr>';

  let data;

  try {
    data = await fetchJSON('/activities');
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="6" class="error-text">${e instanceof Error ? e.message : String(e)}</td></tr>`;
    return;
  }

  if (!Array.isArray(data) || data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" style="color:var(--text-muted)">No activities found.</td></tr>';
    return;
  }

  tbody.innerHTML = data
    .map((/** @type {any} */ a) => {
      const dt = new Date(a.startTimeLocal ?? a.startTimeGMT ?? '');
      const dateStr = isNaN(dt.getTime()) ? '--' : dt.toLocaleDateString();
      const name = a.activityName ?? a.name ?? a.typeKey ?? '--';
      const dur = a.duration ? formatDuration(a.duration) : '--';
      const dist = a.distanceMeters ? `${(a.distanceMeters / 1000).toFixed(1)} km` : '--';
      const hr = a.averageHR ?? '--';
      const cal = a.calories ? Math.round(a.calories) : '--';

      return `<tr>
      <td>${dateStr}</td>
      <td>${name}</td>
      <td>${dur}</td>
      <td>${dist}</td>
      <td>${hr}</td>
      <td>${cal}</td>
    </tr>`;
    })
    .join('');
}

/** Destroy all active Chart.js instances to allow canvas reuse on refresh. */
function destroyCharts() {
  ['chart-hr', 'chart-sleep', 'chart-hrv'].forEach((id) => Chart.getChart(id)?.destroy());
}

/**
 * Destroy existing charts and re-fetch all dashboard data for the given date.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD)
 * @returns {Promise<void>}
 */
async function loadAll(date) {
  destroyCharts();

  await Promise.allSettled([
    renderStats(date),
    renderHRChart(date),
    renderSleepChart(date),
    renderHRVChart(date),
    renderActivities(),
  ]);
}

document.addEventListener('DOMContentLoaded', () => {
  const date = todayISO();

  getEl('date-label').textContent = new Date().toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  loadAll(date);

  const btn = /** @type {HTMLButtonElement} */ (getEl('refresh-btn'));

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    btn.textContent = 'Clearing cache...';

    try {
      await fetch('/cache/clear', { method: 'POST' });
    } catch (_) {
      // cache clear failing is non-fatal
    }

    btn.textContent = 'Loading...';
    await loadAll(todayISO());
    btn.disabled = false;
    btn.textContent = 'Refresh';
  });
});
