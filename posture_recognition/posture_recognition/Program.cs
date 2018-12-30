using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Net;


namespace posture_recognition
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("hello");
            String serviceAdderss = "https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton";
            //string s =Program().GetFunction(serviceAdderss);
            Program program = new Program();
            program.m();
        }
        public void m()
        {
            Console.WriteLine("???");
        }
        string GetFunction(string serviceAddress)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(serviceAddress);
            request.Method = "GET";
            request.ContentType = "text/html;charset=UTF-8";
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            Stream myResponseStream = response.GetResponseStream();
            StreamReader myStreamReader = new StreamReader(myResponseStream, Encoding.UTF8);
            string retString = myStreamReader.ReadToEnd();
            myStreamReader.Close();
            myResponseStream.Close();
            return retString;
        }

    }

}
