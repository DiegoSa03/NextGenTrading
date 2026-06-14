let portfolioChart = null;

async function loadPortfolio() {
    const res = await fetch('/api/portfolio');
    const data = await res.json();
    
    // Update top numbers
    document.getElementById('total-value').innerText = '$' + data.total_portfolio_value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits:2});
    document.getElementById('available-cash').innerText = '$' + data.cash.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits:2});
    
    // Market status
    const statusEl = document.getElementById('market-status');
    if (data.market_open) {
        statusEl.innerText = 'Market: OPEN';
        statusEl.className = 'status-badge status-open';
    } else {
        statusEl.innerText = 'Market: CLOSED';
        statusEl.className = 'status-badge status-closed';
    }

    // Update table
    const tbody = document.querySelector('#holdings-table tbody');
    tbody.innerHTML = '';
    
    let labels = ['Cash'];
    let chartData = [data.cash];
    let colors = ['#38bdf8']; // bright blue for cash

    // Fresh modern color palette (greens, teals, corals, etc, NO purple/gold)
    const colorPalette = ['#4ade80', '#f87171', '#34d399', '#f472b6', '#2dd4bf', '#fb923c'];
    let cIdx = 0;

    data.stocks.forEach(stock => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${stock.ticker}</strong></td>
            <td>${stock.shares}</td>
            <td>$${stock.current_price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits:2})}</td>
            <td>$${stock.total_value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits:2})}</td>
        `;
        tbody.appendChild(tr);
        
        labels.push(stock.ticker);
        chartData.push(stock.total_value);
        colors.push(colorPalette[cIdx % colorPalette.length]);
        cIdx++;
    });

    if(data.stocks.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="4" style="text-align:center; color: var(--text-muted)">No stocks owned yet.</td>`;
        tbody.appendChild(tr);
    }

    updateChart(labels, chartData, colors);
}

function updateChart(labels, data, colors) {
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    
    if(portfolioChart) {
        portfolioChart.destroy();
    }
    
    portfolioChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });
}

async function handleTrade(action) {
    const ticker = document.getElementById('trade-ticker').value;
    const shares = document.getElementById('trade-shares').value;
    const msgEl = document.getElementById('trade-message');
    
    msgEl.innerText = 'Processing...';
    msgEl.style.color = 'var(--text-muted)';
    
    const res = await fetch(`/api/${action}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticker, shares})
    });
    const data = await res.json();
    
    msgEl.innerText = data.message;
    msgEl.style.color = data.success ? 'var(--mint)' : 'var(--coral)';
    
    if(data.success) {
        document.getElementById('trade-ticker').value = '';
        document.getElementById('trade-shares').value = '';
        loadPortfolio();
    }
}

document.getElementById('btn-buy').addEventListener('click', () => handleTrade('buy'));
document.getElementById('btn-sell').addEventListener('click', () => handleTrade('sell'));

document.getElementById('btn-timemachine').addEventListener('click', async () => {
    const ticker = document.getElementById('time-ticker').value;
    const amount = document.getElementById('time-amount').value;
    const years = document.getElementById('time-years').value;
    const resultEl = document.getElementById('time-result');
    
    if(!ticker || !amount || !years) return;

    resultEl.style.display = 'block';
    resultEl.innerHTML = '<span style="color:var(--text-muted)">Traveling through time... ⏱️</span>';
    
    const res = await fetch('/api/timemachine', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticker, amount, years})
    });
    
    const data = await res.json();
    if(data.success) {
        const isProfit = data.profit >= 0;
        const color = isProfit ? 'var(--mint)' : 'var(--coral)';
        const sign = isProfit ? '+' : '';
        
        resultEl.innerHTML = `
            <strong>${ticker}</strong> ${years} years ago was <strong>$${data.old_price.toFixed(2)}</strong>.<br>
            Today it's <strong>$${data.current_price.toFixed(2)}</strong>.<br><br>
            Your $${amount} would now be worth <strong style="color:${color}">$${data.current_value.toFixed(2)}</strong>!<br>
            <span style="color:${color}; font-weight:bold; font-size:1.1rem">Profit: ${sign}$${data.profit.toFixed(2)}</span>
        `;
    } else {
        resultEl.innerHTML = `<span style="color:var(--coral)">Error: ${data.message}</span>`;
    }
});

// Init
loadPortfolio();
// Refresh every 30 seconds
setInterval(loadPortfolio, 30000);
