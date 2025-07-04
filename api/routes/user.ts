import { PrismaClient } from '../generated/prisma';
const prisma = new PrismaClient();
import { Router } from 'express';
import { z } from 'zod';
import bcrypt from 'bcrypt';
const router = Router();
const nodemailer = require('nodemailer');

const userSchema = z.object({
  name: z.string().min(3, { message: 'Name is required' }),
  email: z.string().email().min(10, { message: 'Invalid email format' }),
  password: z.string()
});

router.get('/', async (req, res) => {
  try {
    const users = await prisma.user.findMany();
    res.status(200).json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
})

function validatePassword(password: string) {
  const msg: string[] = [];

  if (password.length < 8) {
    msg.push('Password must be at least 8 characters long');
  }

  if (!/[A-Z]/.test(password)) {
    msg.push('Password must contain at least one uppercase letter');
  }
  if (!/[a-z]/.test(password)) {
    msg.push('Password must contain at least one lowercase letter');
  }
  if (!/[0-9]/.test(password)) {
    msg.push('Password must contain at least one number');
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    msg.push('Password must contain at least one special character');
  }

  return msg;
}

router.post('/', async (req, res) => {
  const validateUser = userSchema.safeParse(req.body);
  if (!validateUser.success) {
    res.status(400).json({ errors: validateUser.error.flatten().fieldErrors });
    return 
  }

  const { name, email, password } = validateUser.data;
  const passwordErrors = validatePassword(password);

  if (passwordErrors.length > 0) {
    res.status(400).json({ errors: passwordErrors.join(', ') });
    return 
  }

  const salt = bcrypt.genSaltSync(12);
  const hash = bcrypt.hashSync(password, salt);

  try {
    const newUser = await prisma.user.create({
      data: {
        name,
        email,
        password: hash,
      },
    });
    res.status(201).json({ newUser, message: 'User created successfully' });
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const { name, email } = req.body;
  try {
    const updatedUser = await prisma.user.update({
      where: { id: Number(id) },
      data: {
        name,
        email,
      },
    });
    res.json(updatedUser);
  } catch (error) {
    console.error('Error updating user:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.user.delete({
      where: { id: Number(id) },
    });
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting user:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

function createDataTable(data: any) {
  let html = `
    <html>
    <body style="font-family: Helvetica, Arial, sans-serif;">
    <h2>Sales report</h2>
    <h3>User: ${data.user}</h3>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
      <thead style="background-color: rgb(195, 191, 191);">
        <tr>
          <th>Data e Hora</th>
          <th>Produto</th>          
          <th>Valor R$:</th>
        </tr>
      </thead>
      <tbody>
`
  let sales = 0
  for (const sale of data.sales) {
    sales += sale.price;
    const date = new Date(sale.createdAt);
    const formattedDate = date.toLocaleString('pt-BR', {
      timeZone: 'America/Sao_Paulo',
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
    html += `
        <tr>
          <td>${formattedDate}</td>
          <td>${sale.Product.name}</td>
          <td>R$ ${sale.price.toFixed(2)}</td>
        </tr>
    `;
    html += `
      </tbody>
      <tfoot>
        <tr>
          <td colspan="2" style="text-align: right; font-weight: bold;">Total:</td>
          <td>R$ ${sales.toFixed(2)}</td>
        </tr>
    `;
    return html
  }
}

const transporter = nodemailer.createTransport({
  host: "sandbox.smtp.mailtrap.io",
  port: 2525,
  secure: false, // true for 465, false for other ports
  auth: {
    user: "5a14217a5ab8ee",
    pass: "e2d426a4ce227c"
  }
})

async function sendEmail(data: any) {
  const html = createDataTable(data);
  const info = await transporter.sendMail({
    from: '"Sales Report" <sales@icloud.com>',
    to: data.userEmail,
    subject: `Sales Report for ${data.user}`,
    text: `Sales Report for ${data.user}`,
    html: html,
  });

  console.log('Message sent: %s', info.messageId);
}

router.post('/send-report/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const sales = await prisma.$transaction(async (tx) => {
      const user = await tx.user.findFirst({
        where: { id: Number(id) },
        include: {
          Sales: {
            include: {
              Product: true,
            },
          },
        },
      });
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      const data = {
        user: user.name,
        userEmail: user.email,
        sales: user.Sales,
      };
      return data;
    });

    await sendEmail(sales);
    res.status(200).json({ message: 'Report sent successfully' });
  } catch (error) {
    console.error('Error sending report:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
})

export default router;
