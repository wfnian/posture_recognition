using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace @interface
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.ShowDialog();
            if (file.FileName != string.Empty)
            {
                string image1Path = file.FileName;
                listBox1.Items.Add("add image1->path :" + image1Path);
                pictureBox1.Load(image1Path);
            }
            
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Dictionary<string, object> verify = new Dictionary<string, object>();
            verify.Add("api_key", "TRSyKP-3x634yVbb7Cz1tBKB2Jl0zB0z");
            verify.Add("api_secret", "AcsV0IfXXKIOUDx3PbZr30obeumB4ekZY");

            Bitmap bitmap = new Bitmap("f:\\pix\\main.png");
            byte[] fileImage;
            using(Stream stream1 = new MemoryStream())
            {
                bitmap.Save(stream1, ImageFormat.Jpeg);
                byte[] arr = new byte[stream1.Length];
                stream1.Position = 0;
                stream1.Read(arr, 0, (int)stream1.Length);
                stream1.Close();
                fileImage = arr;
            }
            HttpHelper4MultipartForm httpHelper4MultipartForm = new HttpHelper4MultipartForm();
            verify.Add("image_file1",new HttpHelper4MultipartForm.FileParameter(fileImage,"1.jpg","");)
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.ShowDialog();
            if (file.FileName != string.Empty)
            {
                string image2Path = file.FileName;
                listBox1.Items.Add("add image2->path :" + image2Path);
                pictureBox2.Load(image2Path);
            }
        }
    }
}
