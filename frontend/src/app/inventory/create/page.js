"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

export default function CreateInventoryItem() {
  const router = useRouter();
  const [form, setForm] = useState({
    walmart_item_id: "",
    name: "",
    brand: "",
    category: "",
    quantity: "",
    unit: "pieces",
    price: "",
    current_stock: "",
    min_stock_threshold: "",
    max_stock_threshold: "",
    description: "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(
        "https://walmart-api-latest.onrender.com/inventory/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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
            description: form.description || "",
          }),
        }
      );

      if (!res.ok) {
        const err = await res.json();
        console.error("API error:", err);
        throw new Error("API Error");
      }

      toast.success("Inventory item created");
      router.push("/inventory");
    } catch (err) {
      console.error(err);
      toast.error("Failed to create item");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-semibold">
            Create Inventory Item
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-4">
                <div>
                  <Label className="pb-2" htmlFor="walmart_item_id">
                    Walmart Item ID
                  </Label>
                  <Input
                    id="walmart_item_id"
                    name="walmart_item_id"
                    value={form.walmart_item_id}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="name">
                    Name
                  </Label>
                  <Input
                    id="name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="brand">
                    Brand
                  </Label>
                  <Input
                    id="brand"
                    name="brand"
                    value={form.brand}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="category">
                    Category
                  </Label>
                  <Input
                    id="category"
                    name="category"
                    value={form.category}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="quantity">
                    Quantity
                  </Label>
                  <Input
                    id="quantity"
                    name="quantity"
                    type="number"
                    value={form.quantity}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="unit">
                    Unit
                  </Label>
                  <Input
                    id="unit"
                    name="unit"
                    value={form.unit}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-4">
                <div>
                  <Label className="pb-2" htmlFor="price">
                    Price
                  </Label>
                  <Input
                    id="price"
                    name="price"
                    type="number"
                    value={form.price}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="current_stock">
                    Current Stock
                  </Label>
                  <Input
                    id="current_stock"
                    name="current_stock"
                    type="number"
                    value={form.current_stock}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="min_stock_threshold">
                    Min Stock Threshold
                  </Label>
                  <Input
                    id="min_stock_threshold"
                    name="min_stock_threshold"
                    type="number"
                    value={form.min_stock_threshold}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="max_stock_threshold">
                    Max Stock Threshold
                  </Label>
                  <Input
                    id="max_stock_threshold"
                    name="max_stock_threshold"
                    type="number"
                    value={form.max_stock_threshold}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <Label className="pb-2" htmlFor="description">
                    Description (optional)
                  </Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full mt-6" disabled={loading}>
              {loading ? "Creating..." : "Create Item"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
