const number = new Intl.NumberFormat("vi-VN");
const decimal = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 });
const currency = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
  maximumFractionDigits: 0,
});
const percent = new Intl.NumberFormat("vi-VN", {
  style: "percent",
  maximumFractionDigits: 1,
});

const formatters = {
  currency: (value) => currency.format(value),
  number: (value) => number.format(value),
  percent: (value) => percent.format(value),
};

function renderKpis(kpis) {
  const cards = [
    ["Doanh thu", kpis.total_revenue, "currency"],
    ["Đơn hàng", kpis.total_orders, "number"],
    ["Khách hàng", kpis.unique_customers, "number"],
    ["Giá trị đơn TB", kpis.average_order_value, "currency"],
    ["Seller", kpis.sellers, "number"],
    ["Review score TB", kpis.average_review_score, "decimal"],
    ["Review tích cực", kpis.positive_review_rate, "percent"],
    ["Giao trễ", kpis.late_delivery_rate, "percent"],
  ];

  document.getElementById("kpi-grid").innerHTML = cards
    .map(([label, value, type]) => {
      const formatted = type === "decimal" ? decimal.format(value) : formatters[type](value);
      return `
        <article class="kpi-card">
          <span class="kpi-label">${label}</span>
          <strong class="kpi-value">${formatted}</strong>
        </article>
      `;
    })
    .join("");
}

function renderBars(targetId, rows, labelKey, valueKey, formatter, limit = 7) {
  const selected = rows.slice(0, limit);
  const max = Math.max(...selected.map((row) => row[valueKey]), 1);
  document.getElementById(targetId).innerHTML = selected
    .map(
      (row) => `
        <div class="bar-row">
          <span class="bar-label" title="${row[labelKey]}">${row[labelKey]}</span>
          <span class="bar-track">
            <span class="bar-fill" style="width:${(row[valueKey] / max) * 100}%"></span>
          </span>
          <strong class="bar-value">${formatter(row[valueKey])}</strong>
        </div>
      `,
    )
    .join("");
}

function renderLineChart(rows) {
  const width = 900;
  const height = 280;
  const padding = { top: 18, right: 15, bottom: 30, left: 18 };
  const max = Math.max(...rows.map((row) => row.revenue), 1);
  const x = (index) =>
    padding.left + (index / Math.max(rows.length - 1, 1)) * (width - padding.left - padding.right);
  const y = (value) =>
    padding.top + (1 - value / max) * (height - padding.top - padding.bottom);
  const points = rows.map((row, index) => [x(index), y(row.revenue)]);
  const path = points.map(([px, py], index) => `${index ? "L" : "M"} ${px} ${py}`).join(" ");
  const area = `${path} L ${x(rows.length - 1)} ${height - padding.bottom} L ${x(0)} ${
    height - padding.bottom
  } Z`;

  const labels = rows
    .map((row, index) => {
      if (index % 3 !== 0 && index !== rows.length - 1) return "";
      return `<text class="axis-label" x="${x(index)}" y="${height - 8}" text-anchor="middle">${row.month}</text>`;
    })
    .join("");

  const dots = points
    .map(
      ([px, py], index) =>
        `<circle class="chart-dot" cx="${px}" cy="${py}" r="4"><title>${rows[index].month}: ${currency.format(
          rows[index].revenue,
        )}</title></circle>`,
    )
    .join("");

  document.getElementById("revenue-chart").innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Doanh thu theo tháng">
      <defs>
        <linearGradient id="revenue-fill" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#087f72" stop-opacity=".28" />
          <stop offset="100%" stop-color="#087f72" stop-opacity=".02" />
        </linearGradient>
      </defs>
      <path class="chart-area" d="${area}" />
      <path class="chart-line" d="${path}" />
      ${dots}
      ${labels}
    </svg>
  `;
}

function renderDelivery(delivery) {
  const rate = delivery.late_orders / delivery.delivered_orders;
  document.getElementById("delivery-summary").innerHTML = `
    <div class="delivery-number">${decimal.format(delivery.average_delivery_days)} ngày</div>
    <p class="delivery-caption">Thời gian giao trung bình. Độ lệch trung bình so với dự kiến:
      <strong>${decimal.format(delivery.average_delay_days)} ngày</strong>.
    </p>
    <div class="delivery-progress">
      <span style="width:${(1 - rate) * 100}%"></span>
      <span style="width:${rate * 100}%"></span>
    </div>
    <div class="delivery-legend">
      <span>Đúng hạn / sớm: ${number.format(delivery.on_time_or_early_orders)}</span>
      <span>Trễ: ${number.format(delivery.late_orders)}</span>
    </div>
  `;
}

function renderMl(ml) {
  document.getElementById("best-model").textContent = `${ml.best_model} deployed`;
  const sorted = [...ml.models].sort((a, b) => b.balanced_accuracy - a.balanced_accuracy);
  document.getElementById("model-table").innerHTML = sorted
    .map(
      (model) => `
        <tr class="${model.model === ml.best_model ? "model-winner" : ""}">
          <td>${model.model}</td>
          <td>${percent.format(model.accuracy)}</td>
          <td>${percent.format(model.balanced_accuracy)}</td>
          <td>${percent.format(model.roc_auc)}</td>
        </tr>
      `,
    )
    .join("");

  const deployed = ml.models.find((model) => model.model === ml.best_model);
  document.getElementById("matrix-caption").textContent =
    `Đánh giá trên ${number.format(ml.test_rows)} đơn hàng mới nhất.`;
  document.getElementById("confusion-matrix").innerHTML = `
    <div class="matrix-cell"><span><strong>${number.format(deployed.tn)}</strong><small>True negative</small></span></div>
    <div class="matrix-cell bad"><span><strong>${number.format(deployed.fp)}</strong><small>False positive</small></span></div>
    <div class="matrix-cell bad"><span><strong>${number.format(deployed.fn)}</strong><small>False negative</small></span></div>
    <div class="matrix-cell"><span><strong>${number.format(deployed.tp)}</strong><small>True positive</small></span></div>
  `;
  document.getElementById("negative-recall").textContent = percent.format(deployed.negative_recall);
}

async function loadDashboard() {
  const response = await fetch("./data/dashboard_data.json");
  if (!response.ok) throw new Error(`Không tải được dashboard data: ${response.status}`);
  const data = await response.json();

  document.getElementById("generated-at").textContent = new Date(data.generated_at).toLocaleString(
    "vi-VN",
  );
  renderKpis(data.kpis);
  renderLineChart(data.monthly_revenue);
  renderDelivery(data.delivery);
  renderBars("category-bars", data.top_categories, "category", "revenue", currency.format, 7);
  renderBars("state-bars", data.state_sales, "customer_state", "revenue", currency.format, 7);
  renderBars("payment-bars", data.payment_methods, "payment_type", "revenue", currency.format, 7);
  renderBars("review-bars", data.review_distribution, "review_score", "reviews", number.format, 5);
  renderMl(data.ml);
}

loadDashboard().catch((error) => {
  document.body.insertAdjacentHTML(
    "afterbegin",
    `<div class="panel" style="margin:16px">${error.message}</div>`,
  );
  console.error(error);
});
