import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import Historical from './Historical';

const socket = io('http://localhost:3007', {
  transports: ['websocket', 'polling']
});

const App: React.FC = () => {
  const [data, setData] = useState<any[]>([]);

  // 1. listen for a cpu event and update the state
  useEffect(() => {
    socket.on('newPrice', newPrice => {
      setData(currentData => [...currentData, newPrice]);

    });
  }, []);



    return (
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <LineChart
            data={data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
        <Historical />
      </div>
    );
  
}

export default App;
