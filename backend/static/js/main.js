document.addEventListener('DOMContentLoaded', function() {
  // --- Currency Converter ---
  document.getElementById('convert-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    document.getElementById('result').textContent = '';
    document.getElementById('error-message').textContent = '';
    const from = document.getElementById('from_currency').value.trim();
    const to = document.getElementById('to_currency').value.trim();
    const amount = document.getElementById('amount').value;
    if (!from || !to || !amount) return;
    document.getElementById('convert-btn').disabled = true;
    try {
      const res = await fetch(`/convert?from_currency=${from}&to_currency=${to}&amount=${amount}`);
      if (!res.ok) throw new Error((await res.json()).detail || 'Conversion failed');
      const data = await res.json();
      document.getElementById('result').innerHTML = `
        <div class="success">
          <b>${data.amount} ${data.from}</b> = <b>${data.converted} ${data.to}</b><br>
          Rate: <b>${data.rate}</b><br>
          Date: <b>${data.date}</b>
        </div>
      `;
    } catch (err) {
      document.getElementById('error-message').textContent = err.message;
    } finally {
      document.getElementById('convert-btn').disabled = false;
    }
  });

  // --- Conversion History ---
  const showHistoryBtn = document.getElementById('show-history-btn');
  const refreshHistoryBtn = document.getElementById('refresh-history-btn');
  const historyTable = document.getElementById('history-table');
  const historyLoading = document.getElementById('history-loading');
  function renderHistory(rows) {
    const tbody = historyTable.querySelector('tbody');
    tbody.innerHTML = '';
    rows.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${row.id}</td>
        <td>${row.from_currency}</td>
        <td>${row.to_currency}</td>
        <td>${row.amount}</td>
        <td>${row.rate}</td>
        <td>${row.converted}</td>
        <td>${row.date}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  async function fetchHistory() {
    historyLoading.textContent = 'Loading...';
    historyTable.style.display = 'none';
    try {
      const res = await fetch('/history');
      if (!res.ok) throw new Error('Failed to fetch history');
      const rows = await res.json();
      renderHistory(rows);
      historyTable.style.display = '';
      historyLoading.textContent = '';
      refreshHistoryBtn.style.display = '';
    } catch (err) {
      historyLoading.textContent = err.message;
    }
  }
  showHistoryBtn.addEventListener('click', fetchHistory);
  refreshHistoryBtn.addEventListener('click', fetchHistory);

  // --- DB Check ---
  document.getElementById('db-check-btn').addEventListener('click', async function() {
    const dbStatus = document.getElementById('db-status');
    dbStatus.textContent = 'Checking...';
    try {
      const res = await fetch('/db-check');
      if (!res.ok) throw new Error((await res.json()).detail || 'DB check failed');
      const data = await res.json();
      dbStatus.innerHTML = `<span class="success">${data.status} (Rows: ${data.result["count(*)"]})</span>`;
    } catch (err) {
      dbStatus.innerHTML = `<span class="error">${err.message}</span>`;
    }
  });

  // --- Server Info ---
  document.getElementById('server-info-btn').addEventListener('click', async function() {
    const serverInfoLoading = document.getElementById('server-info-loading');
    const serverInfoDiv = document.getElementById('server-info');
    const serverInfoTable = document.getElementById('server-info-table');
    
    serverInfoLoading.textContent = 'Loading server information...';
    serverInfoDiv.style.display = 'none';
    
    try {
      const res = await fetch('/server-info');
      if (!res.ok) throw new Error('Failed to fetch server info');
      const data = await res.json();
      
      serverInfoTable.innerHTML = '';
      
      // Display server information in a table format
      const fields = [
        { key: 'hostname', label: 'Hostname' },
        { key: 'pod_name', label: 'Pod Name' },
        { key: 'local_ip', label: 'Local IP' },
        { key: 'pod_ip', label: 'Pod IP' },
        { key: 'node_name', label: 'Node Name' },
        { key: 'namespace', label: 'Namespace' },
        { key: 'environment', label: 'Environment' },
        { key: 'platform', label: 'Platform' }
      ];
      
      fields.forEach(field => {
        if (data[field.key] && data[field.key] !== 'Unknown') {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td style="font-weight: bold; padding: 5px; border-bottom: 1px solid #ddd;">${field.label}:</td>
            <td style="padding: 5px; border-bottom: 1px solid #ddd;">${data[field.key]}</td>
          `;
          serverInfoTable.appendChild(row);
        }
      });
      
      if (data.error) {
        serverInfoTable.innerHTML = `<tr><td colspan="2" style="color: red; padding: 10px;">${data.error}</td></tr>`;
      }
      
      serverInfoDiv.style.display = 'block';
      serverInfoLoading.textContent = '';
    } catch (err) {
      serverInfoLoading.textContent = `Error: ${err.message}`;
    }
  });

  // --- Cat Image ---
  document.getElementById('show-cat-btn').addEventListener('click', function() {
    var img = document.getElementById('fx-image');
    img.style.display = 'block';
    this.style.display = 'none';
  });
});
