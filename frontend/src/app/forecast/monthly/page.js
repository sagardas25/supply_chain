"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { toast } from "sonner";

export default function MonthlyForecastPage() {
  const [store, setStore] = useState("");
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleForecast = async () => {
    if (!store || !year || !month) {
      toast.error("Please fill in all fields");
      return;
    }

    setLoading(true);
    setResults([]);

    try {
      const res = await fetch(
        `https://walmart-api-latest.onrender.com/forecast/monthly`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            store,
            year: parseInt(year),
            month: parseInt(month),
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to fetch forecast");

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Error:", err);
      toast.error("Forecast request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Monthly Forecast</h1>
      </div>

      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input
              placeholder="Store ID"
              value={store}
              onChange={(e) => setStore(e.target.value)}
            />
            <Input
              placeholder="Year (e.g. 2025)"
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
            />
            <Input
              placeholder="Month (1-12)"
              type="number"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
            />
          </div>

          <Button onClick={handleForecast} disabled={loading}>
            {loading ? "Loading..." : "Get Forecast"}
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
                    <TableHead className="w-12">#</TableHead>
                    <TableHead>Item</TableHead>
                    <TableHead className="text-right">
                      Forecasted Units
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.map((result, index) => {
                    const units = result.forecasted_units;
                    let color = "text-green-600";
                    if (units >= 4000) color = "text-red-600 font-semibold";
                    else if (units >= 3700)
                      color = "text-yellow-600 font-medium";

                    return (
                      <TableRow key={index}>
                        <TableCell className="text-muted-foreground">
                          {index + 1}
                        </TableCell>
                        <TableCell className="font-medium">
                          {result.item}
                        </TableCell>
                        <TableCell className={`text-right ${color}`}>
                          {units.toLocaleString()}
                        </TableCell>
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
