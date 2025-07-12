'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { toast } from 'sonner';

export default function SingleDayAllStoresForecastPage() {
  const [item, setItem] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleForecast = async () => {
    if (!item || !date) {
      toast.error('Please provide both item and date');
      return;
    }

    setLoading(true);
    setResults([]);

    try {
      const res = await fetch('https://walmart-api-latest.onrender.com/forecast/single-day-all-stores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item, date }),
      });

      if (!res.ok) throw new Error('Failed to fetch forecast');

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      toast.error('Failed to get forecast');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Single Day All Stores Forecast</h1>
      </div>

      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="flex flex-col space-y-1">
              <label htmlFor="item" className="text-sm font-medium">Item</label>
              <Input
                id="item"
                type="text"
                value={item}
                onChange={(e) => setItem(e.target.value)}
                placeholder="e.g., Rice"
              />
            </div>
            <div className="flex flex-col space-y-1">
              <label htmlFor="date" className="text-sm font-medium">Date</label>
              <Input
                id="date"
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>
          </div>

          <Button onClick={handleForecast} disabled={loading}>
            {loading ? 'Loading...' : 'Get Forecast'}
          </Button>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card className="shadow-md">
          <CardContent className="p-4 space-y-4">
            <h2 className="text-xl font-semibold">
              Forecast for <span className="text-primary">{item}</span> on{' '}
              <span className="text-primary">{date}</span>
            </h2>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>#</TableHead>
                    <TableHead>Store</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead className="text-right">Forecasted Units</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.map((entry, index) => {
                    const units = parseFloat(entry.predicted_units_sold).toFixed(2);
                    const forecastDate = new Date(entry.date).toISOString().split('T')[0];

                    let color = 'text-green-600';
                    const num = parseFloat(units);
                    if (num >= 140) color = 'text-red-600 font-semibold';
                    else if (num >= 125) color = 'text-yellow-600 font-medium';

                    return (
                      <TableRow key={index}>
                        <TableCell className="text-muted-foreground">{index + 1}</TableCell>
                        <TableCell className="font-medium">{entry.store}</TableCell>
                        <TableCell>{forecastDate}</TableCell>
                        <TableCell className={`text-right ${color}`}>{units}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
