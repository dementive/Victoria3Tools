using System;
using System.IO;
using System.Drawing.Imaging;
using System.Drawing;
namespace ConvertDDS
{
    using Pfim;
    using System.Collections.Generic;
    using System.Linq;
    public class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                convert_dds_to_png(args[0], args[1]);
            }
        }
        public static unsafe void convert_dds_to_png(string path, string new_path)
        {
            using var image = Pfim.FromFile(path);
            var format = image.Format switch
            {
                ImageFormat.Rgba32 => PixelFormat.Format32bppArgb,
                _ => throw new NotImplementedException(),
            };
            fixed (byte* ptr = image.Data)
            {
                using var bitmap = new Bitmap(image.Width, image.Height, image.Stride, format, (IntPtr)ptr);
                bitmap.Save(new_path, System.Drawing.Imaging.ImageFormat.Png);
            }
        }
    }
}