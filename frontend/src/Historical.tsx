
import React, { useEffect, useState } from 'react';
import axios , {AxiosResponse} from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
interface query_type{
    item:any;
}
const Historical: React.FC = () => {  
    const [data, setData] = useState([]);

  useEffect(() => {
    axios.get<query_type[]>('http://127.0.0.1:5000/api/data')
      .then((response:AxiosResponse) => {
        const formattedData = response.data.map((item:{'timestamp':any}) => ({
          ...item,
          timestamp: new Date(item.timestamp * 1000).toLocaleString()
        }));
        setData(formattedData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer>
        <LineChart
          width={500}
          height={300}
          data={data}
          margin={{
            top: 5, right: 30, left: 20, bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Historical;
