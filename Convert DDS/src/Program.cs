using System;
using System.IO;
using System.Drawing.Imaging;
using System.Drawing;
using System.Runtime.InteropServices;

namespace ConvertDDS
{
    using Pfim;
    using System.Collections.Generic;
    using System.Linq;
    public class Program
    {
        public static void Main(string[] args)
        {
            if (args.Length == 2)
            {
                convert_file(args[0], args[1]);
            }
        }
        public static unsafe void convert_file(string path, string new_path)
        {
            var image = Pfim.FromFile(path);

            PixelFormat format;

            switch (image.Format)
            {
                case ImageFormat.Rgb24:
                    format = PixelFormat.Format24bppRgb;
                    break;

                case ImageFormat.Rgba32:
                    format = PixelFormat.Format32bppArgb;
                    break;

                case ImageFormat.R5g5b5:
                    format = PixelFormat.Format16bppRgb555;
                    break;

                case ImageFormat.R5g6b5:
                    format = PixelFormat.Format16bppRgb565;
                    break;

                case ImageFormat.R5g5b5a1:
                    format = PixelFormat.Format16bppArgb1555;
                    break;

                case ImageFormat.Rgb8:
                    format = PixelFormat.Format8bppIndexed;
                    break;
                default:
                    throw new NotImplementedException(); 
            }
            var handle = GCHandle.Alloc(image.Data, GCHandleType.Pinned);
            try
            {
                var data = Marshal.UnsafeAddrOfPinnedArrayElement(image.Data, 0);
                var bitmap = new Bitmap(image.Width, image.Height, image.Stride, format, data);
                bitmap.Save(new_path, System.Drawing.Imaging.ImageFormat.Png);
            }
            finally
            {
                handle.Free();
            }
        }
    }
}