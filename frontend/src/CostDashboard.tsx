import { useState, useEffect } from 'react';

interface CostRecord {
  date: string;
  service: string;
  cost: number;
}

function CostDashboard() {
  const [costs, setCosts] = useState<CostRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // For now, use mock data
    // Later we'll fetch from API
    const mockData: CostRecord[] = [
      { date: '2025-01-15', service: 'Amazon EC2', cost: 45.67 },
      { date: '2025-01-15', service: 'Amazon S3', cost: 12.34 },
      { date: '2025-01-15', service: 'Amazon RDS', cost: 89.12 },
      { date: '2025-01-14', service: 'Amazon EC2', cost: 43.21 },
      { date: '2025-01-14', service: 'AWS Lambda', cost: 2.15 },
    ];

    // Simulate API delay
    setTimeout(() => {
      setCosts(mockData);
      setLoading(false);
    }, 500);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          AWS Cost Dashboard
        </h1>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Service
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cost
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {costs.map((cost, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {cost.date}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {cost.service}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-green-600">
                    ${cost.cost.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            📊 Showing mock data. Next week we'll connect to real AWS API!
          </p>
        </div>
      </div>
    </div>
  );
}

export default CostDashboard;