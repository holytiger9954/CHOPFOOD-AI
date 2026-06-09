# 허성범 포트폴리오 : 03-1_CHOP AI

## Intro

> CHOPFOOD MES 프로젝트의 AI 예측 기능을 담당하는 머신러닝 서버입니다.
> Python 기반으로 데이터를 학습하고 예측 모델을 생성하여 MES와 연동하였습니다.
>
> ### 역할
>
> > * 품질, 생산, 점검, 재고/입출고 예측 모델 설계
> > * FastAPI 기반 AI 서버 구축
> > * Spring MVC REST API 연동
> > * 머신러닝 모델 학습 및 예측 기능 구현

## CHOP AI

> ### MES 머신러닝 예측 서버
>
> * 개발기간 : 2026.05.26 ~ 2026.06.04
> * 연계 프로젝트 : CHOP FOOD MES
>
> ### 개발 환경
>
> > * Language : Python
> > * IDE : VS Code
> > * 형상관리 : Git, GitHub
> > * OS : Windows 10
>
> ### 기술 스택
>
> > * Machine Learning : Scikit-learn, Pandas, NumPy
> > * Server : FastAPI, Uvicorn
> > * Data Processing : Pandas
> > * Model : RandomForestClassifier
> > * API : REST API
>
> ### 주요 기능
>
> > * 품질 위험도 예측 (LOW / MEDIUM / HIGH)
> > * 생산 지연 위험도 예측
> > * 설비 및 작업장 점검 위험도 예측
> > * 재고 및 입출고 위험도 예측
> > * Spring MVC 시스템과 REST API 연동
>
> ### AI 아키텍쳐
>
> > Oracle DB
> > → Spring MVC
> > → FastAPI
> > → Machine Learning Model (.pkl)
> > → Prediction Result
