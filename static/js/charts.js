document.addEventListener('DOMContentLoaded', () => {
    const charts = {};
    const endpoints = {
        graficoAgua: { url: '/api/agua', label: 'Litros consumidos', color: '#3B82F6' },
        graficoLuz: { url: '/api/luz', label: 'kWh consumidos', color: '#F59E0B' },
        graficoOxigeno: { url: '/api/oxigeno', label: 'm³ utilizados', color: '#10B981' }
    };

    function loadChart(id, range) {
        const endpoint = endpoints[id];
        fetch(`${endpoint.url}?range=${range}`)
            .then(res => res.json())
            .then(data => {
                const ctx = document.getElementById(id).getContext('2d');
                if (charts[id]) {
                    charts[id].data.labels = data.labels;
                    charts[id].data.datasets[0].data = data.values;
                    charts[id].update();
                } else {
                    charts[id] = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: endpoint.label,
                                data: data.values,
                                borderColor: endpoint.color,
                                backgroundColor: endpoint.color + '33',
                                fill: true,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: { beginAtZero: true }
                            }
                        }
                    });
                }
            });
    }

    window.addEventListener("changeRange", (e) => {
        loadChart(e.detail.id, e.detail.range);
    });

    Object.keys(endpoints).forEach(id => loadChart(id, '1d'));
});