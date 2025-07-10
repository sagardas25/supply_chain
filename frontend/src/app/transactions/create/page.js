'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

export default function CreateStockTransaction() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [inventoryItems, setInventoryItems] = useState([]);
  const [form, setForm] = useState({
    item_id: '',
    transaction_type: '',
    quantity: '',
    reason: '',
  });

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const res = await fetch('https://walmart-api-latest.onrender.com/inventory/');
        const data = await res.json();
        setInventoryItems(data);
      } catch (err) {
        toast.error('Failed to load inventory list');
        console.error(err);
      }
    };
    fetchInventory();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('https://walmart-api-latest.onrender.com/stock/transaction/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: parseInt(form.item_id),
          transaction_type: form.transaction_type,
          quantity: parseInt(form.quantity),
          reason: form.reason,
        }),
      });

      if (!res.ok) throw new Error('Transaction failed');
      toast.success('Stock transaction created!');
      router.push('/inventory');
    } catch (err) {
      console.error(err);
      toast.error('Failed to create transaction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-screen-lg mx-auto px-6 py-10">
      <Card className="shadow-lg border border-muted rounded-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">New Stock Transaction</CardTitle>
          <p className="text-sm text-muted-foreground mt-1">
            Update stock levels by recording an incoming, outgoing, or adjustment entry.
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Inventory Item */}
            <div className="col-span-full">
              <Label className="mb-1 block">Select Inventory Item</Label>
              <Select
                value={form.item_id}
                onValueChange={(value) => setForm({ ...form, item_id: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Choose an item" />
                </SelectTrigger>
                <SelectContent>
                  {inventoryItems.map((item) => (
                    <SelectItem key={item.id} value={String(item.id)}>
                      {item.name} ({item.walmart_item_id})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Transaction Type */}
            <div>
              <Label className="mb-1 block">Transaction Type</Label>
              <Select
                value={form.transaction_type}
                onValueChange={(value) => setForm({ ...form, transaction_type: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="IN">IN – Incoming</SelectItem>
                  <SelectItem value="OUT">OUT – Outgoing</SelectItem>
                  <SelectItem value="ADJUSTMENT">ADJUSTMENT – Manual fix</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Quantity */}
            <div>
              <Label htmlFor="quantity" className="mb-1 block">Quantity</Label>
              <Input
                id="quantity"
                name="quantity"
                type="number"
                value={form.quantity}
                onChange={handleChange}
                placeholder="e.g. 10"
                required
              />
            </div>

            {/* Reason */}
            <div className="md:col-span-full">
              <Label htmlFor="reason" className="mb-1 block">Reason / Notes</Label>
              <Textarea
                id="reason"
                name="reason"
                rows={3}
                value={form.reason}
                onChange={handleChange}
                placeholder="E.g. damaged items, stock audit adjustment..."
              />
            </div>

            {/* Submit Button */}
            <div className="md:col-span-full">
              <Button type="submit" disabled={loading} className="w-full md:w-48">
                {loading ? 'Submitting...' : 'Submit Transaction'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
