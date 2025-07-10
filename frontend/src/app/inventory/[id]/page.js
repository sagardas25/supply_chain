'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

export default function ViewInventoryItemPage() {
  const { id } = useParams();
  const router = useRouter();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const res = await fetch(`https://walmart-api-latest.onrender.com/inventory/${id}`);
        if (!res.ok) throw new Error('Failed to fetch item');
        const data = await res.json();
        setItem(data);
      } catch (err) {
        toast.error('Failed to load inventory item.');
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchItem();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-screen-lg mx-auto px-4 py-8">
        <Skeleton className="h-10 w-1/3 mb-4" />
        <div className="grid grid-cols-2 gap-4">
          {Array(10)
            .fill(0)
            .map((_, i) => (
              <Skeleton key={i} className="h-6 w-full" />
            ))}
        </div>
      </div>
    );
  }

  if (!item) {
    return <p className="text-center text-muted-foreground mt-12">Item not found.</p>;
  }

  return (
    <div className="max-w-screen-lg mx-auto px-4 py-8 space-y-6">
      <div className="flex justify-between items-center">
        <Button variant="outline" onClick={() => router.back()}>
          ← Back
        </Button>
        <Button onClick={() => router.push(`/inventory/${id}/edit`)}>
          Edit Item
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-semibold">
            {item.name}{' '}
            <Badge variant="secondary" className="ml-2 text-sm">
              {item.category}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6 text-sm">
          <Info label="Walmart ID" value={item.walmart_item_id} />
          <Info label="Brand" value={item.brand} />
          <Info label="Quantity" value={`${item.quantity} ${item.unit}`} />
          <Info label="Price">
            <Badge variant="outline" className="text-green-600 border-green-500">
              ₹ {item.price.toLocaleString()}
            </Badge>
          </Info>
          <Info label="Current Stock">
            <Badge variant="secondary">{item.current_stock}</Badge>
          </Info>
          <Info label="Min Threshold" value={item.min_stock_threshold} />
          <Info label="Max Threshold" value={item.max_stock_threshold} />
          <Info label="Created At" value={formatDate(item.created_at)} />
          <Info label="Updated At" value={formatDate(item.updated_at)} />
          {item.description && (
            <div className="md:col-span-2">
              <p className="font-medium text-muted-foreground mb-1">Description</p>
              <p className="text-base">{item.description}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Info({ label, value, children }) {
  return (
    <div>
      <p className="font-medium text-muted-foreground mb-0.5">{label}</p>
      <p className="text-base">{children ?? value ?? '-'}</p>
    </div>
  );
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}
