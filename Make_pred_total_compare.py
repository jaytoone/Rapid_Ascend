import numpy as np
import pandas as pd
from keras.models import load_model
from matplotlib import pyplot as plt
import os
from Make_X_total import made_x
from keras.utils import np_utils
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


home_dir = os.path.expanduser('~')
dir = home_dir + '/OneDrive/CoinBot/ohlcv/'
ohlcv_list = os.listdir(dir)

if __name__ == '__main__':

    #           PARAMS           #
    input_data_length = 30
    model_number = '57'
    model_name_list = list()
    for file in os.listdir('./model'):
        if file.find(model_number) is not -1:  # 해당 파일이면 temp[i] 에 넣겠다.
            model_name_list.append(file)
    # print(model_list)
    # print('macd' in model_list[1])
    # quit()

    crop_size = input_data_length     # 이전 저점까지 slicing
    crop_size2 = input_data_length
    # limit_line = 0.97    # 다음 저점을 고르기 위한 limit_line
    # limit_line2 = 0.8
    # sudden_death = 0
    # sudden_death2 = 0
    check_span = 30
    get_fig = 1

    #       Make folder      #
    try:
        os.mkdir('./pred_ohlcv/%s_%s/' % (input_data_length, model_number))
    except Exception as e:
        pass

    try:
        os.mkdir('./Figure_pred/%s_%s/' % (input_data_length, model_number))
    except Exception as e:
        pass

    except_list = os.listdir('./pred_ohlcv/%s_%s' % (input_data_length, model_number))

    # ohlcv_list = ['2019-10-09 ZRX ohlcv.xlsx']

    #       LOAD MODEL      #
    model_list = list()
    for model_name in model_name_list:
        print('load model %s' % model_name)
        model_list.append(load_model('./model/%s' % model_name))
    print()

    for file in ohlcv_list:

        #         if file in except_list:
        #             continue

        print('loading %s' % file)

        try:
            X_test, _, sliced_ohlc = made_x(file, input_data_length, model_number, check_span, 0, crop_size=crop_size)
            # X_test2, _, sliced_ohlc2 = made_x(file, input_data_length, model_num, check_span, 0, crop_size=crop_size2)
            # X_test, _ = low_high(Coin, input_data_length, sudden_death=1.)
            # closeprice = np.roll(np.array(list(map(lambda x: x[-1][[1]][0], X_test))), -1)
            # print(X_test)
            X_test = np.array(X_test)
            # X_test2 = np.array(X_test2)
            row = X_test.shape[1]
            col = X_test.shape[2]
            # col2 = X_test2.shape[2]

            X_test = X_test.astype('float32').reshape(-1, row, col, 1)
            # X_test2 = X_test2.astype('float32').reshape(-1, row, col2, 1)

        except Exception as e:
            print('Error in getting data from made_x :', e)
            continue

        # OBV = np.roll(np.array(list(map(lambda x: x[-1][[5]][0], X_test))), -1)

        # dataX 에 담겨있는 value 에 [-1] : 바로 이전의 행 x[-1][:].shape = (1, 6)
        # sliced_ohlcv = np.array(list(map(lambda x: x[-1][:], X_test)))
        # print(sliced_ohlcv)
        # quit()

        if X_test is not None:
            if len(X_test) != 0:

                fig_cnt = 1
                for model_name in model_name_list:

                    if 'ohlc' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3]]
                    elif 'volume' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 4]]
                    elif 'ma20' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 5]]
                    elif 'cmo' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 6]]
                    elif 'obv' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 7]]
                    elif 'rsi' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 8]]
                    elif 'macd' in model_name:
                        X_test_resize = X_test[:, :, [0, 1, 2, 3, 9, 10, 11]]

                    # print(model_name)

                    Y_pred_ = model_list[fig_cnt - 1].predict(X_test_resize, verbose=1)
                    # Y_pred2_ = model.predict(X_test2, verbose=1)

                    # value_rank = pd.Series(Y_pred_[:, 1]).sort_values(ascending=False).index[:300]
                    # print(Y_pred2_[:, [2]])
                    # quit()
                    # print(value_rank)
                    # quit()

                    # max_value = np.max(Y_pred_, axis=0)
                    # print(max_value)
                    # max_value2 = np.max(Y_pred2_, axis=0)
                    Y_pred = np.argmax(Y_pred_, axis=1)
                    # Y_pred2 = np.argmax(Y_pred2_, axis=1)
                    # Y_pred = np.zeros(len(Y_pred_))
                    # # Y_pred2 = np.zeros(len(Y_pred2_))
                    # for i in range(len(Y_pred_)):
                    #     if Y_pred_[i][1] > 0.4:
                    #         Y_pred[i] = 1
                    #     elif Y_pred_[i][2] > 0.35:
                    #         Y_pred[i] = 2
                    # for i in range(len(Y_pred2_)):
                    #     if Y_pred2_[i][1] > max_value2[1] * limit_line2:
                    #         Y_pred2[i] = 1
                    #     elif Y_pred2_[i][2] > max_value2[2] * limit_line2:
                    #         Y_pred2[i] = 2

                    #       Save Pred_ohlcv      #
                    #   기존에 pybithumb 을 통해서 제공되던 ohlcv 와는 조금 다르다 >> 이전 데이터와 현재 y 데이터 행이 같다.
                    sliced_Y = Y_pred.reshape(-1, 1)
                    # sliced_Y2 = Y_pred2.reshape(-1, 1)[-len(sliced_Y):]
                    # pred_ohlcv = np.concatenate((sliced_ohlc, sliced_Y, sliced_Y2), axis=1)  # axis=1 가로로 합친다

                    #   col 이 7이 아닌 데이터 걸러주기
                    # try:
                    #     pred_ohlcv_df = pd.DataFrame(pred_ohlcv,
                    #                                  columns=['open', 'close', 'high', 'low', 'low_state', 'high_state'])
                    #
                    # except Exception as e:
                    #     print(e)
                    #     continue
                    # # print(pred_ohlcv_df.tail(20))
                    # # quit()
                    # pred_ohlcv_df.to_excel('./pred_ohlcv/%s_%s/%s' % (input_data_length, model_num, file))

                    # Y_pred 에 1 이 존재하면, Plot Comparing
                    if get_fig == 1:

                        spanlist_low = []
                        spanlist_high = []

                        for m in range(len(Y_pred)):
                            if (Y_pred[m] > 0.5) and (Y_pred[m] < 1.5):
                                if m + 1 < len(Y_pred):
                                    spanlist_low.append((m, m + 1))
                                else:
                                    spanlist_low.append((m - 1, m))

                        for m in range(len(Y_pred)):
                            if (Y_pred[m] > 1.5) and (Y_pred[m] < 2.5):
                                if m + 1 < len(Y_pred):
                                    spanlist_high.append((m, m + 1))
                                else:
                                    spanlist_high.append((m - 1, m))

                        plt.subplot(len(model_list), 1, fig_cnt)
                        fig_cnt += 1
                        # plt.subplot(313)
                        plt.plot(sliced_ohlc[:, [1]], 'gold', label='close')
                        plt.plot(sliced_ohlc[:, [-1]], 'b', label=model_name.split('.')[0].split('_')[-1])
                        plt.legend(loc='upper right')
                        for i in range(len(spanlist_low)):
                            plt.axvspan(spanlist_low[i][0], spanlist_low[i][1], facecolor='c', alpha=0.7)

                        # plt.subplot(212)
                        # # plt.subplot(313)
                        # plt.plot(sliced_ohlc[:, [1]], 'gold', label='close')
                        # plt.plot(sliced_ohlc[:, [-1]], 'b', label='MA')
                        # plt.legend(loc='upper right')
                        # for i in range(len(spanlist_high)):
                        #     plt.axvspan(spanlist_high[i][0], spanlist_high[i][1], facecolor='m', alpha=0.7)

                Date = file.split()[0]
                Coin = file.split()[1].split('.')[0]
                plt.savefig('./Figure_pred/%s_%s/%s %s.png' % (input_data_length, model_number, Date, Coin), dpi=500)
                plt.close()





