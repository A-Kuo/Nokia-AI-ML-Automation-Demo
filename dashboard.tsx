import React, { useState } from 'react';

// Interface defining the structure of our automation logs
interface AuditLog {
  id: string;
  towerId: string;
  action: string;
  timestamp: string;
  status: 'SUCCESS' | 'FAILED';
}

export const AutomationDashboard: React.FC = () => {
  // Mock data representing logs fetched from the Python backend
  const [logs] = useState<AuditLog[]>([
    { id: '1', towerId: 'T-505', action: 'ANTENNA_TILT -6deg', timestamp: '18:00:01', status: 'SUCCESS' },
    { id: '2', towerId: 'T-505', action: 'TX_POWER +2dB', timestamp: '18:00:02', status: 'SUCCESS' },
  ]);

  return (
    <div className="p-6 bg-gray-50 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-blue-900">📡 Network Automation Audit</h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border">
          <thead className="bg-gray-100">
            <tr>
              <th className="py-2 px-4 border-b">Tower ID</th>
              <th className="py-2 px-4 border-b">Automated Action</th>
              <th className="py-2 px-4 border-b">Timestamp</th>
              <th className="py-2 px-4 border-b">Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-gray-50">
                <td className="py-2 px-4 border-b">{log.towerId}</td>
                <td className="py-2 px-4 border-b font-mono text-sm">{log.action}</td>
                <td className="py-2 px-4 border-b">{log.timestamp}</td>
                <td className="py-2 px-4 border-b">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    log.status === 'SUCCESS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {log.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
