'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { toast } from 'sonner';

const ITEMS_PER_PAGE = 10;

export default function DateRangeForecastPage() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const handleForecast = async () => {
    if (!startDate || !endDate) {
      toast.error('Please select both start and end dates');
      return;
    }

    setLoading(true);
    setResults([]);
    setCurrentPage(1);

    try {
      const res = await fetch('https://walmart-api-latest.onrender.com/forecast/date-range', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_date: startDate, end_date: endDate }),
      });

      if (!res.ok) throw new Error('Forecast request failed');

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      toast.error('Failed to get forecast');
    } finally {
      setLoading(false);
    }
  };

  const paginatedResults = results.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  const totalPages = Math.ceil(results.length / ITEMS_PER_PAGE);

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Date Range Forecast</h1>
      </div>

      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="flex flex-col space-y-1">
              <label htmlFor="start-date" className="text-sm font-medium">Start Date</label>
              <Input
                id="start-date"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="flex flex-col space-y-1">
              <label htmlFor="end-date" className="text-sm font-medium">End Date</label>
              <Input
                id="end-date"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
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
            <h2 className="text-xl font-semibold">Forecast Results</h2>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>#</TableHead>
                    <TableHead>Item</TableHead>
                    <TableHead>Store</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead className="text-right">Forecasted Units</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {paginatedResults.map((entry, index) => {
                    const units = parseFloat(entry.predicted_units).toFixed(2);
                    const date = new Date(entry.date).toISOString().split('T')[0];

                    let color = 'text-green-600';
                    const num = parseFloat(units);
                    if (num >= 400) color = 'text-red-600 font-semibold';
                    else if (num >= 300) color = 'text-yellow-600 font-medium';

                    return (
                      <TableRow key={index}>
                        <TableCell className="text-muted-foreground">
                          {(currentPage - 1) * ITEMS_PER_PAGE + index + 1}
                        </TableCell>
                        <TableCell className="font-medium">{entry.item_id}</TableCell>
                        <TableCell>{entry.store_id}</TableCell>
                        <TableCell>{date}</TableCell>
                        <TableCell className={`text-right ${color}`}>{units}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>

            {/* Pagination Controls */}
            <div className="flex justify-end items-center gap-4 pt-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
              >
                Previous
              </Button>
              <span className="text-sm text-muted-foreground">
                Page {currentPage} of {totalPages}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
              >
                Next
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
