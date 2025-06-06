import { PrismaClient } from '../generated/prisma';
const prisma = new PrismaClient();
import { Router } from 'express';
const router = Router();

router.get('/', async (req, res) => {
  try {
    const sales = await prisma.sales.findMany({
      include: {
        Product: true,
        User: true,
      },
    });
    res.status(200).json(sales);
  } catch (error) {
    console.error('Error fetching sales:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.post('/', async (req, res) => {
  const { productId, userId, quantity } = req.body;
  try {
    const newSale = await prisma.$transaction(async (tx) => {
      const product = await tx.product.findUnique({
        where: { id: Number(productId) },
      });
      if (!product) {
        throw new Error('Product not found');
      }
      if (product.stock < quantity) {
        throw new Error('Insufficient stock');
      }
      const sale = await tx.sales.create({
        data: {
          productId: Number(productId),
          userId: Number(userId),
          quantity: Number(quantity),
          price: parseFloat(product.price.toString()) * quantity,
        },
      });
      await tx.product.update({
        where: { id: Number(productId) },
        data: { stock: product.stock - quantity },
      });
      return sale;
    });
    res.status(201).json({ newSale, message: 'Sale created successfully' });
  } catch (error) {
    console.error('Error creating sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { productId, userId, quantity, price } = req.body;
  try {
    const updatedSale = await prisma.sales.update({
      where: { id: Number(id) },
      data: {
        productId: Number(productId),
        userId: Number(userId),
        quantity: Number(quantity),
        price: parseFloat(price),
      },
    });
    res.json(updatedSale);
  } catch (error) {
    console.error('Error updating sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const deleteSale = await prisma.$transaction(async (tx) => {
      const sale = await tx.sales.findUnique({
        where: { id: Number(id) },
        include: { Product: true },
      });
      if (!sale) {
        throw new Error('Sale not found');
      }
      await tx.product.update({
        where: { id: sale.productId },
        data: { stock: sale.Product.stock + sale.quantity },
      });
      await tx.sales.findMany()
      return tx.sales.delete({
        where: { id: Number(id) },
      });
    });
    res.status(204).send({ deleteSale, message: 'Sale deleted successfully' });
  } catch (error) {
    console.error('Error deleting sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router
