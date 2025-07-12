"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
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
import ConfirmDialog from "@/components/ConfirmDialog";

export default function InventoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showConfirm, setShowConfirm] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  const fetchItems = async () => {
    try {
      const res = await fetch(
        "https://walmart-api-latest.onrender.com/inventory/"
      );
      const data = await res.json();
      setItems(data);
    } catch (err) {
      console.error("Failed to fetch inventory:", err);
      toast.error("Failed to fetch inventory");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDeleteClick = (id) => {
    setSelectedId(id);
    setShowConfirm(true);
  };

  const handleConfirmDelete = async () => {
    try {
      const res = await fetch(
        `https://walmart-api-latest.onrender.com/inventory/${selectedId}`,
        {
          method: "DELETE",
        }
      );

      if (!res.ok) throw new Error("Delete failed");

      toast.success("Item deleted successfully");
      fetchItems(); // refresh list
    } catch (err) {
      console.error("Failed to delete item:", err);
      toast.error("Failed to delete item");
    } finally {
      setShowConfirm(false);
      setSelectedId(null);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <h1 className="text-3xl font-bold">Inventory Items</h1>
        <div className="flex gap-3">
        <Link href="/forecast">
  <Button
    className="rounded-xl bg-blue-500 text-white hover:bg-blue-700 shadow-md hover:shadow-lg transition-all"
  >
    Go to Forecasting
  </Button>
</Link>


          <Link href="/inventory/create">
            <Button className="rounded-xl shadow-md hover:shadow-lg">
              + Add New Item
            </Button>
          </Link>
        </div>
      </div>

      <Card className="shadow-md">
        <CardContent className="p-4">
          {loading ? (
            <p className="text-muted-foreground">Loading...</p>
          ) : items.length === 0 ? (
            <p className="text-muted-foreground">No items found.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Brand</TableHead>
                  <TableHead>Quantity</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-center">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{item.name}</TableCell>
                    <TableCell>{item.brand}</TableCell>
                    <TableCell>{item.quantity}</TableCell>
                    <TableCell>{item.category}</TableCell>
                    <TableCell className="text-center space-x-2">
                      <Link href={`/inventory/${item.id}`}>
                        <Button
                          className="hover:bg-gray-400"
                          variant="secondary"
                          size="sm"
                        >
                          View
                        </Button>
                      </Link>
                      <Link href={`/inventory/${item.id}/edit`}>
                        <Button className="hover:bg-gray-600" size="sm">
                          Edit
                        </Button>
                      </Link>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDeleteClick(item.id)}
                        className="hover:bg-red-800"
                      >
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <ConfirmDialog
        open={showConfirm}
        onCancel={() => setShowConfirm(false)}
        onConfirm={handleConfirmDelete}
      />
    </div>
  );
}
