export const fetchInventory = async () => {
  const res = await fetch("https://walmart-api-latest.onrender.com/inventory/");
  return res.json();
};
