document.getElementById('converter-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const from = document.getElementById('from').value.toUpperCase();
  const to = document.getElementById('to').value.toUpperCase();
  const amount = document.getElementById('amount').value;

  const resultBox = document.getElementById('result-box');
  const resultText = document.getElementById('result');

  try {
    const response = await fetch(`/convert?from_currency=${from}&to_currency=${to}&amount=${amount}`);
    const data = await response.json();

    if (response.ok) {
      resultText.textContent = `${amount} ${from} = ${data.converted} ${to}`;
    } else {
      resultText.textContent = `Error: ${data.detail}`;
    }

    resultBox.style.display = 'block';
  } catch (error) {
    resultText.textContent = '❌ Failed to fetch conversion.';
    resultBox.style.display = 'block';
  }
});
