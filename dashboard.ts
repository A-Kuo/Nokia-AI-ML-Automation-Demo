// Define a clear Interface for our data
interface AuditLog {
    id: string;
    towerId: string;
    action: string;
    timestamp: string;
    status: 'SUCCESS' | 'FAILED';
}

// Mock Data Source (simulating API fetch from our Python backend)
const mockData: AuditLog[] = [
    { id: '1', towerId: 'T-505', action: 'ANTENNA_TILT -6deg', timestamp: '18:00:01', status: 'SUCCESS' },
    { id: '2', towerId: 'T-505', action: 'TX_POWER +2dB', timestamp: '18:00:02', status: 'SUCCESS' },
    { id: '3', towerId: 'T-101', action: 'LOAD_BALANCE_INIT', timestamp: '18:05:10', status: 'SUCCESS' }
];

class DashboardController {
    private tableBody: HTMLElement;

    constructor() {
        this.tableBody = document.getElementById('log-body') as HTMLElement;
        this.bindEvents();
        this.render(mockData);
    }

    bindEvents() {
        const btn = document.getElementById('refresh-btn');
        btn?.addEventListener('click', () => {
            console.log("Refetching automation logs...");
            // In a real app, this would be: await fetch('/api/logs')
            this.render(mockData); 
            alert("Logs refreshed from NetOps core.");
        });
    }

    render(logs: AuditLog[]) {
        this.tableBody.innerHTML = ''; // Clear current rows
        
        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.towerId}</td>
                <td style="font-family: monospace">${log.action}</td>
                <td>${log.timestamp}</td>
                <td><span class="status-success">${log.status}</span></td>
            `;
            this.tableBody.appendChild(row);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new DashboardController();
});
