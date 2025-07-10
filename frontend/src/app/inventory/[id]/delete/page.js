'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { Skeleton } from '@/components/ui/skeleton';

export default function DeleteInventoryPage() {
  const { id } = useParams();
  const router = useRouter();

  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const res = await fetch(`https://walmart-api-latest.onrender.com/inventory/${id}`);
        if (!res.ok) throw new Error('Item not found');
        const data = await res.json();
        setItem(data);
      } catch (err) {
        toast.error('Failed to fetch item');
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchItem();
  }, [id]);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      const res = await fetch(`https://walmart-api-latest.onrender.com/inventory/${id}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Delete failed');
      toast.success('Item deleted successfully');
      router.push('/inventory');
    } catch (err) {
      toast.error('Deletion failed');
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-screen-md mx-auto px-6 py-10">
        <Skeleton className="h-8 w-1/3 mb-4" />
        <Skeleton className="h-20 w-full" />
      </div>
    );
  }

  if (!item) {
    return <p className="text-center text-muted-foreground mt-12">Item not found.</p>;
  }

  return (
    <div className="max-w-screen-md mx-auto px-6 py-10">
      <Card className="shadow-md border border-destructive">
        <CardHeader>
          <CardTitle className="text-xl font-bold text-destructive">
            ⚠️ Confirm Deletion
          </CardTitle>
          <p className="text-muted-foreground mt-2">
            Are you sure you want to permanently delete this item?
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <Info label="Name" value={item.name} />
            <Info label="Brand" value={item.brand} />
            <Info label="Category" value={item.category} />
            <Info label="Current Stock" value={item.current_stock} />
            <Info label="Price" value={`₹ ${item.price}`} />
            <Info label="SKU" value={item.walmart_item_id} />
          </div>

          <div className="flex justify-between gap-4 mt-6">
            <Button
              variant="outline"
              onClick={() => router.push(`/inventory/${id}`)}
              className="w-full"
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              className="w-full"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? 'Deleting...' : 'Yes, Delete'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div>
      <p className="text-muted-foreground text-xs">{label}</p>
      <p className="text-base">{value ?? '-'}</p>
    </div>
  );
}
