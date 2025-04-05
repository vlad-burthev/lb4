using System;

class Program
{
    static void Main()
    {
        double[,] A = {
            { -100, 50, 10, 25, 30 },
            { 50, -60, 5, 10, 25 },
            { 10, 5, -50, 20, 50 },
            { 25, 10, 20, -40, 10 },
            { 30, 25, 50, 10, -10 }
        };

        double[] eigenvector = { 1, 1, 1, 1, 1 };
        double tolerance = 1e-6;
        double lambdaOld = 0, lambdaNew = 0;
        int maxIterations = 1000, iter = 0;

        while (iter < maxIterations)
        {
            double[] Ax = MultiplyMatrixVector(A, eigenvector);
            lambdaNew = Ax[0] / eigenvector[0];

            if (Math.Abs(lambdaNew - lambdaOld) < tolerance)
                break;

            NormalizeVector(Ax);
            eigenvector = Ax;
            lambdaOld = lambdaNew;
            iter++;
        }

        Console.WriteLine("Найбільше власне число: " + lambdaNew);
    }

    static double[] MultiplyMatrixVector(double[,] A, double[] x)
    {
        int n = x.Length;
        double[] result = new double[n];
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                result[i] += A[i, j] * x[j];
            }
        }
        return result;
    }

    static void NormalizeVector(double[] x)
    {
        double norm = Math.Sqrt(DotProduct(x, x));
        for (int i = 0; i < x.Length; i++)
        {
            x[i] /= norm;
        }
    }

    static double DotProduct(double[] a, double[] b)
    {
        double sum = 0;
        for (int i = 0; i < a.Length; i++)
        {
            sum += a[i] * b[i];
        }
        return sum;
    }
}
