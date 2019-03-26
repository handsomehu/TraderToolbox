using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp2
{
    class Program
    {
        public static bool isConnected = false;
        private static string strMarketData = "Price   Volumn\r";
        public static int theCount = 0;

        public static void onLoginCallback()
        {
            Console.WriteLine("Frond end Connected.");

            //public void getHost(string _investor = "118907", string _pwd = "Hello", string _broker = "9999"
            //, string _addr = "tcp://180.168.146.187:10031")
            CThostFtdcReqUserLoginField f = new CThostFtdcReqUserLoginField();
            f.BrokerID = "9999";
            f.UserID = "118907";
            f.Password = "Newpass";
            C1Price.UserLogin();
            Console.WriteLine("User Login Called");

        }
        public static void onRspUserLoginMethod(ref CThostFtdcRspUserLoginField pRspUserLogin, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast)
        {
            Console.WriteLine(pRspInfo.ErrorMsg);
            if (pRspInfo.ErrorID == 0)
                isConnected = true;
            Console.WriteLine("rsp login end");
        }

        static void onRtnDepthMarketDataCallback(ref CThostFtdcDepthMarketDataField pDepthMarketData)
        {
            //if (!string.IsNullOrWhiteSpace(pDepthMarketData.InstrumentID) && !pDepthMarketData.InstrumentID.StartsWith("SP"))

            strMarketData += pDepthMarketData.LastPrice.ToString() + "\t" + pDepthMarketData.Volume.ToString() + "\r";
            Console.WriteLine(pDepthMarketData.LastPrice.ToString() + "\t" + pDepthMarketData.Volume.ToString() + "\r");
            theCount += 1;


        }

        static void onRspSubMarketDataCallback(ref CThostFtdcSpecificInstrumentField pSpecificInstrument, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast)
        {
            Console.WriteLine(pRspInfo.ErrorID.ToString(), pRspInfo.ErrorMsg.ToString());
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {
            C1Price inst1 = new C1Price();
            //inst1.OnFrontConnected += new C1Price.FrontConnected(onLoginCallback);
            //inst1.OnRspUserLogin += new C1Price.RspUserLogin( onRspUserLoginMethod);
            //inst1.OnRtnDepthMarketData += new C1Price.RtnDepthMarketData(OnRtnDepthMarketDataCallback);

            inst1.OnFrontConnected += onLoginCallback;
            inst1.OnRspUserLogin += onRspUserLoginMethod;
            inst1.OnRtnDepthMarketData += onRtnDepthMarketDataCallback;

            inst1.Connect();
            string[] contractList = new string[] { "rb1905" };
            while (isConnected != true)
                System.Threading.Thread.Sleep(1000);
            
            Console.WriteLine("sub1");
            inst1.SubMarketData(contractList);
            Console.WriteLine("sub2");
            Console.WriteLine(strMarketData);

            while (theCount < 100)
            { }
            inst1.DisConnect();



                    
            
        }
    }
}
