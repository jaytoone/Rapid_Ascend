## EMA RIBBON

| MODEL_NUM         | DESCRIPTION                                                  | RESULT                                                       |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| _65               | ema_ribbon                                                   | 잔 거래가 너무 많다..                                        |
| _66               | ema_cross                                                    | 97% -> 고점이 아닌 것을 예측을 잘해서 높게 나오는거임..      |
| _67               | 장기 / 단기 상승의 구분                                      | 60 %..                                                       |
| 100_68            | ema_cross_long , idl =100                                    | 안좋아짐..                                                   |
| 30_69             | ema_cross -> price 데이터만 사용                             | candle 보다 none candle 이 나은거 같다..                     |
| 30_70             | ema_cross_long -> price 데이터만 사용 figure_size=(1, 1)     |                                                              |
| 30_71             | ema_cross_long -> rsi 사용해도 좋을듯하다                    |                                                              |
| 30_72             | ema_cross -> 한개의 고점만 만들지 말고 최고점 기준으로 이전 이후 데이터로 분리해본다. | 고점이 아닌 곳도 고점으로 잡아버리는 불상사                  |
| 30_73             | ema_cross_long -> 캔들 차트 말고 내가 원래 하던 모양도 고려해보기, 이때 ema 와 price 스케일링 조심하기 | 61.16 %..                                                    |
| 30_74             | 30_73 model 을 차트 모델로 돌려보기                          | cmo : 0.64641                                                |
| 30_75             | ema_cross_no_candle -> CROSSOVER부터 CROSSUNDER 내에서 고점과 아닌 데이터셋 만들어주기 | data에 문제가 있는거 같음 -> 고점, 저점, 거래안함으로 나누어야하나 |
| _76               | ema_cross -> crop_span내에서 한개의 고점                     | **no_candle 이 훨 좋음! argmax()로 했을때 고점이 좀 더 일찍 잡힌다. 가장 높은 고점을 노리는 방법 없을까** 분산이 높다 |
| _77               | ema_cross_long_no_candle -> long_short 만 하지말고, 전체적으로 한다음에 거기서 long만 표시해주면? | **dataset을 어떻게 꾸리냐가 중요함! 아무래도 long이 아닌 데이터가 너무 많아서 0이 많아진거 같다** 30_73 cmo 가 더 좋음.. |
| _78               | macd 으로 고점 찾기                                          |                                                              |
| _79               | dataset 은 none_crop                                         | no_candle 버려.. 시간 아깝다.                                |
| _80               | MACD 가 0 선 기준으로 CROSSOVER 부터 CROSSUNDER 까지의 기간중에서 최고점 뒤로는 1 아니면 0, | 고점표시가 안된다..                                          |
| _81               | MACD를 사용해서 _57과 같이 라벨링                            | 음.. 아마 데이터셋을 잘못만든거 같음..                       |
| _82               | MACD도 CROP 전 스케일링이 맞다. 그렇게 따지면 OBV도          |                                                              |
| _83               | MACD 라벨링, 양의 MACD 구간에서만 _57 OHLC 라벨링과 동일하게, CHECK_SPAN=10 | **나쁘지 않은데 좀 더 첨예하게 할 수 없을까?**               |
| _84               | MACD 라벨, CROP_SPAN 구간에서 최대 MACD == 1 ELSE 0          | **어느정도 잘 나오는거 같음 -> 괜찮은 거 같은데..?** >> nan 값이 나오는 이유는 ? <u>데이터셋에서 cmo, rsi, macd setting 잘못됨</u> **정확도가 올라가면 첨예해지지만, 분산이 낮아진다.** ** |
| _85               | _84 에서 최대 MACD 이전으로 0                                | 생각대로 나오지 않는결과..                                   |
| _86               | _84 데이터셋 세팅 고친 버전                                  | 84 > 86                                                      |
| _87               | MACD_OSC 5 8 5 -> TRADE_STATE [0, 1, 2, 3]                   | 88 보다 plus_profit이 더 좋긴함..                            |
| _88               | MACD_OSC 5 8 5 -> TRADE_STATE [0, 1]                         |                                                              |
| _89               | MACD_OSC 20 33 5 -> TRADE_STATE 0123 + MA20 지워버림         | **4개의 라벨링으로 다양한 고점을 수용할 수 있음**            |
|                   | 3퍼센트 정확도 오른거 거기서 거기..                          |                                                              |
| _90               | _89 버전 TRADE_STATE 01                                      | **Best Fit! 최고점을 잘 잡는데 생략되는 봉들이 많다**        |
|                   | _90 버전 MACD에 CROP_SCALING 먹이기                          | 정확도 대폭 떨어진다..                                       |
| _91               | _89 데이터 160만                                             | **_90 만큼의 정확도, 생략되는 봉들이 많다**                  |
|                   | _89 데이터 80만                                              | **160만 데이터보다 생략되는 봉들이 적다**                    |
| _92               | _90 데이터 80만                                              | 생략되는 봉들이 더 많아진다.                                 |
| _93               | _90 데이터 5만                                               | 생략되는 봉이 많다.                                          |
|                   | 데이터셋 정의를 바꾸어보는건 어떨까                          |                                                              |
| _94               | _89 데이터셋 변경 : 구간내 종가 최고점으로                   | 고점이 거의 사라짐..                                         |
| _95               | _89 데이터셋 변경 : MACD 고점이후로 CROSSUNDER 까지 1 ELSE 0 | 고점이 거의 사라짐..                                         |
| _96               | _90 데이터셋 변경 : 구간내 종가 최고점으로                   |                                                              |
| _97               | _90 데이터셋 변경 : MACD 고점이후로 CROSSUNDER 까지 1 ELSE 0 |                                                              |
| _98               | MACD_ONLY 로 고점 라벨링 (구간내 최고점 MACD)                |                                                              |
| **쓸만한 데이터** | **84_rsimacd, 90_macdonly**                                  |                                                              |



## WORK TO DO

**내가 원하는 결과 : **

1. **라벨링된 Y 값(=MACD_OSC 최고점)을 가장 정확하게 맞히는 방법**

   | 지표별   | 특징                                                         |
   | -------- | ------------------------------------------------------------ |
   | fillmode | 무관하다고 보면..                                            |
   | ohlc     | 성급한 고점, ohlc 개별적으로 사용해도 동일한 효과 = **결국 어떠한 지표가 섞여서 결과가 다른 방향으로 흐르면 그게 그 지표의 성격이다** |
   | macdonly | 첨예하게 고점을 선택한다. 하지만 다양한 고점을 예측하지는 못함 (어느정도 높은 고점만) |
   | signal   | CROSSOVER 시작부터 고점;                                     |
   | osc      | <u>기준</u>                                                  |
   | cmo      | 성급한 고점                                                  |
   | rsi      | 성급한 고점 + 분산이 심하다.                                 |
   | obv      | 최종 고점보다 서둘러 예측                                    |
   | zero     | 무관하다고 보면 된다.                                        |
   | volume   | 고점보단 CROSSOVER, CROSSUNDER를 고점으로 인식               |

   * **정말로 최종 고점을 잡기 힘들다면 자잘한 고점이 없는 히스토그램을 이용하면 된다. 그거는 고점 잡기 편하니까**
   * 고점잡기 편한 데이터란? 최고점의 높이가 비슷한 것들
   * CNN 말고 RNN으로 해보기

2. 손해 볼 진입을 거르는 방법







## MODIFICATION

* 데이터 스케일링
  
  * none_crop price 가 결과값이 더 좋으니, 모든 데이터를 crop전 리스케일한다.
  * 0 기준선이 없으면, 예측할때 crop 한다. (price, ma <=> obv 는 변화폭에 민감함으로 예외)
  
  

### STRATEGY

#### 급상승을 예고하는 저점 + 고점전략 먼저 모델 나중

---

| 진입                                                         | 매수                                                        | 매도                     | 이탈 |
| ------------------------------------------------------------ | ----------------------------------------------------------- | ------------------------ | ---- |
| EMA_CROSS 이전 진입 - 빠른 진입이 중요, 잔거래는 거를 수 있어야한다. |                                                             | 가장 높은 MACD 매도      |      |
| 급상승을 예측하고, 급상승 타면, 고점에 매각                  |                                                             |                          |      |
| 상향 추세에서 저점                                           |                                                             | 고점                     |      |
| **MACD_OSC의 CROSSOVER 진입** 좀 더 빠르게 세팅 -> 급상승과 아닌 진입 구분하기 -> <u>Setting : 20 33 5</u> | 55초 이후에 MACD_OSC 의 CROSSOVER가 결정되면, 현재가로 진입 | **MACD_OSC 최고점 매도** |      |
| -                                                            | -                                                           | MACD의 최고점으로 매도   |      |

완성된 데이터를 사용할건지, 완성될 데이터를 사용할건지



## REFERENCE

Ribbon :  https://www.investopedia.com/articles/active-trading/012815/top-technical-indicators-scalping-trading-strategy.asp