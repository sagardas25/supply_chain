"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function SingleDayForecastPage() {
  const [item, setItem] = useState("");
  const [store, setStore] = useState("");
  const [date, setDate] = useState("");
  const [forecastResult, setForecastResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleForecast = async () => {
    if (!item || !store || !date) {
      toast.error("Please fill in all fields");
      return;
    }

    setLoading(true);
    setForecastResult(null);

    try {
      const res = await fetch(
        `https://walmart-api-latest.onrender.com/forecast/single-day`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ item, store, date }),
        }
      );

      if (!res.ok) throw new Error("Forecast failed");

      const data = await res.json();
      console.log("data : +" + data);

      setForecastResult(data);
    } catch (err) {
      console.error("Forecast error:", err);
      toast.error("Failed to fetch forecast");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Single-Day Forecast</h1>
      </div>

      <Card className="shadow-sm">
        <CardContent className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input
              placeholder="Item"
              value={item}
              onChange={(e) => setItem(e.target.value)}
            />
            <Input
              placeholder="Store"
              value={store}
              onChange={(e) => setStore(e.target.value)}
            />
            <Input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <Button onClick={handleForecast} disabled={loading}>
            {loading ? "Forecasting..." : "Get Forecast"}
          </Button>
        </CardContent>
      </Card>

      {forecastResult && (
        <Card className="shadow-md">
          <CardContent className="p-4">
            <h2 className="text-xl font-semibold mb-4">Forecast Result</h2>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Item</TableHead>
                  <TableHead>Store</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Forecast</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell>{forecastResult.item}</TableCell>
                  <TableCell>{forecastResult.store}</TableCell>
                  <TableCell>{forecastResult.date}</TableCell>
                  <TableCell>{forecastResult.predicted_units_sold}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
