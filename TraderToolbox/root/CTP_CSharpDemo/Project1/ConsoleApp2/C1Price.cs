using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;

namespace ConsoleApp2
{
    public class C1Price
    {
        /// 
        const string strDllFile = @"C:\hdbstudio_rev\TraderToolbox\root\CTP_CSharpDemo\Project1\Debug\PROJECT1.dll";
        string FrontAddr;
        string BrokerID;
        string InvestorID;
        string password;

        public void getHost(string _investor = "118907", string _pwd = "Hello", string _broker = "9999"
            , string _addr = "tcp://180.168.146.187:10031")
        {
            this.FrontAddr = _addr;
            this.BrokerID = _broker;
            this.InvestorID = _investor;
            this.password = _pwd;
        }
        public C1Price()
        {
            getHost();
        }
        public void Connect() { Console.WriteLine(this.FrontAddr); connect(this.FrontAddr); }
        [DllImport(strDllFile, EntryPoint = "?Connect@@YAXPAD@Z", CallingConvention = CallingConvention.Cdecl)]
        static extern void connect(string pFrontAddr);

        /// <summary>
        /// 断开连接
        /// </summary>
        public void DisConnect() { disConnect(); }
        [DllImport(strDllFile, EntryPoint = "?DisConnect@@YAXXZ", CallingConvention = CallingConvention.Cdecl)]
        static extern void disConnect();

        /// <summary>
        /// 登录
        /// </summary>
        public static void UserLogin() { userLogin("9999", "118907", "Hello"); }
        [DllImport(strDllFile, EntryPoint = "?ReqUserLogin@@YAXQAD00@Z", CallingConvention = CallingConvention.Cdecl)]
        static extern void userLogin(string BROKER_ID, string INVESTOR_ID, string PASSWORD);

        /// <summary>
        /// 用户注销
        /// </summary>
        public void UserLogout() { userLogout(this.BrokerID, this.InvestorID); }
        [DllImport(strDllFile, EntryPoint = "?ReqUserLogout@@YAXQAD0@Z", CallingConvention = CallingConvention.Cdecl)]
        static extern void userLogout(string BROKER_ID, string INVESTOR_ID);

        #region 错误响应
        [DllImport(strDllFile, EntryPoint = "?RegOnRspError@@YGXP6GHPAUCThostFtdcRspInfoField@@H_N@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRspError(RspError cb);
        RspError rspError;
        /// <summary>
        /// 
        /// </summary>
        public delegate void RspError(ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast);
        /// <summary>
        /// 连接响应
        /// </summary>
        public event RspError OnRspError
        {
            add { rspError += value; regOnRspError(rspError); }
            remove { rspError -= value; regOnRspError(rspError); }

        }
        #endregion

        #region 心跳响应
        [DllImport(strDllFile, EntryPoint = "?RegOnHeartBeatWarning@@YGXP6GHH@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnHeartBeatWarning(HeartBeatWarning cb);
        HeartBeatWarning heartBeatWarning;
        /// <summary>
        /// 
        /// </summary>
        public delegate void HeartBeatWarning(int nTimeLapse);
        /// <summary>
        /// 心跳响应
        /// </summary>
        public event HeartBeatWarning OnHeartBeatWarning
        {
            add { heartBeatWarning += value; regOnHeartBeatWarning(heartBeatWarning); }
            remove { heartBeatWarning -= value; regOnHeartBeatWarning(heartBeatWarning); }

        }
        #endregion

        #region 连接响应
        [DllImport(strDllFile, EntryPoint = "?RegOnFrontConnected@@YGXP6GHXZ@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnFrontConnected(FrontConnected cb);
        FrontConnected frontConnected;
        /// <summary>
        /// 
        /// </summary>
        public delegate void FrontConnected();
        /// <summary>
        /// 连接响应
        /// </summary>
        public event FrontConnected OnFrontConnected
        {
            add { frontConnected += value; regOnFrontConnected(frontConnected); }
            remove { frontConnected -= value; regOnFrontConnected(frontConnected); }

        }
        #endregion

        #region 断开应答
        [DllImport(strDllFile, EntryPoint = "?RegOnFrontDisconnected@@YGXP6GHH@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnFrontDisconnected(FrontDisconnected cb);
        FrontDisconnected frontDisconnected;
        /// <summary>
        /// 
        /// </summary>
        public delegate void FrontDisconnected(int nReason);
        /// <summary>
        /// 断开应答
        /// </summary>
        public event FrontDisconnected OnFrontDisconnected
        {
            add { frontDisconnected += value; regOnFrontDisconnected(frontDisconnected); }
            remove { frontDisconnected -= value; regOnFrontDisconnected(frontDisconnected); }
        }
        #endregion

        #region 登入请求应答
        [DllImport(strDllFile, EntryPoint = "?RegOnRspUserLogin@@YGXP6GHPAUCThostFtdcRspUserLoginField@@PAUCThostFtdcRspInfoField@@H_N@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRspUserLogin(RspUserLogin cb);
        RspUserLogin rspUserLogin;
        /// <summary>
        /// 
        /// </summary>
        public delegate void RspUserLogin(ref CThostFtdcRspUserLoginField pRspUserLogin, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast);
        /// <summary>
        /// 登入请求应答
        /// </summary>
        public event RspUserLogin OnRspUserLogin
        {
            add { rspUserLogin += value; regOnRspUserLogin(rspUserLogin); }
            remove { rspUserLogin -= value; regOnRspUserLogin(rspUserLogin); }
        }
        #endregion

        #region 登出请求应答
        [DllImport(strDllFile, EntryPoint = "?RegOnRspUserLogout@@YGXP6GHPAUCThostFtdcUserLogoutField@@PAUCThostFtdcRspInfoField@@H_N@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRspUserLogout(RspUserLogout cb);
        RspUserLogout rspUserLogout;
        /// <summary>
        /// 
        /// </summary>
        /// <param name="pUserLogout"></param>
        /// <param name="pRspInfo"></param>
        /// <param name="nRequestID"></param>
        /// <param name="bIsLast"></param>
        public delegate void RspUserLogout(ref CThostFtdcUserLogoutField pUserLogout, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast);
        /// <summary>
        /// 登出请求应答
        /// </summary>
        public event RspUserLogout OnRspUserLogout
        {
            add { rspUserLogout += value; regOnRspUserLogout(rspUserLogout); }
            remove { rspUserLogout -= value; regOnRspUserLogout(rspUserLogout); }
        }
        #endregion

        /// <summary>
        /// 订阅行情
        /// </summary>
        /// <param name="instruments">合约代码:可填多个,订阅所有填null</param>
        public void SubMarketData(params string[] instruments) { subMarketData(instruments, instruments == null ? 0 : instruments.Length); }
        [DllImport(strDllFile, EntryPoint = "?SubMarketData@@YAXQAPADH@Z", CallingConvention = CallingConvention.Cdecl)]
        static extern void subMarketData(string[] instrumentsID, int nCount);
        
        /// <summary>
        /// 退订行情
        /// </summary>
        /// <param name="instruments">合约代码:可填多个,退订所有填null</param>
        public void UnSubMarketData(params string[] instruments) { unSubMarketData(instruments, instruments == null ? 0 : instruments.Length); }
        [DllImport(strDllFile, EntryPoint = "?UnSubscribeMarketData@@YAXQAPADH@Z", CallingConvention = CallingConvention.Cdecl)]
        static extern void unSubMarketData(string[] ppInstrumentID, int nCount);
        #region 订阅行情应答
        [DllImport(strDllFile, EntryPoint = "?RegOnRspSubMarketData@@YGXP6GHPAUCThostFtdcSpecificInstrumentField@@PAUCThostFtdcRspInfoField@@H_N@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRspSubMarketData(RspSubMarketData cb);
        RspSubMarketData rspSubMarketData;
        /// <summary>
        /// 
        /// </summary>
        /// <param name="pSpecificInstrument"></param>
        /// <param name="pRspInfo"></param>
        /// <param name="nRequestID"></param>
        /// <param name="bIsLast"></param>
        public delegate void RspSubMarketData(ref CThostFtdcSpecificInstrumentField pSpecificInstrument, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast);
        /// <summary>
        /// 订阅行情应答
        /// </summary>
        public event RspSubMarketData OnRspSubMarketData
        {
            add { rspSubMarketData += value; regOnRspSubMarketData(rspSubMarketData); }
            remove { rspSubMarketData -= value; regOnRspSubMarketData(rspSubMarketData); }
        }
        #endregion

        #region 退订请求应答
        [DllImport(strDllFile, EntryPoint = "?RegOnRspUnSubMarketData@@YGXP6GHPAUCThostFtdcSpecificInstrumentField@@PAUCThostFtdcRspInfoField@@H_N@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRspUnSubMarketData(RspUnSubMarketData cb);
        RspUnSubMarketData rspUnSubMarketData;
        /// <summary>
        /// 
        /// </summary>
        /// <param name="pSpecificInstrument"></param>
        /// <param name="pRspInfo"></param>
        /// <param name="nRequestID"></param>
        /// <param name="bIsLast"></param>
        public delegate void RspUnSubMarketData(ref CThostFtdcSpecificInstrumentField pSpecificInstrument, ref CThostFtdcRspInfoField pRspInfo, int nRequestID, bool bIsLast);
        /// <summary>
        /// 退订请求应答
        /// </summary>
        public event RspUnSubMarketData OnRspUnSubMarketData
        {
            add { rspUnSubMarketData += value; regOnRspUnSubMarketData(rspUnSubMarketData); }
            remove { rspUnSubMarketData -= value; regOnRspUnSubMarketData(rspUnSubMarketData); }
        }
        #endregion

        #region 深度行情通知
        [DllImport(strDllFile, EntryPoint = "?RegOnRtnDepthMarketData@@YGXP6GHPAUCThostFtdcDepthMarketDataField@@@Z@Z", CallingConvention = CallingConvention.StdCall)]
        static extern void regOnRtnDepthMarketData(RtnDepthMarketData cb);
        RtnDepthMarketData rtnDepthMarketData;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="pDepthMarketData"></param>
        public delegate void RtnDepthMarketData(ref CThostFtdcDepthMarketDataField pDepthMarketData);
        /// <summary>
        /// 深度行情通知
        /// </summary>
        public event RtnDepthMarketData OnRtnDepthMarketData
        {
            add { rtnDepthMarketData += value; regOnRtnDepthMarketData(rtnDepthMarketData); }
            remove { rtnDepthMarketData -= value; regOnRtnDepthMarketData(rtnDepthMarketData); }
        }
        #endregion
    }
}
