// Sidebar Toggle
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        document.body.classList.toggle('sidebar-open');
    });
}

// Chart.js initialization for Attendance Trend
const attendanceChartElem = document.getElementById('attendanceChart');
if (attendanceChartElem) {
    const attendanceCtx = attendanceChartElem.getContext('2d');
    new Chart(attendanceCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Total Present',
                data: [480, 475, 490, 485, 495, 470, 450],
                borderColor: '#6366f1',
                tension: 0.3,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Students'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Day of the Week'
                    }
                }
            }
        }
    });
}

// Chart.js initialization for Fine Status Doughnut Chart
const fineChartElem = document.getElementById('fineChart');
if (fineChartElem) {
    const fineCtx = fineChartElem.getContext('2d');
    new Chart(fineCtx, {
        type: 'doughnut',
        data: {
            labels: ['Present', 'Absent', 'Late'],
            datasets: [{
                data: [485, 5, 10],
                backgroundColor: ['#22c55e', '#ef4444', '#f9a825']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 20
                    }
                },
            }
        }
    });
}




// Sidebar Toggle
document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.body.classList.toggle('sidebar-open');
});