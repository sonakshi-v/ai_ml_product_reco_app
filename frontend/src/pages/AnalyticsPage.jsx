import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import './AnalyticsPage.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const API_BASE_URL = 'https://ai-ml-product-reco-app.onrender.com/api';

function AnalyticsPage() {
  const [summary, setSummary] = useState(null);
  const [priceDist, setPriceDist] = useState(null);
  const [topBrands, setTopBrands] = useState([]);
  const [topCategories, setTopCategories] = useState([]);
  const [materials, setMaterials] = useState([]);
  const [colors, setColors] = useState([]);
  const [countries, setCountries] = useState([]);
  const [priceByCat, setPriceByCat] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [
        summaryRes,
        priceRes,
        brandsRes,
        categoriesRes,
        materialsRes,
        colorsRes,
        countriesRes,
        priceByCatRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/analytics/summary`),
        axios.get(`${API_BASE_URL}/analytics/price-distribution`),
        axios.get(`${API_BASE_URL}/analytics/top-brands`),
        axios.get(`${API_BASE_URL}/analytics/top-categories`),
        axios.get(`${API_BASE_URL}/analytics/material-distribution`),
        axios.get(`${API_BASE_URL}/analytics/color-distribution`),
        axios.get(`${API_BASE_URL}/analytics/country-origin`),
        axios.get(`${API_BASE_URL}/analytics/price-by-category`)
      ]);

      setSummary(summaryRes.data);
      setPriceDist(priceRes.data);
      setTopBrands(brandsRes.data);
      setTopCategories(categoriesRes.data);
      setMaterials(materialsRes.data);
      setColors(colorsRes.data);
      setCountries(countriesRes.data);
      setPriceByCat(priceByCatRes.data);
    } catch (err) {
      setError('Failed to load analytics data.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-page"><div className="loading">Loading analytics...</div></div>;
  }

  if (error) {
    return <div className="analytics-page"><div className="error-message">{error}</div></div>;
  }

  // Chart data
  const brandChartData = {
    labels: topBrands.map(b => b.brand),
    datasets: [{
      label: 'Number of Products',
      data: topBrands.map(b => b.count),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
    }]
  };

  const categoryChartData = {
    labels: topCategories.map(c => c.category),
    datasets: [{
      label: 'Number of Products',
      data: topCategories.map(c => c.count),
      backgroundColor: 'rgba(153, 102, 255, 0.6)',
    }]
  };

  const materialChartData = {
    labels: materials.map(m => m.material),
    datasets: [{
      data: materials.map(m => m.count),
      backgroundColor: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
      ],
    }]
  };

  return (
    <div className="analytics-page">
      <div className="analytics-container">
        <h2>Dataset Analytics</h2>

        {summary && (
          <div className="summary-cards">
            <div className="summary-card">
              <h3>Total Products</h3>
              <p className="metric">{summary.total_products.toLocaleString()}</p>
            </div>
            <div className="summary-card">
              <h3>Unique Brands</h3>
              <p className="metric">{summary.unique_brands}</p>
            </div>
            <div className="summary-card">
              <h3>Average Price</h3>
              <p className="metric">${summary.price_range.mean.toFixed(2)}</p>
            </div>
            <div className="summary-card">
              <h3>Products with Images</h3>
              <p className="metric">{summary.products_with_images} ({summary.image_percentage.toFixed(1)}%)</p>
            </div>
          </div>
        )}

        <div className="charts-grid">
          <div className="chart-container">
            <h3>Top Brands</h3>
            <Bar data={brandChartData} options={{ responsive: true }} />
          </div>

          <div className="chart-container">
            <h3>Top Categories</h3>
            <Bar data={categoryChartData} options={{ responsive: true }} />
          </div>

          <div className="chart-container">
            <h3>Material Distribution</h3>
            <Doughnut data={materialChartData} options={{ responsive: true }} />
          </div>

          <div className="chart-container">
            <h3>Price Range by Category</h3>
            {priceByCat.length > 0 && (
              <Bar
                data={{
                  labels: priceByCat.map(p => p.category),
                  datasets: [{
                    label: 'Average Price ($)',
                    data: priceByCat.map(p => p.avg_price),
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                  }]
                }}
                options={{ responsive: true }}
              />
            )}
          </div>
        </div>

        <div className="data-tables">
          <div className="table-container">
            <h3>Color Distribution</h3>
            <table>
              <thead>
                <tr>
                  <th>Color</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                {colors.map((color, idx) => (
                  <tr key={idx}>
                    <td>{color.color}</td>
                    <td>{color.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="table-container">
            <h3>Country of Origin</h3>
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                {countries.map((country, idx) => (
                  <tr key={idx}>
                    <td>{country.country}</td>
                    <td>{country.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;
