import express from 'express';
import userRoutes from "./routes/user"
import productRoutes from "./routes/product";
import salesRoutes from "./routes/sales";

const app = express();
const port = 3000;

app.use(express.json());

app.use('/users', userRoutes);
app.use('/products', productRoutes)
app.use('/sales', salesRoutes);

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
