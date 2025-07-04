import { PrismaClient } from '../generated/prisma';
const prisma = new PrismaClient();
import { Router } from 'express';
const router = Router();
import { checkToken } from '../middleware/checkToken';

router.get('/', checkToken, async (req, res) => {
  try {
    const sales = await prisma.sales.findMany({
      where: {
        userId: req.user!.id,
      },
      select: {
        id: true,
        quantity: true,
        price: true,
        deleted: true,
        deletedAt: true,
        Product: {
          select: {
            id: true,
            name: true,
            price: true,
          }
        },
      },
    });

    res.status(200).json(sales);
  } catch (error) {
    console.error('Error fetching sales:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.post('/', checkToken, async (req, res) => {
  const { productId, quantity } = req.body;
  try {
    await prisma.$transaction(async (tx) => {
      const product = await tx.product.findUnique({
        where: { id: Number(productId) },
      });
      if (product?.userId !== req.user!.id) {
        res.status(403).json({ error: 'Unauthorized to sell this product' });
        throw new Error('Unauthorized to sell this product');
      }
      if (product.stock < quantity) {
        throw new Error('Insufficient stock');
      }
      const sale = await tx.sales.create({
        data: {
          productId: Number(productId),
          userId: req.user!.id,
          quantity: Number(quantity),
          price: parseFloat(product.price.toString()) * quantity,
        },
      });
      await tx.product.update({
        where: { id: Number(productId) },
        data: { stock: product.stock - quantity },
      });
      await prisma.log.create({
        data: {
          action: `${req.user!.name} sold an item for ${sale.price}`,
          userId: req.user!.id,
        },
      });
      return sale;
    });
    res.status(201).json({ message: 'Sale created successfully' });
  } catch (error) {
    console.error('Error creating sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.put('/:id', checkToken, async (req, res) => {
  const { id } = req.params;
  const { productId, quantity, price } = req.body;
  try {
    const updatedSale = await prisma.$transaction(async (tx) => {
      const sale = await tx.sales.findUnique({
        where: { id: Number(id) },
        include: { Product: true },
      });
      if (!sale) {
        throw new Error('Sale not found');
      }
      if (sale.userId !== req.user!.id) {
        res.status(403).json({ error: 'Unauthorized to update this sale' });
        throw new Error('Unauthorized to update this sale');
      }
      const product = await tx.product.findUnique({
        where: { id: Number(productId) },
      });
      if (product?.userId !== req.user!.id) {
        res.status(403).json({ error: 'Unauthorized to update this product' });
        throw new Error('Unauthorized to update this product');
      }
      if (product.stock + sale.quantity < quantity) {
        throw new Error('Insufficient stock');
      }
      await tx.product.update({
        where: { id: Number(sale.productId) },
        data: { stock: product.stock + sale.quantity - quantity },
      });
      return tx.sales.update({
        where: { id: Number(id) },
        data: {
          productId: Number(productId),
          quantity: Number(quantity),
          price: parseFloat(price),
        },
      });
    });
    res.json(updatedSale);
  } catch (error) {
    console.error('Error updating sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/:id', checkToken, async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.$transaction(async (tx) => {
      const sale = await tx.sales.findUnique({
        where: { id: Number(id) },
        include: { Product: true },
      });
      if (!sale) {
        throw new Error('Sale not found');
      }
      if (sale.userId !== req.user!.id) {
        res.status(403).json({ error: 'Unauthorized to delete this sale' });
        throw new Error('Unauthorized to delete this sale');
      }
      await tx.product.update({
        where: { id: sale.productId },
        data: { stock: sale.Product.stock + sale.quantity },
      });
      await tx.sales.findMany()
      await tx.sales.update({
        where: { id: Number(id) },
        data: { deleted: true, deletedAt: new Date() },
      });
      await tx.log.create({
        data: {
          action: `${req.user!.name} deleted sale with ID ${id}`,
          userId: req.user!.id,
        },
      });
    });
    res.status(204).json({ message: 'Sale deleted successfully' });
  } catch (error) {
    console.error('Error deleting sale:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router