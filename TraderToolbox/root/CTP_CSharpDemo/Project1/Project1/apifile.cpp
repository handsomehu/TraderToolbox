#include "stdafx.h"
#include "Project1.h"
#include <iostream>
//#include <vector>		//动态数组,支持赋值
//using namespace std;

#include "../ctpfiles/ThostFtdcMdApi.h"

// UserApi对象
CThostFtdcMdApi* pUserApi;

// 请求编号
int iRequestID = 0;

//回调函数
CBOnRspError cbOnRspError = 0;
CBOnHeartBeatWarning cbOnHeartBeatWarning = 0;

CBOnFrontConnected cbOnFrontConnected = 0;
CBOnFrontDisconnected cbOnFrontDisconnected = 0;
CBOnRspUserLogin cbOnRspUserLogin = 0;
CBOnRspUserLogout cbOnRspUserLogout = 0;
CBOnRspSubMarketData cbOnRspSubMarketData = 0;
CBOnRspUnSubMarketData cbOnRspUnSubMarketData = 0;
CBOnRtnDepthMarketData cbOnRtnDepthMarketData = 0;

PROJECT1_API void ReqConnect()
{

}
//连接
PROJECT1_API void Connect(char* FRONT_ADDR)
{

	CThostFtdcMdSpi* pUserSpi = new CProject1();
	// 初始化UserApi
	pUserApi = CThostFtdcMdApi::CreateFtdcMdApi();			// 创建UserApi

	pUserApi->RegisterSpi(pUserSpi);						// 注册事件类
	pUserApi->RegisterFront(FRONT_ADDR);					// connect
	pUserApi->Init();
	//pUserApi->Join();
}
PROJECT1_API void DisConnect()
{
	pUserApi->Release();
}
//登录
PROJECT1_API void ReqUserLogin(TThostFtdcBrokerIDType BROKER_ID, TThostFtdcInvestorIDType INVESTOR_ID, TThostFtdcPasswordType PASSWORD)
{
	CThostFtdcReqUserLoginField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.UserID, INVESTOR_ID);
	strcpy_s(req.Password, PASSWORD);
	pUserApi->ReqUserLogin(&req, ++iRequestID);
}

///登出请求
PROJECT1_API void ReqUserLogout(TThostFtdcBrokerIDType BROKER_ID, TThostFtdcInvestorIDType INVESTOR_ID)
{
	CThostFtdcUserLogoutField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.UserID, INVESTOR_ID);
	pUserApi->ReqUserLogout(&req, ++iRequestID);
}

//订阅行情
PROJECT1_API void SubMarketData(char* instrumentsID[], int nCount)
{
	pUserApi->SubscribeMarketData(instrumentsID, nCount);
}

PROJECT1_API void WINAPI RegOnRspError(CBOnRspError cb)
{
	cbOnRspError = cb;
}
//心跳
PROJECT1_API void WINAPI RegOnHeartBeatWarning(CBOnHeartBeatWarning cb)
{
	cbOnHeartBeatWarning = cb;
}

//连接应答
PROJECT1_API void WINAPI RegOnFrontConnected(CBOnFrontConnected cb)
{
	cbOnFrontConnected = cb;
}
//连接断开
PROJECT1_API void WINAPI RegOnFrontDisconnected(CBOnFrontDisconnected cb)
{
	cbOnFrontDisconnected = cb;
}
//登录请求应答
PROJECT1_API void WINAPI RegOnRspUserLogin(CBOnRspUserLogin cb)
{
	cbOnRspUserLogin = cb;
}
//登出请求应答
PROJECT1_API void WINAPI RegOnRspUserLogout(CBOnRspUserLogout cb)
{
	cbOnRspUserLogout = cb;
}

PROJECT1_API void WINAPI RegOnRspSubMarketData(CBOnRspSubMarketData cb)
{
	cbOnRspSubMarketData = cb;
}

//退订行情应答
PROJECT1_API void WINAPI RegOnRspUnSubMarketData(CBOnRspUnSubMarketData cb)
{
	cbOnRspUnSubMarketData = cb;
}
//深度行情通知
PROJECT1_API void WINAPI RegOnRtnDepthMarketData(CBOnRtnDepthMarketData cb)
{
	cbOnRtnDepthMarketData = cb;
}