// node Fred.js
import fetch from 'node-fetch';
import Table from 'cli-table3';

// Configurable options
const showSummaryTable = true;  // Show summary table with averages and medians
const roundToInt = false;        // Display integers only

const FRED_API_KEY = '2959dfe84aa500118d187cd28baa847c';
const FRED_BASE_URL = 'https://api.stlouisfed.org/fred/series/observations';

const seriesId = 'ICSA';
// Example: 'GDP' for Gross Domestic Product
// The print I saw in 2020 is the annualized % change for realGDP
// Current-Dollar GDP is the $29 trillion figure that I know https://fred.stlouisfed.org/series/GDP 
// realGDP = GDPC1; nominalGDP = NGDPSAXDCUSQ

const params = {
  series_id: seriesId,
  api_key: FRED_API_KEY,
  file_type: 'json',
};

function buildUrl(baseUrl, queryParams) {
  const query = new URLSearchParams(queryParams).toString();
  return `${baseUrl}?${query}`;
}

function calculatePercentageChange(current, previous) {
  if (!previous || previous === 0) return null;
  return ((current - previous) / previous) * 100;
}

function formatNumber(value) {
  return roundToInt ? Math.round(value) : value.toFixed(2);
}

function calculateAverage(arr) {
  const sum = arr.reduce((acc, item) => acc + item.value, 0);
  return sum / arr.length;
}

function calculateMedian(arr) {
  const sorted = arr.map(d => d.value).sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0
    ? sorted[mid]
    : (sorted[mid - 1] + sorted[mid]) / 2;
}

function sliceAndSummarize(data, label, weeks) {
  const subset = data.slice(-weeks);
  if (subset.length === 0) return null;
  return {
    period: label,
    average: calculateAverage(subset),
    median: calculateMedian(subset),
  };
}

async function fetchFredData() {
  const url = buildUrl(FRED_BASE_URL, params);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    const observations = data.observations.map((obs) => ({
      date: obs.date,
      value: parseFloat(obs.value),
    }));

    const enhancedData = observations.map((obs, index) => ({
      date: obs.date,
      value: obs.value,
      pctChangePrev: calculatePercentageChange(
        obs.value,
        observations[index - 1]?.value
      ),
      pctChange4Periods: calculatePercentageChange(
        obs.value,
        observations[index - 4]?.value
      ),
    }));

    const detailTable = new Table({
      head: ['Date', 'Value', '% Change (Prev)', '% Change (4 Periods Ago)'],
    });

    enhancedData.forEach((row) => {
      detailTable.push([
        row.date,
        formatNumber(row.value),
        row.pctChangePrev !== null ? `${formatNumber(row.pctChangePrev)}%` : 'N/A',
        row.pctChange4Periods !== null ? `${formatNumber(row.pctChange4Periods)}%` : 'N/A',
      ]);
    });

    console.log(detailTable.toString());

    if (showSummaryTable) {
      const summaryData = [
        sliceAndSummarize(observations, '1 Year (52 wks)', 52),
        sliceAndSummarize(observations, '3 Year (156 wks)', 156),
        sliceAndSummarize(observations, '5 Year (260 wks)', 260),
        sliceAndSummarize(observations, '10 Year (520 wks)', 520),
      ].filter(Boolean);

      const summaryTable = new Table({
        head: ['Period', 'Average', 'Median'],
      });

      summaryData.forEach(row => {
        summaryTable.push([
          row.period,
          formatNumber(row.average),
          formatNumber(row.median),
        ]);
      });

      console.log('\nSummary Averages & Medians:');
      console.log(summaryTable.toString());
    }
  } catch (error) {
    console.error('Error fetching data from FRED:', error);
  }
}

fetchFredData();
