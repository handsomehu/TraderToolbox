// Project1.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include "Project1.h"


//// 这是导出变量的一个示例
//PROJECT1_API int nProject1=0;
//
//// 这是导出函数的一个示例。
//PROJECT1_API int fnProject1(void)
//{
//    return 42;
//}

extern CBOnRspError cbOnRspError;
extern CBOnHeartBeatWarning cbOnHeartBeatWarning;

extern CBOnFrontConnected cbOnFrontConnected;
extern CBOnFrontDisconnected cbOnFrontDisconnected;
extern CBOnRspUserLogin cbOnRspUserLogin;
extern CBOnRspUserLogout cbOnRspUserLogout;
extern CBOnRspSubMarketData cbOnRspSubMarketData;
extern CBOnRspUnSubMarketData cbOnRspUnSubMarketData;
extern CBOnRtnDepthMarketData cbOnRtnDepthMarketData;

// 这是已导出类的构造函数。
CProject1::CProject1()
{
    return;
}

void CProject1::OnFrontConnected()
{
	if (cbOnFrontConnected != NULL)
		cbOnFrontConnected();

}

void CProject1::OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	if (cbOnRspError != NULL)
		cbOnRspError(pRspInfo, nRequestID, bIsLast);
}

void CProject1::OnFrontDisconnected(int nReason)
{
	//cerr << "--->>> " << __FUNCTION__ << endl;
	//cerr << "--->>> Reason = " << nReason << endl;
	if (cbOnFrontDisconnected != NULL)
		cbOnFrontDisconnected(nReason);
}

void CProject1::OnHeartBeatWarning(int nTimeLapse)
{
	if (cbOnHeartBeatWarning != NULL)
		cbOnHeartBeatWarning(nTimeLapse);
}

void CProject1::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin,
	CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	if (cbOnRspUserLogin != NULL)
		cbOnRspUserLogin(pRspUserLogin, pRspInfo, nRequestID, bIsLast);
}

void CProject1::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	if (cbOnRspUserLogout != NULL)
		cbOnRspUserLogout(pUserLogout, pRspInfo, nRequestID, bIsLast);
}

void CProject1::OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	//cerr << __FUNCTION__ << endl;
	if (cbOnRspSubMarketData != NULL)
		cbOnRspSubMarketData(pSpecificInstrument, pRspInfo, nRequestID, bIsLast);
}

void CProject1::OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	//cerr << __FUNCTION__ << endl;
	if (cbOnRspUnSubMarketData != NULL)
		cbOnRspUnSubMarketData(pSpecificInstrument, pRspInfo, nRequestID, bIsLast);
}

void CProject1::OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData)
{
	//cerr << "深度行情" << endl;
	if (cbOnRtnDepthMarketData != NULL)
		cbOnRtnDepthMarketData(pDepthMarketData);
}
