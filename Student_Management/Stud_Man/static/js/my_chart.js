function drawClassStats(labels, data) {
    const ctx = document.getElementById('classStats');

    new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Sĩ số',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'pink', 'purple', 'black', 'gray', 'darkblue']
      }]
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Combined Line/Bar Chart'
      }
    }
  });
}

function drawClassPassStats(labels, data) {
    const ctx = document.getElementById('classPassStats');

    new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Tỷ lệ đạt',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'pink', 'purple', 'black', 'gray', 'darkblue']
      }]
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Combined Line/Bar Chart'
      }
    }
  });
}

function insertSjName() {
    let a = document.getElementById("stats-subject-name")
    let c = document.getElementById("stats-semester")
    let b = document.getElementById("text-subject")
    let d = document.getElementById("text-semester")
    b.innerHTML = a.value
    d.innerHTML = c.value
}

