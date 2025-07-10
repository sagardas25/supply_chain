'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

export default function EditInventoryPage() {
  const { id } = useParams();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    walmart_item_id: '',
    name: '',
    brand: '',
    category: '',
    quantity: '',
    unit: '',
    price: '',
    current_stock: '',
    min_stock_threshold: '',
    max_stock_threshold: '',
    description: '',
  });

  // Load existing item
  useEffect(() => {
    if (!id) return;

    const fetchItem = async () => {
      try {
        const res = await fetch(`https://walmart-api-latest.onrender.com/inventory/${id}`);
        if (!res.ok) throw new Error('Failed to fetch item');
        const data = await res.json();
        setForm({
          ...data,
          description: data.description || '',
        });
      } catch (err) {
        toast.error('Failed to load item data');
        console.error(err);
      }
    };

    fetchItem();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`https://walmart-api-latest.onrender.com/inventory/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          walmart_item_id: form.walmart_item_id,
          name: form.name,
          brand: form.brand,
          category: form.category,
          quantity: parseInt(form.quantity),
          unit: form.unit,
          price: parseFloat(form.price),
          current_stock: parseInt(form.current_stock),
          min_stock_threshold: parseInt(form.min_stock_threshold),
          max_stock_threshold: parseInt(form.max_stock_threshold),
          description: form.description || '',
        }),
      });

      if (!res.ok) throw new Error('Update failed');
      toast.success('Item updated successfully');
      router.push('/inventory');
    } catch (err) {
      console.error(err);
      toast.error('Failed to update item');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-semibold">Edit Inventory Item</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpdate}>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-4">
                <div>
                  <Label htmlFor="walmart_item_id">Walmart Item ID</Label>
                  <Input id="walmart_item_id" name="walmart_item_id" value={form.walmart_item_id} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" name="name" value={form.name} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="brand">Brand</Label>
                  <Input id="brand" name="brand" value={form.brand} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Input id="category" name="category" value={form.category} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="quantity">Quantity</Label>
                  <Input id="quantity" name="quantity" type="number" value={form.quantity} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="unit">Unit</Label>
                  <Input id="unit" name="unit" value={form.unit} onChange={handleChange} required />
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-4">
                <div>
                  <Label htmlFor="price">Price</Label>
                  <Input id="price" name="price" type="number" value={form.price} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="current_stock">Current Stock</Label>
                  <Input id="current_stock" name="current_stock" type="number" value={form.current_stock} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="min_stock_threshold">Min Stock Threshold</Label>
                  <Input id="min_stock_threshold" name="min_stock_threshold" type="number" value={form.min_stock_threshold} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="max_stock_threshold">Max Stock Threshold</Label>
                  <Input id="max_stock_threshold" name="max_stock_threshold" type="number" value={form.max_stock_threshold} onChange={handleChange} required />
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Textarea id="description" name="description" value={form.description} onChange={handleChange} />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full mt-6" disabled={loading}>
              {loading ? 'Updating...' : 'Update Item'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
