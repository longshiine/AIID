<img width="782" alt="스크린샷 2021-05-28 오후 5 55 55" src="https://user-images.githubusercontent.com/70363646/119958385-f68c4e80-bfdd-11eb-9ecd-72494919b5d7.png">

# 복합인지 실종예측 모델 연구 (AIID)
### Advanced Integrated Intelligence for Identification  

## 1. 연구 목적 및 방향성

a) 기존 목표

기존에 연구의 목표 및 방향성은 영상에서 추출된 텍스트 기반 이벤트 데이터를 입력 받아 실종위험 예측 및 위험 상황을 인지하는 것이었다. LSTM 모델을 기반으로, 추가적으로 과거 실종 사건 데이터를 모델 훈련에 활용하는 방향 또한 목표하였다. 결과적으로 과거 사건과 현재 이벤트를 기준으로 실종 위험 예측을 하는 것이다.

b) 변경 목표

연구를 진행함에 따라, 주어진 데이터로 목표한 모델을 구축하는 것이 사실상 불가능하다는 결론에 다다랐다. LSTM 모델을 학습시키기 위해선 영상에서 추출된 텍스트 기반 이벤트 데이터(xml파일)와 함께 해당 이벤트가 실제 실종 사건 발생으로 이어졌는지 그 여부에 대한 정보가 필요한데, 해당 정보 확보가 불가능했다. 따라서 과거 실종 데이터만으로 예측 모델을 구축하는 방향으로 선회하였고, 과거 실종 데이터를 적절히 가공하여 이를 기반으로 다양한 예측 모델을 구축하고 그 성능을 평가하였다.

## 2. 데이터 전처리

'20191118_복합인지기술_실종 주소 관련.xlsb'를 가장 원본 데이터로 삼아, 몇가지 데이터 선별 및 전처리 과정을 거쳤다.

### 1차 가공

실종 접수와 발생 일시의 차이가 너무 크게 벌어질 경우(예를 들어 2000년에 접수한 1950년의 실종은 무려 접수와 발생 날짜의 차이가 50년이 된다), 발생 일시 및 상황에 대한 정보가 불확실할 수 있기 때문에 이를 고려하여 발생 일시가 2015년 전인 데이터는 제외하였다.

### 2차 가공

OpenAPI를 활용하여 기상 정보(기온(C), 강수량(mm), 풍속(m/s), 습도(%), 일조(hr), 일사(MJ/m2))와 주소를 좌표화시킨 정보를 추가하였다. 좌표화된 주소 정보는 본 연구에서 쓰이진 않았지만, 추후 활용될 수 있음을 감안하여 확보한 정보를 유지하였다. 2차 가공 과정에서 발생 장소에 대한 정보가 모호한 데이터(예를 들어 '서울'이라고만 나온 경우)가 제외되었다.

두 차례의 가공을 통해 얻은 데이터셋은 이후 각 모델에 따라 필요한 추가적인 전처리 과정을 거쳐 학습에 활용되었다.

## 3. Basic Model (RF, DNN)

LSTM 모델을 구축하기 전, RandomForest(이하 'RF') 모델과 단순한 구조의 Deep Neural Network(이하 'DNN') 모델을 구축하고 그 성능을 평가하였다.

RF와 DNN 모두 특정 지역(동)에 대하여, 월, 요일, 기상 정보(기온(C), 강수량(mm), 풍속(m/s), 습도(%), 일조(hr), 일사(MJ/m2))를 input으로 넣었을 때 실종 발생 시간(시간 단위)을 output으로 주는 패러다임으로 모델을 구축하였다. 실종 사건이 발생한 케이스에 대한 데이터만으로 학습하기에, 주어진 일자에 실종 사건이 발생한다는 전제 조건 하에 언제(어느 시간에) 발생할지를 예측하는 모델들이다.

RF와 DNN의 성능을 평가하기 위해 데이터셋을 training set와 evaluation set로 나누기엔 데이터의 양이 부족하여, 10-fold cross evaluation을 통한 평균 accuracy 값들을 실종 사건 수가 가장 많은 13개 동의 데이터에 대해 구하였다:
<img width="687" alt="스크린샷 2021-05-28 오후 5 45 01" src="https://user-images.githubusercontent.com/70363646/119956830-74e7f100-bfdc-11eb-970a-e41733696c31.png">


13개 동에 대해 평균적으로 RF는 26.57%, DNN은 16.18%의 accuracy를 보였으며, 이는 모두 24시간 중 한 시간을 임의로 고르는 4.17%보다 높았다.

## 4. LSTM Autoencoder for Anomaly Detection

데이터 전처리 과정을 거쳐 기존의 Task를 Anomaly Detection Task로 변형하고, 이에 대해 LSTM AutoEncoder 모델을 적용해보았다.

### Intro

LSTM Autoencoder를 통해 Anomaly Detection하는 방법을 적용했다. Autoencoder의 경우 보통 이미지의 생성이나 복원에 많이 사용되며 이러한 구조를 이어받아 대표적인 딥러닝 생성 모델인 GAN(Generative Adversarial Network)으로 까지 이어졌는데 이러한 자기 학습 모델은 Anomaly Detection 분야에서도 널리 사용되고 있다.

대표적으로 이미지 분야에서도 정상적인 이미지로 모델 학습 후 비정상적인 이미지를 넣어 이를 디코딩 하게 되면 정상 이미지 특성과 디코딩 된 이미지 간의 차이인 재구성 손실(Reconstruction Error)를 계산하게 되는데 이 재구성 손실이 낮은 부분은 정상(normal), 재구성 손실이 높은 부분은 이상(Abnormal)로 판단할 수 있다.

이러한 Anomaly Detection은 이미지 뿐만 아니라 이제부터 살펴보고자 하는 시계열 데이터에도 적용이 가능하다. 예를 들어 특정 설비의 센서를 통해 비정상 신호를 탐지하고자 한다면 Autoencoder를 LSTM 레이어로 구성한다면 이러한 시퀀스 학습이 가능하게 된다. 이를 통해 정상 신호만을 이용하여 모델을 학습시켜 추후 비정상 신호가 모델에 입력되면 높은 reconstruction error를 나타낼 것이므로 이를 비정상 신호로 판단할 수 있게 된다.
![스크린샷 2021-05-28 오후 5 45 29](https://user-images.githubusercontent.com/70363646/119956889-829d7680-bfdc-11eb-95ec-44050348cd9b.png)


LSTM Autoencoder는 시퀀스(sequence) 데이터에 Encoder-Decoder LSTM 아키텍처를 적용하여 구현한 오토인코더이다. 모델에 입력 시퀀스가 순차적으로 들어오게 되고, 마지막 입력 시퀀스가 들어온 후 디코더는 입력 시퀀스를 재생성하거나 혹은 목표 시퀀스에 대한 예측을 출력한다.

위에서 설명한 것과 마찬가지로

**LSTM Autoencoder 학습 시에는 정상(normal) 신호의 데이터로만 모델을 학습시키게 된다.**

encoder와 decoder는 학습이 진행될 수 록 정상 신호를 더 정상 신호 답게 표현하는 방법을 학습하게 될 것이며 최종적으로 재구성 한 결과도 정상 신호와 매우 유사한 분포를 가지는 데이터일 것이다. 그렇기 때문에 이 모델에 비정상 신호를 입력으로 넣게 되면 정상 분포와 다른 특성의 분포를 나타낼 것이기 때문에 높은 reconstruction error를 보이게 될 것이다.

### Curve Shifting을 적용한 LSTM Autoencoder
<img width="662" alt="스크린샷 2021-05-28 오후 5 46 52" src="https://user-images.githubusercontent.com/70363646/119957063-b5e00580-bfdc-11eb-8adf-e7808e495b3c.png">

전체 프로세스는 위 아키텍처와 같다. 먼저 Curve Shifting을 통해 데이터의 시점을 변환해주고 normal 데이터만을 통해 LSTM Autoencoder 모델을 학습시키게 된다. 그 후 재구성 손실을 계산 후 Precision Recall Curve를 통해 normal/abnormal을 구분하기 위한 threshold를 지정하게 되고 이 threshold를 기준으로 마지막으로 테스트 셋의 재구성 손실을 분류하여 t+n 시점을 예측하게 된다.각 부분에 대해 아래에서 좀 더 상세히 살펴보자.

### 1. Curve Shifting

비정상 신호를 탐지하기 위해서는 비정상 신호가 들어오기 전에 즉, 뭔가 고장 혹은 결함이 발생하기 전에 미리 예측을 해야만 한다. 그렇기 때문에 단순히 현재 시점의 error를 계산하여 비정상 신호를 탐지하는 것은 이미 고장이 발생한 후 예측하는 것과 다름이 없기 때문에 **데이터에 대한 시점 변환**이 꼭 필요하다.

이러한 future value 예측을 위해 다양한 방법이 있는데 여기서는 **Curve Shifting**이라는 기법을 적용할 것이다.
<img width="350" alt="스크린샷 2021-05-28 오후 5 47 13" src="https://user-images.githubusercontent.com/70363646/119957115-c1333100-bfdc-11eb-9d9b-5a0a96972729.png">

Curve Shifting은 **사전 예측 개념**을 적용하기 위한 Shifting 방법이다. 예를 들어 위 그림과 같이 비정상 신호(1)를 2일 전에 조기 예측 하고자 한다면 단순히 Y값을 두 칸씩 내리는 것이 아니라 비정상 신호(1)가 있는 날짜로부터 2일 전까지의 데이터를 비정상 신호(1)로 바꾸어주는 것이다. 이는 비정상 신호가 발생하기 전 어떠한 조짐이 있을 것이며 이러한 조짐이 데이터 특성에 나타날 것이라는 가정을 가지고 학습하는 방법이다.그리고 나서 본래 비정상 신호(1) 데이터를 제거해주는데 이렇게 하는 이유는 라벨을 바꿔주는 순간 이는 비정상 신호 예측 문제가 아닌 비정상 신호 조짐 예측 문제가 되는 것이 때문에 데이터의 학습 혼동을 없애주기 위해 제거하는 것이라 보면 될 것이다.

### 2. Threshold by Precision-Recall-Curve

Autoencoder는 재구성 된 결과를 intput과 비교하여 재구성 손실(Reconstruction Error)를 계산한다고 말했다. 그리고 이 재구성 손실값을 통해 손실값이 낮으면 정상으로, 손실값이 높으면 이상으로 판단한다고 하였는데, 이 정상과 이상을 나누는 기준은 과연 무엇일까?일반적으로 모델이 정상 데이터만으로 학습을 하여 정상 데이터를 재구성하였을 때 학습이 잘 되었다고 가정하면 손실값은 0에 가까울 것이고, 학습이 잘 안되었다고 하면 손실값은 1에 가까울 것이다. 보통 분류(Classification)문제에서는 예측 확률값(0% ~ 100%)을 통해 50%를 기준으로 분류를 하게 되는데, 이 recontruction error의 경우 그렇게 극단적으로 값이 튀기는 힘들기 때문에 정상과 이상을 분리하는 타당한 threshold값을 정하는 것이 필요하다.
<img width="563" alt="스크린샷 2021-05-28 오후 5 47 35" src="https://user-images.githubusercontent.com/70363646/119957158-cb552f80-bfdc-11eb-8dd2-f082febd9fea.png">

위와 같은 문제의 적절한 threshold값을 적용하기 위한 방법 중 하나로 precision recall curve가 있다. 이는 Recall(재현율)과 Precision(정밀도)가 서로 Trade off 관계를 가지기 때문에 어느 한쪽에 치우지지 않는 최적의 threshold를 구하기 위한 방법이다.추후 이 검증 기법을 적용하여 LSTM Autoencoder를 통해 재구성 된 정상 신호와 비정상 신호를 구분하기 위한 적절한 threshold를 찾아낼 것이다.

## Implementation

### Task

시간에 따른 기상 데이터가 추가된 5년치 실시간 실종 데이터에서 실제 실종을 예측해볼 것이다.

이는 사실상 날씨만 가지고 실종을 예측하는 task이다.

<img width="702" alt="스크린샷 2021-05-28 오후 5 47 47" src="https://user-images.githubusercontent.com/70363646/119957217-d7d98800-bfdc-11eb-9439-bde0961bd7a0.png">

<img width="512" alt="스크린샷 2021-05-28 오후 5 48 22" src="https://user-images.githubusercontent.com/70363646/119957310-ef187580-bfdc-11eb-9730-50455009fd89.png">

<img width="471" alt="스크린샷 2021-05-28 오후 5 48 26" src="https://user-images.githubusercontent.com/70363646/119957340-f475c000-bfdc-11eb-9dac-6db998bb7ec9.png">

<img width="458" alt="스크린샷 2021-05-28 오후 5 48 31" src="https://user-images.githubusercontent.com/70363646/119957353-f8094700-bfdc-11eb-81f7-360fbd4075de.png">

예측 dimension이 너무 낮아서 threshold값이 제대로 추정이 안된다. (현재 기상 정보만으로 예측을 하기 때문)

<img width="466" alt="스크린샷 2021-05-28 오후 5 49 06" src="https://user-images.githubusercontent.com/70363646/119957429-08212680-bfdd-11eb-8af1-529cae70157f.png">

<img width="468" alt="스크린샷 2021-05-28 오후 5 49 11" src="https://user-images.githubusercontent.com/70363646/119957442-09eaea00-bfdd-11eb-8ed9-af4e9b4a6227.png">


현재 8685개의 Test set(391개의 anomal)에 대해 정상은 7925개를 맞추고, 비정상은 18개를 맞췄다.

<img width="678" alt="스크린샷 2021-05-28 오후 5 49 35" src="https://user-images.githubusercontent.com/70363646/119957505-1707d900-bfdd-11eb-8a58-c5d42755f94b.png">


실종이 일어나지 않은 무수한 케이스 + 실종에서 5% 정도로 실제 실종을 알아내고 있다. 이상행동과 같은 실시간 데이터가 추가된다면 **"실시간 실종 예측률"**이 올라갈 것으로 보인다.  현재는 오로지 실시간 기상 데이터만으로 실종을 예측하고 있다.

**실시간 데이터의 추가적인 column 확보가 필요하다**

## 5. 지도 마킹

- 지도 마킹의 경우 Kakao map API 와 React를 이용해 구현하였다.
- 원래 구현 목표: 실시간으로 제공되는 동별 위험도를 지도에 Mapping
- 한계점: 실시간으로 제공되는  영상 기반 이벤트 데이터를 DNN 혹은 LSTM 등으로 처리 후, 지도 위에 매핑하는 것이 목표였으나, 가용한 데이터가 과거의 실종 데이터 뿐이었기에, 목표를 수정함
- 수정된 목표:
    1. 과거의 실종을 통계적으로 분석하여, 각 구별 위험도를 상대적으로 분석하고, 이를 지도상에 다른 색의 polygon으로 layering (진할 수록 위험도 up)
    2. 최근에 일어난 실종 사건의 경우 마커를 이용해 지도 상에 마킹하고, 일정한 기준에 따라 clustering하여 빈도의 시각화 및 UX 개선

    ## 구현 화면
    **<1. 마킹 및 클러스터링>**  
    <img width="401" alt="스크린샷 2021-05-28 오후 5 50 49" src="https://user-images.githubusercontent.com/70363646/119957709-4a4a6800-bfdd-11eb-8251-6bad13b9afe1.png">

    **< 2. Relative 위험도 폴리곤>**                         
    <img width="404" alt="스크린샷 2021-05-28 오후 5 50 55" src="https://user-images.githubusercontent.com/70363646/119957723-4d455880-bfdd-11eb-8372-fa3696bc0d94.png">

    <img width="410" alt="스크린샷 2021-05-28 오후 5 51 01" src="https://user-images.githubusercontent.com/70363646/119957747-546c6680-bfdd-11eb-88c3-57df1d89537c.png">


- 의의:
1. 추후 데이터가 업데이트 될시 응용 가능한 위험도 매핑 매커니즘.
2. 실시간 데이터 부분만 수정하여 마킹 가능

## 6. 논의

본 연구는 본래 영상에서 추출된 텍스트 기반 이벤트 데이터를 입력 받아 실종위험 예측 및 위험 상황을 인지하는 것을 목표로 하였으나, 해당 패러다임을 모델에 적용시키기 위한 데이터가 부족하여 과거 실종 사건의 발생 일시와 발생 당시의 기상 정보로 실종을 예측하는 모델을 구축하였다.

LSTM 모델 단독으로 발생 일시와 시간까지 예측하는 것이 가장 이상적이겠지만, 현재는 특정한 날짜와 이 날짜의 기상 정보가 주어졌을 때 해당 일자에 실종 사건이 일어날지 여부만을 예측한다. 따라서 이를 보완하기 위해 basic model로 제시한 RF 혹은 DNN 모델을 활용하는 것이 가능하다. RF와 DNN 모델은 실종 사건이 발생한다는 가정 하에 몇 시에 사건이 발생할지 예측하기 때문에, LSTM 모델의 예측으로 특정 일에 실종 사건 발생이 예상되면 RF나 DNN 모델을 통해 몇 시에 일어날지 예측할 수 있다.

현재 주어진 데이터를 통한 학습의 결과 RF 모델이 DNN 모델보다 더욱 우수한 성능을 보이는데, 이는 더욱 풍부한 데이터셋이 주어진다면 성능이 역전할 가능성이 존재한다. 현재 DNN 모델은 적은 양의 training dataset을 통해 유의미한 학습을 하기 위해 의도적으로 overfitting하게 모델과 hyperparameter들이 설계되었다. 만약 충분한 데이터셋이 주어진다면, 이에 따라 DNN 모델을 수정할 여지가 생겨 DNN 모델이 더 우수한 성능을 낼 수도 있다.

본 연구에서 제시한 모델들은 앞서 언급한 바와 같이 실종 사건의 시간 및 날짜 정보와 기상 정보를 기반으로 실종을 예측하는데, 발생 당일에 대학수학능력평가와 같은 국가적 혹은 지역적 차원에서 실시되는 연례 행사가 실시되었는지 조사하여 이를 하나의 새로운 feature로서 활용해 모델의 성능을 향상시키는 방안도 검토하면 좋을 것이다.

데이터 전처리 과정에서 주소를 xy좌표로 변환한 데이터를 추가하였는데, 추후 연구에서 이 위치적 정보를 기준으로 데이터셋을 나누어 학습시키면 어떤 양상의 결과가 도출되는지 보는 것도 유의미할 것이다. 본 연구에선 '동/읍/면'을 기준으로 데이터를 나누어 각 지역별 모델을 얻을 수 있는 패러다임으로 모델을 구축하였으나, xy좌표 데이터를 활용한다면 일정한 xy좌표 범위에 따른 그리드(grid)를 설정하여 그리드별 실종 예측 모델을 얻을 수 있을 것이다.

## 7. Appendix
<img width="536" alt="스크린샷 2021-05-28 오후 5 56 49" src="https://user-images.githubusercontent.com/70363646/119958536-1754a400-bfde-11eb-8873-e1d1981970b7.png">
