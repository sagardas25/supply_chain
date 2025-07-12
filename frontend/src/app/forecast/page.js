'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';

const forecastRoutes = [
  {
    title: 'Single Day Forecast',
    description: 'Predict demand for a single item in one store on a specific date.',
    href: '/forecast/single-day',
  },
  {
    title: 'Monthly Forecast',
    description: 'Predict sales for all items in one store over a month.',
    href: '/forecast/monthly',
  },
  {
    title: 'Date Range Forecast',
    description: 'Forecast all items across all stores over a given date range.',
    href: '/forecast/date-range',
  },
  {
    title: 'Single Day – All Stores',
    description: 'Forecast a specific item across all stores for a single day.',
    href: '/forecast/single-day-all-stores',
  },

];

export default function ForecastDashboardPage() {
  return (
    <div className="p-6 sm:p-10 max-w-full  mx-auto space-y-8 bg-gray-300">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-2">Forecasting Dashboard</h1>
        <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
          Choose a forecasting feature to get insights on sales performance.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {forecastRoutes.map((route, index) => (
          <Card
            key={index}
            className="border border-gray-200 bg-white rounded-2xl shadow-sm hover:shadow-md transition-shadow"
          >
            <CardHeader>
              <CardTitle className="text-lg text-gray-800">{route.title}</CardTitle>
              <CardDescription className="text-sm text-gray-500">{route.description}</CardDescription>
            </CardHeader>
            <CardContent className="pt-0">
              <Link href={route.href}>
                <Button
                  variant="default"
                  className="w-full mt-4 shadow-md hover:shadow-lg transition-all duration-150 bg-primary text-white hover:bg-primary/90"
                >
                  Open <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
