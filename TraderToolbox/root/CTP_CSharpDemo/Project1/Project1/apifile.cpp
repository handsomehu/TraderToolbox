#include "stdafx.h"
#include "Project1.h"
#include <iostream>
//#include <vector>		//��̬����,֧�ָ�ֵ
//using namespace std;

#include "../ctpfiles/ThostFtdcMdApi.h"

// UserApi����
CThostFtdcMdApi* pUserApi;

// ������
int iRequestID = 0;

//�ص�����
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
//����
PROJECT1_API void Connect(char* FRONT_ADDR)
{

	CThostFtdcMdSpi* pUserSpi = new CProject1();
	// ��ʼ��UserApi
	pUserApi = CThostFtdcMdApi::CreateFtdcMdApi();			// ����UserApi

	pUserApi->RegisterSpi(pUserSpi);						// ע���¼���
	pUserApi->RegisterFront(FRONT_ADDR);					// connect
	pUserApi->Init();
	//pUserApi->Join();
}
PROJECT1_API void DisConnect()
{
	pUserApi->Release();
}
//��¼
PROJECT1_API void ReqUserLogin(TThostFtdcBrokerIDType BROKER_ID, TThostFtdcInvestorIDType INVESTOR_ID, TThostFtdcPasswordType PASSWORD)
{
	CThostFtdcReqUserLoginField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.UserID, INVESTOR_ID);
	strcpy_s(req.Password, PASSWORD);
	pUserApi->ReqUserLogin(&req, ++iRequestID);
}

///�ǳ�����
PROJECT1_API void ReqUserLogout(TThostFtdcBrokerIDType BROKER_ID, TThostFtdcInvestorIDType INVESTOR_ID)
{
	CThostFtdcUserLogoutField req;
	memset(&req, 0, sizeof(req));
	strcpy_s(req.BrokerID, BROKER_ID);
	strcpy_s(req.UserID, INVESTOR_ID);
	pUserApi->ReqUserLogout(&req, ++iRequestID);
}

//��������
PROJECT1_API void SubMarketData(char* instrumentsID[], int nCount)
{
	pUserApi->SubscribeMarketData(instrumentsID, nCount);
}

PROJECT1_API void WINAPI RegOnRspError(CBOnRspError cb)
{
	cbOnRspError = cb;
}
//����
PROJECT1_API void WINAPI RegOnHeartBeatWarning(CBOnHeartBeatWarning cb)
{
	cbOnHeartBeatWarning = cb;
}

//����Ӧ��
PROJECT1_API void WINAPI RegOnFrontConnected(CBOnFrontConnected cb)
{
	cbOnFrontConnected = cb;
}
//���ӶϿ�
PROJECT1_API void WINAPI RegOnFrontDisconnected(CBOnFrontDisconnected cb)
{
	cbOnFrontDisconnected = cb;
}
//��¼����Ӧ��
PROJECT1_API void WINAPI RegOnRspUserLogin(CBOnRspUserLogin cb)
{
	cbOnRspUserLogin = cb;
}
//�ǳ�����Ӧ��
PROJECT1_API void WINAPI RegOnRspUserLogout(CBOnRspUserLogout cb)
{
	cbOnRspUserLogout = cb;
}

PROJECT1_API void WINAPI RegOnRspSubMarketData(CBOnRspSubMarketData cb)
{
	cbOnRspSubMarketData = cb;
}

//�˶�����Ӧ��
PROJECT1_API void WINAPI RegOnRspUnSubMarketData(CBOnRspUnSubMarketData cb)
{
	cbOnRspUnSubMarketData = cb;
}
//�������֪ͨ
PROJECT1_API void WINAPI RegOnRtnDepthMarketData(CBOnRtnDepthMarketData cb)
{
	cbOnRtnDepthMarketData = cb;
}