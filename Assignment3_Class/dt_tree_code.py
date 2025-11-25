"""
Decision tree model for John3 imitation learning.
Generated from trained model.
"""
def predict_bet(card, myscore, oppscore, minbet, pot, role):
    """
    Predict bet amount based on game state.
    
    Args:
        card: Card value (0.0-1.0)
        myscore: My current score
        oppscore: Opponent's current score
        minbet: Minimum bet increment
        pot: Current pot size
        role: 0 for small blind, 1 for big blind
    
    Returns:
        Predicted bet amount
    """
if card <= 0.9750001430511475:
  if minbet <= 3.0:
    if minbet <= 1.5:
      if card <= 0.25000153481960297:
        if role <= 0.5:
          if pot <= 1.5:
                return 1.0
          else:
            if card <= 0.24999116361141205:
                  return 0.0
            else:
                  return 0.2
        else:
          if pot <= 25.5:
            if pot <= 3.5:
              if myscore <= 198.5:
                if card <= 0.20673058182001114:
                  if pot <= 2.5:
                        return 2.0
                  else:
                    if card <= 0.15070875734090805:
                      if card <= 0.0924965888261795:
                        if card <= 0.06400084868073463:
                          if card <= 0.05289230868220329:
                                return 2.0
                          else:
                            if card <= 0.052928389981389046:
                                  return 2.1
                            else:
                                  return 2.0
                        else:
                          if card <= 0.06406494602560997:
                                return 2.1
                          else:
                            if myscore <= 100.5:
                                  return 2.000846381718155
                            else:
                                  return 2.003176043557169
                      else:
                        if card <= 0.09255343303084373:
                              return 2.090909090909091
                        else:
                          if oppscore <= 107.5:
                            if oppscore <= 76.5:
                                  return 2.009433962264151
                            else:
                                  return 2.0043614794138174
                          else:
                            if card <= 0.09396092593669891:
                                  return 2.0434782608695654
                            else:
                                  return 2.0106951871657754
                    else:
                      if oppscore <= 136.5:
                        if myscore <= 195.5:
                          if oppscore <= 111.5:
                            if card <= 0.15106570720672607:
                                  return 2.0377358490566038
                            else:
                                  return 2.012834516657564
                          else:
                            if card <= 0.15480496734380722:
                                  return 2.0517241379310347
                            else:
                                  return 2.0226648351648353
                        else:
                              return 2.125
                      else:
                        if card <= 0.19550638645887375:
                          if card <= 0.16013868153095245:
                                return 2.0
                          else:
                            if card <= 0.17317073792219162:
                                  return 2.1
                            else:
                                  return 2.0317460317460316
                        else:
                          if oppscore <= 142.5:
                                return 2.375
                          else:
                                return 2.1666666666666665
                else:
                  if pot <= 2.5:
                        return 2.0
                  else:
                    if myscore <= 97.5:
                      if oppscore <= 122.5:
                        if card <= 0.20733320713043213:
                          if card <= 0.20709610730409622:
                                return 2.076923076923077
                          else:
                                return 2.2
                        else:
                          if myscore <= 93.5:
                            if oppscore <= 108.5:
                                  return 2.0033557046979866
                            else:
                                  return 2.0268729641693812
                          else:
                            if card <= 0.22718974947929382:
                                  return 2.022875816993464
                            else:
                                  return 2.0594900849858355
                      else:
                        if card <= 0.24134549498558044:
                          if oppscore <= 148.5:
                            if myscore <= 66.5:
                                  return 2.0
                            else:
                                  return 2.0526315789473686
                          else:
                            if myscore <= 45.5:
                                  return 2.0303030303030303
                            else:
                                  return 2.2142857142857144
                        else:
                          if card <= 0.24813659489154816:
                            if card <= 0.247616246342659:
                                  return 2.111111111111111
                            else:
                                  return 2.3
                          else:
                                return 2.0
                    else:
                      if oppscore <= 97.5:
                        if myscore <= 109.5:
                          if card <= 0.2488570362329483:
                            if card <= 0.24647457152605057:
                                  return 2.0726040658276865
                            else:
                                  return 2.018867924528302
                          else:
                                return 2.1666666666666665
                        else:
                          if card <= 0.20713672786951065:
                                return 2.2666666666666666
                          else:
                            if card <= 0.2125788778066635:
                                  return 2.0086206896551726
                            else:
                                  return 2.033096926713948
                      else:
                        if myscore <= 99.5:
                          if card <= 0.2102746143937111:
                                return 2.0
                          else:
                            if card <= 0.21134275197982788:
                                  return 2.3
                            else:
                                  return 2.101298701298701
                        else:
                          if oppscore <= 99.5:
                            if myscore <= 101.5:
                                  return 2.090047393364929
                            else:
                                  return 2.1928934010152283
                          else:
                            if card <= 0.23676493763923645:
                                  return 2.410958904109589
                            else:
                                  return 2.3095238095238093
              else:
                    return 1.0
            else:
              if pot <= 5.5:
                if myscore <= 116.5:
                  if card <= 0.10590912029147148:
                    if card <= 0.061181364580988884:
                          return 2.0
                    else:
                      if oppscore <= 90.5:
                        if card <= 0.07384660840034485:
                          if card <= 0.0699387900531292:
                                return 2.0
                          else:
                            if card <= 0.07116576284170151:
                                  return 2.6
                            else:
                                  return 2.2857142857142856
                        else:
                          if oppscore <= 88.5:
                            if oppscore <= 86.5:
                                  return 2.0
                            else:
                                  return 2.0454545454545454
                          else:
                            if card <= 0.08927139639854431:
                                  return 2.0
                            else:
                                  return 2.25
                      else:
                        if oppscore <= 108.5:
                          if card <= 0.06163443624973297:
                                return 2.2
                          else:
                            if myscore <= 92.5:
                                  return 2.1142857142857143
                            else:
                                  return 2.0316856780735106
                        else:
                          if pot <= 4.5:
                                return 2.0
                          else:
                            if myscore <= 84.5:
                                  return 2.0
                            else:
                                  return 2.0476190476190474
                  else:
                    if pot <= 4.5:
                      if myscore <= 103.5:
                        if oppscore <= 151.5:
                          if card <= 0.12150586396455765:
                                return 2.0
                          else:
                            if oppscore <= 111.5:
                                  return 2.0736507936507937
                            else:
                                  return 2.031137724550898
                        else:
                          if myscore <= 34.5:
                                return 2.1818181818181817
                          else:
                            if card <= 0.18510685116052628:
                                  return 2.4
                            else:
                                  return 2.4
                      else:
                        if card <= 0.11319195106625557:
                          if oppscore <= 91.5:
                            if card <= 0.10998783633112907:
                                  return 2.4705882352941178
                            else:
                                  return 2.1818181818181817
                          else:
                            if card <= 0.10934590548276901:
                                  return 2.0
                            else:
                                  return 2.2
                        else:
                          if card <= 0.22354597598314285:
                            if card <= 0.21500379592180252:
                                  return 2.11703511053316
                            else:
                                  return 2.0
                          else:
                            if card <= 0.22966475039720535:
                                  return 2.34375
                            else:
                                  return 2.0921052631578947
                    else:
                      if oppscore <= 128.5:
                        if myscore <= 72.5:
                              return 2.75
                        else:
                          if card <= 0.23453516513109207:
                            if card <= 0.23022150993347168:
                                  return 2.2005988023952097
                            else:
                                  return 2.46875
                          else:
                            if card <= 0.24307283014059067:
                                  return 2.0
                            else:
                                  return 2.1666666666666665
                      else:
                        if myscore <= 50.5:
                          if myscore <= 45.5:
                                return 2.0
                          else:
                                return 2.5454545454545454
                        else:
                              return 2.0
                else:
                  if card <= 0.07641366496682167:
                    if card <= 0.049381496384739876:
                          return 2.0
                    else:
                      if oppscore <= 39.5:
                            return 2.0
                      else:
                        if myscore <= 148.5:
                          if oppscore <= 78.5:
                            if pot <= 4.5:
                                  return 2.1052631578947367
                            else:
                                  return 2.0
                          else:
                                return 2.0
                        else:
                          if card <= 0.06452169269323349:
                                return 2.1666666666666665
                          else:
                                return 2.4
                  else:
                    if card <= 0.17932193726301193:
                      if myscore <= 189.5:
                        if oppscore <= 73.5:
                          if oppscore <= 69.5:
                            if myscore <= 134.5:
                                  return 2.112676056338028
                            else:
                                  return 2.2904109589041095
                          else:
                            if pot <= 4.5:
                                  return 2.550724637681159
                            else:
                                  return 2.1578947368421053
                        else:
                          if oppscore <= 76.5:
                            if card <= 0.14702027291059494:
                                  return 2.0615384615384613
                            else:
                                  return 2.1818181818181817
                          else:
                            if oppscore <= 79.5:
                                  return 2.3017241379310347
                            else:
                                  return 2.192513368983957
                      else:
                        if pot <= 4.5:
                              return 2.0
                        else:
                              return 2.25
                    else:
                      if card <= 0.1896825134754181:
                        if card <= 0.18655972927808762:
                          if oppscore <= 60.0:
                            if oppscore <= 43.0:
                                  return 2.0
                            else:
                                  return 2.1818181818181817
                          else:
                            if oppscore <= 75.5:
                                  return 3.235294117647059
                            else:
                                  return 2.2222222222222223
                        else:
                          if myscore <= 134.0:
                                return 2.6923076923076925
                          else:
                                return 3.1875
                      else:
                        if oppscore <= 66.5:
                          if card <= 0.23090624064207077:
                            if myscore <= 135.5:
                                  return 3.1818181818181817
                            else:
                                  return 2.305389221556886
                          else:
                            if card <= 0.23768877983093262:
                                  return 3.16
                            else:
                                  return 2.473684210526316
                        else:
                          if card <= 0.24547836184501648:
                            if myscore <= 125.5:
                                  return 2.2857142857142856
                            else:
                                  return 2.116883116883117
                          else:
                            if card <= 0.24757978320121765:
                                  return 3.3
                            else:
                                  return 2.142857142857143
              else:
                if card <= 0.23648801445960999:
                  if card <= 0.19075221568346024:
                        return 2.0
                  else:
                    if card <= 0.19123440235853195:
                          return 3.0
                    else:
                          return 2.0
                else:
                  if card <= 0.23710468411445618:
                        return 2.8823529411764706
                  else:
                    if card <= 0.2487686350941658:
                          return 2.0
                    else:
                      if card <= 0.2491510808467865:
                            return 2.4
                      else:
                            return 2.0
          else:
                return 0.0
      else:
        if pot <= 25.5:
          if pot <= 3.5:
            if pot <= 2.5:
              if pot <= 1.5:
                    return 1.0
              else:
                    return 2.0
            else:
              if card <= 0.4764818996191025:
                if card <= 0.4259529709815979:
                  if card <= 0.353915736079216:
                    if oppscore <= 106.5:
                      if myscore <= 105.5:
                        if card <= 0.28148169815540314:
                          if myscore <= 99.5:
                            if oppscore <= 102.5:
                                  return 2.12597200622084
                            else:
                                  return 2.0789473684210527
                          else:
                            if myscore <= 100.5:
                                  return 2.3677884615384617
                            else:
                                  return 2.1226666666666665
                        else:
                          if myscore <= 96.5:
                            if card <= 0.3493107110261917:
                                  return 2.1614730878186967
                            else:
                                  return 2.230769230769231
                          else:
                            if myscore <= 100.5:
                                  return 2.2972886762360445
                            else:
                                  return 2.229455081001473
                      else:
                        if card <= 0.2829008102416992:
                          if oppscore <= 86.5:
                            if myscore <= 192.5:
                                  return 2.035892776010904
                            else:
                                  return 2.116279069767442
                          else:
                            if role <= 0.5:
                                  return 2.074626865671642
                            else:
                                  return 2.0449293966623876
                        else:
                          if myscore <= 196.5:
                            if oppscore <= 89.5:
                                  return 2.0968939905469277
                            else:
                                  return 2.1440677966101696
                          else:
                            if card <= 0.32592761516571045:
                                  return 2.7
                            else:
                                  return 2.8
                    else:
                      if card <= 0.2896778732538223:
                        if oppscore <= 136.5:
                          if role <= 0.5:
                            if myscore <= 70.5:
                                  return 2.1129032258064515
                            else:
                                  return 2.0545774647887325
                          else:
                            if myscore <= 89.5:
                                  return 2.0296236989591674
                            else:
                                  return 2.0562248995983934
                        else:
                          if card <= 0.2808872014284134:
                            if oppscore <= 145.5:
                                  return 2.0454545454545454
                            else:
                                  return 2.1157894736842104
                          else:
                            if card <= 0.28317536413669586:
                                  return 2.388888888888889
                            else:
                                  return 2.0952380952380953
                      else:
                        if oppscore <= 109.5:
                          if card <= 0.29073265194892883:
                            if role <= 0.5:
                                  return 2.1666666666666665
                            else:
                                  return 2.4166666666666665
                          else:
                            if card <= 0.35265257954597473:
                                  return 2.115569823434992
                            else:
                                  return 2.259259259259259
                        else:
                          if oppscore <= 187.5:
                            if role <= 0.5:
                                  return 2.094699922057677
                            else:
                                  return 2.0729253981559093
                          else:
                                return 2.3636363636363638
                  else:
                    if oppscore <= 108.5:
                      if oppscore <= 93.5:
                        if card <= 0.41395987570285797:
                          if oppscore <= 90.5:
                            if myscore <= 189.5:
                                  return 2.150943396226415
                            else:
                                  return 2.3125
                          else:
                            if card <= 0.36045898497104645:
                                  return 2.307017543859649
                            else:
                                  return 2.203864734299517
                        else:
                          if myscore <= 113.5:
                            if card <= 0.4188362658023834:
                                  return 2.2390243902439027
                            else:
                                  return 2.3447098976109215
                          else:
                            if card <= 0.4232049882411957:
                                  return 2.185185185185185
                            else:
                                  return 2.2473684210526317
                      else:
                        if oppscore <= 103.5:
                          if myscore <= 103.5:
                            if myscore <= 99.5:
                                  return 2.346116970278044
                            else:
                                  return 2.4085704939483152
                          else:
                            if card <= 0.3702041953802109:
                                  return 2.2130750605326877
                            else:
                                  return 2.293610911701364
                        else:
                          if role <= 0.5:
                            if myscore <= 92.5:
                                  return 2.2217391304347824
                            else:
                                  return 2.2919148936170215
                          else:
                            if card <= 0.4235805720090866:
                                  return 2.231107850330154
                            else:
                                  return 2.358490566037736
                    else:
                      if role <= 0.5:
                        if card <= 0.40327906608581543:
                          if card <= 0.35831597447395325:
                            if myscore <= 69.0:
                                  return 2.2857142857142856
                            else:
                                  return 2.062937062937063
                          else:
                            if oppscore <= 109.5:
                                  return 2.224242424242424
                            else:
                                  return 2.161806746712407
                        else:
                          if card <= 0.4035746604204178:
                                return 2.5
                          else:
                            if oppscore <= 161.0:
                                  return 2.2020089285714284
                            else:
                                  return 2.5
                      else:
                        if myscore <= 38.5:
                          if myscore <= 19.5:
                                return 2.1666666666666665
                          else:
                                return 2.526315789473684
                        else:
                          if card <= 0.42462681233882904:
                            if myscore <= 83.5:
                                  return 2.110706482155863
                            else:
                                  return 2.1437908496732025
                          else:
                            if oppscore <= 124.5:
                                  return 2.1794871794871793
                            else:
                                  return 2.5833333333333335
                else:
                  if card <= 0.44473862648010254:
                    if myscore <= 90.5:
                      if role <= 0.5:
                        if oppscore <= 126.5:
                          if myscore <= 81.5:
                            if card <= 0.44345684349536896:
                                  return 2.2051282051282053
                            else:
                                  return 2.4
                          else:
                            if oppscore <= 114.5:
                                  return 2.246696035242291
                            else:
                                  return 2.335766423357664
                        else:
                          if card <= 0.4369208961725235:
                            if myscore <= 67.5:
                                  return 2.1964285714285716
                            else:
                                  return 2.4186046511627906
                          else:
                            if card <= 0.4378380924463272:
                                  return 2.727272727272727
                            else:
                                  return 2.392156862745098
                      else:
                        if card <= 0.4350723773241043:
                          if card <= 0.42897604405879974:
                            if card <= 0.42867933213710785:
                                  return 2.1704545454545454
                            else:
                                  return 2.6153846153846154
                          else:
                            if card <= 0.430277481675148:
                                  return 2.081967213114754
                            else:
                                  return 2.1871657754010694
                        else:
                          if oppscore <= 110.5:
                            if card <= 0.4391331225633621:
                                  return 2.5833333333333335
                            else:
                                  return 2.3333333333333335
                          else:
                            if oppscore <= 147.5:
                                  return 2.227272727272727
                            else:
                                  return 2.5
                    else:
                      if myscore <= 108.5:
                        if oppscore <= 104.5:
                          if oppscore <= 95.5:
                            if card <= 0.4419342279434204:
                                  return 2.375
                            else:
                                  return 2.539473684210526
                          else:
                            if card <= 0.42603254318237305:
                                  return 2.9
                            else:
                                  return 2.504927536231884
                        else:
                          if card <= 0.42615269124507904:
                                return 2.8181818181818183
                          else:
                            if role <= 0.5:
                                  return 2.4048257372654156
                            else:
                                  return 2.33810888252149
                      else:
                        if oppscore <= 52.5:
                          if myscore <= 169.5:
                            if oppscore <= 44.5:
                                  return 2.106382978723404
                            else:
                                  return 2.0
                          else:
                            if card <= 0.44083596765995026:
                                  return 2.175438596491228
                            else:
                                  return 2.5
                        else:
                          if card <= 0.4398479461669922:
                            if myscore <= 123.5:
                                  return 2.28428927680798
                            else:
                                  return 2.23
                          else:
                            if myscore <= 115.5:
                                  return 2.4375
                            else:
                                  return 2.276595744680851
                  else:
                    if myscore <= 91.5:
                      if card <= 0.46035154163837433:
                        if myscore <= 51.5:
                          if card <= 0.4523061662912369:
                                return 2.5
                          else:
                                return 2.7142857142857144
                        else:
                          if oppscore <= 114.5:
                            if role <= 0.5:
                                  return 2.406015037593985
                            else:
                                  return 2.337121212121212
                          else:
                            if card <= 0.4496460258960724:
                                  return 2.3640350877192984
                            else:
                                  return 2.2395833333333335
                      else:
                        if myscore <= 78.5:
                          if oppscore <= 136.5:
                            if card <= 0.46515098214149475:
                                  return 2.193548387096774
                            else:
                                  return 2.3434782608695652
                          else:
                            if card <= 0.46326693892478943:
                                  return 2.7058823529411766
                            else:
                                  return 2.372340425531915
                        else:
                          if card <= 0.47446784377098083:
                            if card <= 0.46307648718357086:
                                  return 2.5223880597014925
                            else:
                                  return 2.4262048192771086
                          else:
                            if card <= 0.4762951135635376:
                                  return 2.6037735849056602
                            else:
                                  return 2.3846153846153846
                    else:
                      if myscore <= 114.5:
                        if card <= 0.4603729695081711:
                          if oppscore <= 95.5:
                            if role <= 0.5:
                                  return 2.5262008733624453
                            else:
                                  return 2.470982142857143
                          else:
                            if myscore <= 96.5:
                                  return 2.4984848484848485
                            else:
                                  return 2.5890302066772657
                        else:
                          if myscore <= 94.5:
                            if card <= 0.46290329098701477:
                                  return 2.6666666666666665
                            else:
                                  return 2.4984126984126984
                          else:
                            if myscore <= 105.5:
                                  return 2.6255025847214246
                            else:
                                  return 2.568080357142857
                      else:
                        if card <= 0.4587554633617401:
                          if myscore <= 187.5:
                            if oppscore <= 53.5:
                                  return 2.2556818181818183
                            else:
                                  return 2.3802345058626466
                          else:
                            if card <= 0.4538484364748001:
                                  return 2.4444444444444446
                            else:
                                  return 2.8333333333333335
                        else:
                          if oppscore <= 35.5:
                            if card <= 0.47364485263824463:
                                  return 2.4782608695652173
                            else:
                                  return 2.2222222222222223
                          else:
                            if card <= 0.46715351939201355:
                                  return 2.479302832244009
                            else:
                                  return 2.564681724845996
              else:
                if card <= 0.5547012090682983:
                  if card <= 0.511103481054306:
                    if myscore <= 89.5:
                      if card <= 0.4930476248264313:
                        if card <= 0.4768736809492111:
                          if card <= 0.4766046851873398:
                                return 2.4
                          else:
                            if myscore <= 83.0:
                                  return 2.6666666666666665
                            else:
                                  return 2.8181818181818183
                        else:
                          if card <= 0.47863540053367615:
                            if card <= 0.4776240140199661:
                                  return 2.396551724137931
                            else:
                                  return 2.253968253968254
                          else:
                            if oppscore <= 124.5:
                                  return 2.42456608811749
                            else:
                                  return 2.523076923076923
                      else:
                        if oppscore <= 141.5:
                          if oppscore <= 113.5:
                            if card <= 0.4947054982185364:
                                  return 2.85
                            else:
                                  return 2.6199261992619927
                          else:
                            if card <= 0.5040522813796997:
                                  return 2.5111940298507465
                            else:
                                  return 2.587467362924282
                        else:
                          if card <= 0.4959813058376312:
                                return 2.8823529411764706
                          else:
                            if card <= 0.5025380849838257:
                                  return 2.5714285714285716
                            else:
                                  return 2.7941176470588234
                    else:
                      if card <= 0.4924202561378479:
                        if oppscore <= 51.5:
                          if card <= 0.479195699095726:
                            if card <= 0.47819608449935913:
                                  return 2.586206896551724
                            else:
                                  return 2.7857142857142856
                          else:
                            if myscore <= 195.5:
                                  return 2.472081218274112
                            else:
                                  return 2.8
                        else:
                          if oppscore <= 105.5:
                            if oppscore <= 99.5:
                                  return 2.653681506849315
                            else:
                                  return 2.7019527235354572
                          else:
                            if card <= 0.485112726688385:
                                  return 2.57556270096463
                            else:
                                  return 2.6311475409836067
                      else:
                        if oppscore <= 105.5:
                          if myscore <= 108.5:
                            if card <= 0.5108414590358734:
                                  return 2.748825288338317
                            else:
                                  return 2.6129032258064515
                          else:
                            if card <= 0.5069017708301544:
                                  return 2.677045619116582
                            else:
                                  return 2.7680798004987532
                        else:
                          if card <= 0.5106377601623535:
                            if card <= 0.4963002949953079:
                                  return 2.6041666666666665
                            else:
                                  return 2.675728155339806
                          else:
                            if myscore <= 91.5:
                                  return 2.6363636363636362
                            else:
                                  return 2.3
                  else:
                    if oppscore <= 110.5:
                      if card <= 0.5341590940952301:
                        if card <= 0.5204549431800842:
                          if card <= 0.5204058885574341:
                            if card <= 0.5123636722564697:
                                  return 2.827272727272727
                            else:
                                  return 2.7607861936720997
                          else:
                                return 2.357142857142857
                        else:
                          if myscore <= 163.5:
                            if myscore <= 97.5:
                                  return 2.774912075029308
                            else:
                                  return 2.8357225881441304
                          else:
                            if myscore <= 186.5:
                                  return 2.6344086021505375
                            else:
                                  return 2.82
                      else:
                        if myscore <= 162.5:
                          if myscore <= 99.5:
                            if role <= 0.5:
                                  return 2.861111111111111
                            else:
                                  return 2.8056537102473498
                          else:
                            if oppscore <= 82.5:
                                  return 2.8425584255842558
                            else:
                                  return 2.884677419354839
                        else:
                          if card <= 0.5501376688480377:
                            if oppscore <= 35.5:
                                  return 2.72972972972973
                            else:
                                  return 2.5384615384615383
                          else:
                            if card <= 0.5535829365253448:
                                  return 2.96875
                            else:
                                  return 2.6
                    else:
                      if card <= 0.5241831541061401:
                        if myscore <= 86.5:
                          if card <= 0.5192103981971741:
                            if card <= 0.5113701820373535:
                                  return 2.3
                            else:
                                  return 2.656470588235294
                          else:
                            if myscore <= 67.5:
                                  return 2.702127659574468
                            else:
                                  return 2.5271317829457365
                        else:
                          if card <= 0.5179144144058228:
                            if card <= 0.5118516087532043:
                                  return 2.9
                            else:
                                  return 2.6106194690265485
                          else:
                            if card <= 0.5214574635028839:
                                  return 2.8983050847457625
                            else:
                                  return 2.68
                      else:
                        if oppscore <= 116.5:
                          if card <= 0.5297138690948486:
                            if myscore <= 86.5:
                                  return 2.7777777777777777
                            else:
                                  return 2.595505617977528
                          else:
                            if role <= 0.5:
                                  return 2.814404432132964
                            else:
                                  return 2.7369942196531793
                        else:
                          if card <= 0.5443181395530701:
                            if card <= 0.5390051007270813:
                                  return 2.7088
                            else:
                                  return 2.6244343891402715
                          else:
                            if oppscore <= 119.5:
                                  return 2.6904761904761907
                            else:
                                  return 2.790625
                else:
                  if card <= 0.6179015934467316:
                    if myscore <= 90.5:
                      if card <= 0.6062305867671967:
                        if myscore <= 79.5:
                          if card <= 0.6049705445766449:
                            if oppscore <= 150.5:
                                  return 2.826581378820185
                            else:
                                  return 2.902173913043478
                          else:
                            if oppscore <= 134.5:
                                  return 2.6206896551724137
                            else:
                                  return 2.9
                        else:
                          if card <= 0.5559310019016266:
                            if oppscore <= 113.5:
                                  return 2.9130434782608696
                            else:
                                  return 3.0
                          else:
                            if card <= 0.5703950226306915:
                                  return 2.8220211161387634
                            else:
                                  return 2.869075829383886
                      else:
                        if card <= 0.6173784732818604:
                          if myscore <= 85.5:
                            if card <= 0.6146719753742218:
                                  return 2.9158653846153846
                            else:
                                  return 2.8714285714285714
                          else:
                            if card <= 0.616394430398941:
                                  return 2.9448529411764706
                            else:
                                  return 3.0
                        else:
                          if card <= 0.617668867111206:
                                return 2.6315789473684212
                          else:
                                return 2.9375
                    else:
                      if card <= 0.5763563215732574:
                        if oppscore <= 41.5:
                          if card <= 0.5554518699645996:
                                return 3.0
                          else:
                            if card <= 0.5611012578010559:
                                  return 2.6984126984126986
                            else:
                                  return 2.806060606060606
                        else:
                          if card <= 0.5760654509067535:
                            if card <= 0.5649596154689789:
                                  return 2.893192009783938
                            else:
                                  return 2.914491108588725
                          else:
                            if card <= 0.5761674642562866:
                                  return 2.7
                            else:
                                  return 2.8793103448275863
                      else:
                        if oppscore <= 53.5:
                          if myscore <= 193.5:
                            if oppscore <= 13.5:
                                  return 2.7971014492753623
                            else:
                                  return 2.877049180327869
                          else:
                            if card <= 0.5897091329097748:
                                  return 2.9
                            else:
                                  return 3.0
                        else:
                          if card <= 0.6062666475772858:
                            if card <= 0.594211220741272:
                                  return 2.9279904306220095
                            else:
                                  return 2.9417900403768504
                          else:
                            if card <= 0.6178295314311981:
                                  return 2.96085409252669
                            else:
                                  return 2.8
                  else:
                    if card <= 0.6544837653636932:
                      if card <= 0.6273940205574036:
                        if oppscore <= 37.5:
                          if myscore <= 181.5:
                            if card <= 0.6248416900634766:
                                  return 2.891304347826087
                            else:
                                  return 2.6666666666666665
                          else:
                                return 3.0
                        else:
                          if oppscore <= 104.5:
                            if myscore <= 113.5:
                                  return 2.9750173490631506
                            else:
                                  return 2.9867172675521823
                          else:
                            if card <= 0.6235493719577789:
                                  return 2.9405487804878048
                            else:
                                  return 2.9653579676674364
                      else:
                        if myscore <= 81.5:
                          if card <= 0.6541904509067535:
                            if card <= 0.6462332010269165:
                                  return 2.9540059347181007
                            else:
                                  return 2.989051094890511
                          else:
                                return 2.8
                        else:
                          if oppscore <= 53.5:
                            if card <= 0.6532124578952789:
                                  return 2.9731182795698925
                            else:
                                  return 2.8421052631578947
                          else:
                            if card <= 0.6543648838996887:
                                  return 2.9879342349509415
                            else:
                                  return 2.9285714285714284
                    else:
                      if card <= 0.6974517405033112:
                        if oppscore <= 115.5:
                          if myscore <= 194.5:
                            if myscore <= 142.5:
                                  return 2.996052977808964
                            else:
                                  return 2.984567901234568
                          else:
                            if card <= 0.6722915768623352:
                                  return 2.8181818181818183
                            else:
                                  return 3.0
                        else:
                          if myscore <= 69.5:
                            if oppscore <= 135.5:
                                  return 2.9364161849710984
                            else:
                                  return 2.978798586572438
                          else:
                            if card <= 0.6971175372600555:
                                  return 2.9813620071684586
                            else:
                                  return 2.9
                      else:
                        if card <= 0.7480373978614807:
                          if card <= 0.7479803562164307:
                            if oppscore <= 143.5:
                                  return 2.998847996119566
                            else:
                                  return 2.989071038251366
                          else:
                                return 2.9
                        else:
                          if oppscore <= 14.5:
                            if oppscore <= 13.5:
                                  return 3.0
                            else:
                                  return 2.9863013698630136
                          else:
                                return 3.0
          else:
            if card <= 0.7027833163738251:
              if card <= 0.5639681220054626:
                if card <= 0.46584632992744446:
                  if pot <= 5.5:
                    if card <= 0.35243967175483704:
                      if pot <= 4.5:
                        if myscore <= 122.5:
                          if oppscore <= 98.5:
                            if myscore <= 110.5:
                                  return 2.156609195402299
                            else:
                                  return 2.2251791197543502
                          else:
                            if myscore <= 47.5:
                                  return 2.4
                            else:
                                  return 2.0974373415939174
                        else:
                          if oppscore <= 29.5:
                            if card <= 0.26483502984046936:
                                  return 2.0
                            else:
                                  return 2.2388059701492535
                          else:
                            if myscore <= 135.5:
                                  return 2.404494382022472
                            else:
                                  return 2.581151832460733
                      else:
                        if oppscore <= 75.5:
                          if role <= 0.5:
                            if myscore <= 154.5:
                                  return 3.5609756097560976
                            else:
                                  return 3.0384615384615383
                          else:
                            if myscore <= 143.5:
                                  return 2.810810810810811
                            else:
                                  return 3.24468085106383
                        else:
                          if role <= 0.5:
                            if myscore <= 103.5:
                                  return 2.489130434782609
                            else:
                                  return 2.9130434782608696
                          else:
                            if myscore <= 69.5:
                                  return 2.027027027027027
                            else:
                                  return 2.3518957345971563
                    else:
                      if myscore <= 96.5:
                        if card <= 0.4036700874567032:
                          if oppscore <= 113.5:
                            if card <= 0.40206028521060944:
                                  return 2.3398692810457518
                            else:
                                  return 2.074074074074074
                          else:
                            if card <= 0.37819576263427734:
                                  return 2.193396226415094
                            else:
                                  return 2.28743961352657
                        else:
                          if oppscore <= 108.5:
                            if card <= 0.42246875166893005:
                                  return 2.376681614349776
                            else:
                                  return 2.600886917960089
                          else:
                            if pot <= 4.5:
                                  return 2.314205079962371
                            else:
                                  return 2.5271317829457365
                      else:
                        if pot <= 4.5:
                          if oppscore <= 95.5:
                            if card <= 0.41082441806793213:
                                  return 2.5095057034220534
                            else:
                                  return 2.6444141689373297
                          else:
                            if oppscore <= 100.5:
                                  return 2.8618592528236317
                            else:
                                  return 2.6618287373004352
                        else:
                          if myscore <= 121.5:
                            if role <= 0.5:
                                  return 2.8698224852071004
                            else:
                                  return 2.4580152671755724
                          else:
                            if myscore <= 177.5:
                                  return 3.4150943396226414
                            else:
                                  return 2.857142857142857
                  else:
                    if myscore <= 114.5:
                      if card <= 0.3900145888328552:
                        if myscore <= 104.5:
                          if card <= 0.3729105293750763:
                            if card <= 0.33331406116485596:
                                  return 2.0351715154146763
                            else:
                                  return 2.0036363636363634
                          else:
                            if card <= 0.3731428384780884:
                                  return 2.7
                            else:
                                  return 2.0620842572062084
                        else:
                          if pot <= 12.5:
                            if card <= 0.26862600445747375:
                                  return 2.0
                            else:
                                  return 2.123441396508728
                          else:
                                return 2.0
                      else:
                        if card <= 0.39025452733039856:
                              return 4.0
                        else:
                          if pot <= 11.5:
                            if card <= 0.4140685945749283:
                                  return 2.1462522851919563
                            else:
                                  return 2.0400981996726677
                          else:
                            if pot <= 12.5:
                                  return 2.49645390070922
                            else:
                                  return 2.0
                    else:
                      if pot <= 12.5:
                        if pot <= 11.5:
                          if card <= 0.38099798560142517:
                            if pot <= 8.5:
                                  return 2.2686746987951807
                            else:
                                  return 2.0486381322957197
                          else:
                            if pot <= 8.5:
                                  return 2.608156028368794
                            else:
                                  return 2.26
                        else:
                          if card <= 0.3750198930501938:
                            if myscore <= 133.5:
                                  return 2.3125
                            else:
                                  return 2.8560311284046693
                          else:
                            if role <= 0.5:
                                  return 3.8506493506493507
                            else:
                                  return 2.263157894736842
                      else:
                        if pot <= 13.5:
                          if card <= 0.3101527988910675:
                            if card <= 0.29190880060195923:
                                  return 2.0
                            else:
                                  return 3.1
                          else:
                                return 2.0
                        else:
                              return 2.0
                else:
                  if pot <= 5.5:
                    if pot <= 4.5:
                      if oppscore <= 108.5:
                        if oppscore <= 92.5:
                          if myscore <= 130.5:
                            if card <= 0.5522158741950989:
                                  return 2.8401206636500755
                            else:
                                  return 3.0520833333333335
                          else:
                            if card <= 0.5085120499134064:
                                  return 2.9190938511326863
                            else:
                                  return 3.1279620853080567
                        else:
                          if oppscore <= 103.5:
                            if oppscore <= 99.5:
                                  return 3.062768701633706
                            else:
                                  return 3.2413793103448274
                          else:
                            if card <= 0.5082846581935883:
                                  return 2.8213166144200628
                            else:
                                  return 2.978922716627635
                      else:
                        if card <= 0.5404217839241028:
                          if oppscore <= 114.5:
                            if card <= 0.5087846517562866:
                                  return 2.6027397260273974
                            else:
                                  return 2.8097560975609754
                          else:
                            if myscore <= 54.5:
                                  return 2.8846153846153846
                            else:
                                  return 2.4316730523627075
                        else:
                          if card <= 0.5433170795440674:
                            if card <= 0.5427960157394409:
                                  return 2.962962962962963
                            else:
                                  return 3.5714285714285716
                          else:
                            if card <= 0.5443072617053986:
                                  return 2.272727272727273
                            else:
                                  return 2.7022900763358777
                    else:
                      if myscore <= 69.5:
                        if card <= 0.5186993181705475:
                          if card <= 0.47011809051036835:
                                return 2.0
                          else:
                            if card <= 0.4788711220026016:
                                  return 3.2
                            else:
                                  return 2.527027027027027
                        else:
                          if myscore <= 48.5:
                            if card <= 0.5487653613090515:
                                  return 2.2142857142857144
                            else:
                                  return 3.1538461538461537
                          else:
                            if myscore <= 61.5:
                                  return 3.8461538461538463
                            else:
                                  return 3.2
                      else:
                        if myscore <= 92.5:
                          if card <= 0.46846508979797363:
                                return 2.7058823529411766
                          else:
                            if oppscore <= 128.5:
                                  return 3.508604206500956
                            else:
                                  return 4.4
                        else:
                          if card <= 0.5367470383644104:
                            if myscore <= 105.5:
                                  return 3.820415879017013
                            else:
                                  return 3.611195158850227
                          else:
                            if oppscore <= 103.5:
                                  return 3.971631205673759
                            else:
                                  return 3.55
                  else:
                    if myscore <= 123.5:
                      if oppscore <= 89.5:
                        if pot <= 11.5:
                          if myscore <= 119.5:
                            if pot <= 7.5:
                                  return 2.181159420289855
                            else:
                                  return 2.5405405405405403
                          else:
                            if card <= 0.5118241012096405:
                                  return 2.098360655737705
                            else:
                                  return 2.0
                        else:
                          if pot <= 12.5:
                            if card <= 0.5033153295516968:
                                  return 3.176470588235294
                            else:
                                  return 5.188405797101449
                          else:
                                return 2.0
                      else:
                        if card <= 0.46613599359989166:
                              return 3.5714285714285716
                        else:
                          if card <= 0.5612925589084625:
                            if pot <= 11.5:
                                  return 2.1087928464977646
                            else:
                                  return 2.2779316712834716
                          else:
                            if pot <= 6.5:
                                  return 3.7142857142857144
                            else:
                                  return 2.508771929824561
                    else:
                      if pot <= 11.5:
                        if card <= 0.5234041213989258:
                          if pot <= 9.5:
                            if myscore <= 175.5:
                                  return 2.742616033755274
                            else:
                                  return 2.3981481481481484
                          else:
                            if myscore <= 173.5:
                                  return 2.0
                            else:
                                  return 2.8181818181818183
                        else:
                          if myscore <= 180.5:
                            if pot <= 7.5:
                                  return 2.3777777777777778
                            else:
                                  return 3.0391061452513966
                          else:
                            if myscore <= 184.5:
                                  return 5.3076923076923075
                            else:
                                  return 3.6578947368421053
                      else:
                        if pot <= 12.5:
                          if role <= 0.5:
                            if oppscore <= 28.0:
                                  return 2.0
                            else:
                                  return 6.229074889867841
                          else:
                                return 2.0
                        else:
                          if pot <= 16.5:
                            if card <= 0.5069029927253723:
                                  return 2.0
                            else:
                                  return 3.52212389380531
                          else:
                                return 2.0
              else:
                if myscore <= 122.5:
                  if pot <= 12.5:
                    if pot <= 11.5:
                      if pot <= 8.5:
                        if pot <= 4.5:
                          if card <= 0.6443131268024445:
                            if oppscore <= 110.5:
                                  return 3.423985993580391
                            else:
                                  return 3.1047765793528503
                          else:
                            if oppscore <= 123.5:
                                  return 3.6921618204804045
                            else:
                                  return 3.2545454545454544
                        else:
                          if pot <= 6.5:
                            if oppscore <= 123.5:
                                  return 4.188344594594595
                            else:
                                  return 3.557046979865772
                          else:
                            if card <= 0.6411073505878448:
                                  return 2.6232876712328768
                            else:
                                  return 4.0
                      else:
                        if pot <= 9.5:
                          if role <= 0.5:
                            if oppscore <= 84.5:
                                  return 3.0
                            else:
                                  return 2.0
                          else:
                            if card <= 0.6755762100219727:
                                  return 2.8439716312056738
                            else:
                                  return 3.6470588235294117
                        else:
                          if pot <= 10.5:
                            if oppscore <= 93.5:
                                  return 2.1463414634146343
                            else:
                                  return 2.0203562340966923
                          else:
                            if card <= 0.6151993572711945:
                                  return 2.0927835051546393
                            else:
                                  return 2.569620253164557
                    else:
                      if oppscore <= 99.5:
                        if card <= 0.6414790451526642:
                          if myscore <= 112.5:
                            if card <= 0.6278493404388428:
                                  return 4.5
                            else:
                                  return 5.888888888888889
                          else:
                            if card <= 0.6130837202072144:
                                  return 5.684210526315789
                            else:
                                  return 7.769230769230769
                        else:
                          if role <= 0.5:
                            if card <= 0.6463745534420013:
                                  return 11.0
                            else:
                                  return 8.0
                          else:
                                return 5.157894736842105
                      else:
                        if card <= 0.6630300879478455:
                          if oppscore <= 107.5:
                            if card <= 0.6485691666603088:
                                  return 2.2419354838709675
                            else:
                                  return 4.0
                          else:
                            if card <= 0.5989387035369873:
                                  return 2.9195402298850577
                            else:
                                  return 3.9254658385093166
                        else:
                          if card <= 0.6682526767253876:
                                return 5.75
                          else:
                            if card <= 0.684934139251709:
                                  return 3.6176470588235294
                            else:
                                  return 4.631578947368421
                  else:
                    if myscore <= 112.5:
                      if card <= 0.6894250512123108:
                        if card <= 0.5670812726020813:
                          if card <= 0.5665127635002136:
                                return 2.0
                          else:
                                return 3.1
                        else:
                          if myscore <= 106.5:
                                return 2.0
                          else:
                            if oppscore <= 92.5:
                                  return 2.0
                            else:
                                  return 2.6842105263157894
                      else:
                        if pot <= 14.5:
                              return 4.428571428571429
                        else:
                          if pot <= 16.5:
                                return 2.736842105263158
                          else:
                                return 2.0
                    else:
                      if card <= 0.6111891567707062:
                            return 2.0
                      else:
                        if pot <= 18.5:
                          if pot <= 13.5:
                                return 2.0
                          else:
                            if role <= 0.5:
                                  return 3.52
                            else:
                                  return 5.190476190476191
                        else:
                          if card <= 0.661359429359436:
                                return 2.0
                          else:
                                return 3.0588235294117645
                else:
                  if pot <= 11.5:
                    if pot <= 8.5:
                      if pot <= 4.5:
                        if card <= 0.5947954952716827:
                          if oppscore <= 16.5:
                            if card <= 0.5743371546268463:
                                  return 3.4
                            else:
                                  return 3.6666666666666665
                          else:
                            if oppscore <= 28.5:
                                  return 2.8205128205128207
                            else:
                                  return 3.2598425196850394
                        else:
                          if card <= 0.6628844439983368:
                            if card <= 0.6606365442276001:
                                  return 3.5592105263157894
                            else:
                                  return 3.142857142857143
                          else:
                            if card <= 0.7001778781414032:
                                  return 3.7453580901856762
                            else:
                                  return 3.28
                      else:
                        if card <= 0.6382133662700653:
                          if oppscore <= 27.5:
                            if pot <= 6.5:
                                  return 4.39
                            else:
                                  return 2.765432098765432
                          else:
                            if pot <= 7.5:
                                  return 3.994722955145119
                            else:
                                  return 5.0508474576271185
                        else:
                          if pot <= 6.5:
                            if card <= 0.6868337392807007:
                                  return 4.100719424460432
                            else:
                                  return 4.590361445783133
                          else:
                            if oppscore <= 64.5:
                                  return 5.090277777777778
                            else:
                                  return 6.333333333333333
                    else:
                      if pot <= 10.5:
                        if card <= 0.6749476492404938:
                          if pot <= 9.5:
                            if oppscore <= 18.5:
                                  return 3.1052631578947367
                            else:
                                  return 2.42
                          else:
                            if oppscore <= 31.5:
                                  return 2.0
                            else:
                                  return 2.3037974683544302
                        else:
                          if myscore <= 174.5:
                            if pot <= 9.5:
                                  return 4.333333333333333
                            else:
                                  return 2.4210526315789473
                          else:
                                return 5.1
                      else:
                        if myscore <= 171.5:
                          if card <= 0.6667818129062653:
                            if oppscore <= 42.5:
                                  return 2.0
                            else:
                                  return 3.3278688524590163
                          else:
                            if card <= 0.6757333278656006:
                                  return 6.909090909090909
                            else:
                                  return 3.8947368421052633
                        else:
                          if myscore <= 182.0:
                                return 7.4
                          else:
                                return 3.8
                  else:
                    if pot <= 12.5:
                      if role <= 0.5:
                        if card <= 0.606182336807251:
                          if card <= 0.5774820446968079:
                            if oppscore <= 66.5:
                                  return 7.384615384615385
                            else:
                                  return 3.6666666666666665
                          else:
                            if card <= 0.5853868722915649:
                                  return 11.333333333333334
                            else:
                                  return 7.344827586206897
                        else:
                          if myscore <= 167.5:
                            if card <= 0.6974973976612091:
                                  return 10.486238532110091
                            else:
                                  return 8.666666666666666
                          else:
                                return 5.076923076923077
                      else:
                        if card <= 0.6585688889026642:
                          if card <= 0.5931060314178467:
                                return 2.0
                          else:
                                return 4.105263157894737
                        else:
                          if myscore <= 154.0:
                                return 9.5
                          else:
                                return 6.545454545454546
                    else:
                      if card <= 0.6717458367347717:
                        if card <= 0.6479151248931885:
                          if pot <= 15.5:
                            if card <= 0.5929145812988281:
                                  return 3.7941176470588234
                            else:
                                  return 2.4473684210526314
                          else:
                            if card <= 0.6369664371013641:
                                  return 2.0
                            else:
                                  return 3.6666666666666665
                        else:
                          if pot <= 19.5:
                            if card <= 0.6652040183544159:
                                  return 5.325
                            else:
                                  return 2.65
                          else:
                                return 2.0
                      else:
                        if pot <= 18.5:
                          if role <= 0.5:
                            if pot <= 15.5:
                                  return 3.5714285714285716
                            else:
                                  return 6.357142857142857
                          else:
                            if myscore <= 164.5:
                                  return 10.4
                            else:
                                  return 5.333333333333333
                        else:
                          if oppscore <= 52.0:
                                return 2.0
                          else:
                            if card <= 0.6890065371990204:
                                  return 3.2
                            else:
                                  return 5.6
            else:
              if pot <= 6.5:
                if pot <= 4.5:
                  if card <= 0.7515353560447693:
                    if oppscore <= 112.5:
                      if card <= 0.7046174108982086:
                        if card <= 0.7032698392868042:
                              return 4.0
                        else:
                          if card <= 0.7044602632522583:
                            if card <= 0.7041938602924347:
                                  return 3.5813953488372094
                            else:
                                  return 4.0
                          else:
                                return 3.230769230769231
                      else:
                        if card <= 0.7513565123081207:
                          if card <= 0.750444620847702:
                            if oppscore <= 43.5:
                                  return 3.931972789115646
                            else:
                                  return 3.8352745424292847
                          else:
                                return 4.0
                        else:
                              return 3.4545454545454546
                    else:
                      if card <= 0.7067714631557465:
                        if oppscore <= 132.5:
                          if role <= 0.5:
                            if oppscore <= 122.5:
                                  return 3.8823529411764706
                            else:
                                  return 3.6
                          else:
                                return 3.176470588235294
                        else:
                              return 2.8333333333333335
                      else:
                        if oppscore <= 116.5:
                          if card <= 0.7367797195911407:
                            if card <= 0.7262353599071503:
                                  return 3.7560975609756095
                            else:
                                  return 3.5294117647058822
                          else:
                            if card <= 0.7431007623672485:
                                  return 4.0
                            else:
                                  return 3.75
                        else:
                          if oppscore <= 145.0:
                            if oppscore <= 138.5:
                                  return 3.5792207792207793
                            else:
                                  return 3.3
                          else:
                            if role <= 0.5:
                                  return 4.0
                            else:
                                  return 3.7333333333333334
                  else:
                    if card <= 0.8080227375030518:
                      if myscore <= 68.5:
                        if oppscore <= 132.5:
                              return 3.3846153846153846
                        else:
                          if card <= 0.7743426561355591:
                            if card <= 0.762366771697998:
                                  return 3.8260869565217392
                            else:
                                  return 4.0
                          else:
                            if card <= 0.8011911511421204:
                                  return 3.6507936507936507
                            else:
                                  return 4.0
                      else:
                        if oppscore <= 120.5:
                          if oppscore <= 23.5:
                                return 4.0
                          else:
                            if card <= 0.7788557708263397:
                                  return 3.944410129709697
                            else:
                                  return 3.9254312743461326
                        else:
                          if card <= 0.7815938293933868:
                            if card <= 0.7752364277839661:
                                  return 3.89010989010989
                            else:
                                  return 3.5714285714285716
                          else:
                            if oppscore <= 122.5:
                                  return 3.85
                            else:
                                  return 3.953488372093023
                    else:
                      if card <= 0.8381411135196686:
                        if oppscore <= 161.5:
                          if card <= 0.8379394710063934:
                            if card <= 0.8100872933864594:
                                  return 3.96875
                            else:
                                  return 3.9947780678851177
                          else:
                                return 3.8
                        else:
                              return 3.8
                      else:
                        if myscore <= 62.5:
                          if card <= 0.8500603139400482:
                                return 3.8823529411764706
                          else:
                                return 4.0
                        else:
                          if myscore <= 78.5:
                            if myscore <= 77.5:
                                  return 4.0
                            else:
                                  return 3.9649122807017543
                          else:
                                return 4.0
                else:
                  if pot <= 5.5:
                    if card <= 0.8096979856491089:
                      if oppscore <= 137.5:
                        if oppscore <= 92.5:
                          if oppscore <= 67.5:
                            if card <= 0.7610336244106293:
                                  return 4.701863354037267
                            else:
                                  return 4.881188118811881
                          else:
                            if card <= 0.7058555781841278:
                                  return 4.086956521739131
                            else:
                                  return 4.539232053422371
                        else:
                          if oppscore <= 102.5:
                            if card <= 0.8077219426631927:
                                  return 4.838862559241706
                            else:
                                  return 4.4
                          else:
                            if card <= 0.8088452517986298:
                                  return 4.710191082802548
                            else:
                                  return 4.1
                      else:
                        if card <= 0.7727064490318298:
                          if oppscore <= 172.0:
                            if card <= 0.7378387451171875:
                                  return 4.15625
                            else:
                                  return 3.5
                          else:
                                return 4.8125
                        else:
                          if myscore <= 32.0:
                                return 4.538461538461538
                          else:
                                return 5.0
                    else:
                      if card <= 0.8184086680412292:
                        if oppscore <= 86.0:
                          if card <= 0.8113562762737274:
                                return 5.0
                          else:
                            if oppscore <= 79.5:
                                  return 4.117647058823529
                            else:
                                  return 4.538461538461538
                        else:
                          if card <= 0.81804159283638:
                            if card <= 0.8176022469997406:
                                  return 4.979310344827586
                            else:
                                  return 4.75
                          else:
                                return 4.4
                      else:
                        if card <= 0.8698861598968506:
                          if card <= 0.8693674206733704:
                            if myscore <= 46.5:
                                  return 4.892857142857143
                            else:
                                  return 4.992449664429531
                          else:
                                return 4.7
                        else:
                              return 5.0
                  else:
                    if card <= 0.8000423610210419:
                      if myscore <= 80.5:
                        if myscore <= 79.5:
                          if myscore <= 74.5:
                            if myscore <= 59.0:
                                  return 5.2
                            else:
                                  return 4.235294117647059
                          else:
                            if oppscore <= 123.5:
                                  return 4.571428571428571
                            else:
                                  return 5.666666666666667
                        else:
                              return 3.6
                      else:
                        if oppscore <= 92.5:
                          if oppscore <= 42.5:
                            if card <= 0.7180704772472382:
                                  return 6.0
                            else:
                                  return 5.380281690140845
                          else:
                            if card <= 0.7683043777942657:
                                  return 4.681081081081081
                            else:
                                  return 5.2592592592592595
                        else:
                          if myscore <= 96.5:
                            if card <= 0.7820174992084503:
                                  return 5.301310043668122
                            else:
                                  return 4.8936170212765955
                          else:
                            if card <= 0.706131249666214:
                                  return 4.4
                            else:
                                  return 5.586206896551724
                    else:
                      if card <= 0.8857519328594208:
                        if card <= 0.8790477514266968:
                          if card <= 0.8122825622558594:
                            if card <= 0.8074550330638885:
                                  return 5.904761904761905
                            else:
                                  return 5.4
                          else:
                            if card <= 0.8196171820163727:
                                  return 6.0
                            else:
                                  return 5.87175572519084
                        else:
                          if oppscore <= 112.5:
                            if oppscore <= 82.5:
                                  return 5.238095238095238
                            else:
                                  return 5.9
                          else:
                                return 5.0
                      else:
                        if card <= 0.8900840878486633:
                          if card <= 0.8892460763454437:
                                return 6.0
                          else:
                                return 5.6
                        else:
                              return 6.0
              else:
                if card <= 0.85948047041893:
                  if myscore <= 111.5:
                    if pot <= 13.5:
                      if card <= 0.8108047544956207:
                        if pot <= 11.5:
                          if pot <= 9.5:
                            if card <= 0.7631241679191589:
                                  return 5.252747252747253
                            else:
                                  return 7.363143631436315
                          else:
                            if pot <= 10.5:
                                  return 2.087431693989071
                            else:
                                  return 2.853211009174312
                        else:
                          if myscore <= 105.5:
                            if myscore <= 64.5:
                                  return 4.2988505747126435
                            else:
                                  return 6.543859649122807
                          else:
                            if pot <= 12.5:
                                  return 9.432432432432432
                            else:
                                  return 5.384615384615385
                      else:
                        if card <= 0.8389827013015747:
                          if pot <= 10.5:
                            if myscore <= 87.5:
                                  return 6.791666666666667
                            else:
                                  return 7.66
                          else:
                            if pot <= 11.5:
                                  return 3.367088607594937
                            else:
                                  return 7.3604651162790695
                        else:
                          if pot <= 11.5:
                            if oppscore <= 104.5:
                                  return 8.5375
                            else:
                                  return 7.118421052631579
                          else:
                            if oppscore <= 132.5:
                                  return 10.950980392156863
                            else:
                                  return 7.315789473684211
                    else:
                      if pot <= 19.5:
                        if card <= 0.7654183208942413:
                          if card <= 0.7393001317977905:
                            if oppscore <= 96.5:
                                  return 3.0
                            else:
                                  return 2.0
                          else:
                            if card <= 0.7463993430137634:
                                  return 5.235294117647059
                            else:
                                  return 2.5283018867924527
                        else:
                          if myscore <= 106.5:
                            if role <= 0.5:
                                  return 2.8514851485148514
                            else:
                                  return 4.693548387096774
                          else:
                            if pot <= 15.5:
                                  return 9.909090909090908
                            else:
                                  return 5.1
                      else:
                        if oppscore <= 90.5:
                              return 4.294117647058823
                        else:
                          if card <= 0.7504384815692902:
                            if card <= 0.7467100918292999:
                                  return 2.3304347826086955
                            else:
                                  return 5.636363636363637
                          else:
                            if myscore <= 98.5:
                                  return 2.0791666666666666
                            else:
                                  return 2.447058823529412
                  else:
                    if pot <= 11.5:
                      if card <= 0.8096103668212891:
                        if pot <= 9.5:
                          if card <= 0.7627131640911102:
                            if pot <= 8.5:
                                  return 6.674157303370786
                            else:
                                  return 3.235294117647059
                          else:
                            if pot <= 8.5:
                                  return 6.9798994974874375
                            else:
                                  return 8.222222222222221
                        else:
                          if pot <= 10.5:
                            if myscore <= 183.5:
                                  return 2.6779661016949152
                            else:
                                  return 5.294117647058823
                          else:
                            if oppscore <= 58.5:
                                  return 6.984615384615385
                            else:
                                  return 4.830645161290323
                      else:
                        if card <= 0.8409884572029114:
                          if pot <= 10.5:
                            if pot <= 7.5:
                                  return 6.761904761904762
                            else:
                                  return 8.045714285714286
                          else:
                            if oppscore <= 57.5:
                                  return 9.363636363636363
                            else:
                                  return 5.4
                        else:
                          if pot <= 8.5:
                            if pot <= 7.5:
                                  return 7.0
                            else:
                                  return 7.877551020408164
                          else:
                            if myscore <= 117.5:
                                  return 8.0
                            else:
                                  return 9.36923076923077
                    else:
                      if myscore <= 174.5:
                        if oppscore <= 73.5:
                          if card <= 0.7283890545368195:
                            if pot <= 12.5:
                                  return 10.96551724137931
                            else:
                                  return 6.360655737704918
                          else:
                            if pot <= 22.5:
                                  return 10.929824561403509
                            else:
                                  return 16.76923076923077
                        else:
                          if pot <= 12.5:
                            if role <= 0.5:
                                  return 11.01639344262295
                            else:
                                  return 6.166666666666667
                          else:
                            if pot <= 23.5:
                                  return 5.328
                            else:
                                  return 11.0
                      else:
                        if pot <= 16.5:
                          if oppscore <= 16.5:
                            if myscore <= 185.5:
                                  return 4.444444444444445
                            else:
                                  return 2.6176470588235294
                          else:
                            if role <= 0.5:
                                  return 7.166666666666667
                            else:
                                  return 11.666666666666666
                        else:
                          if myscore <= 179.5:
                            if pot <= 21.5:
                                  return 6.166666666666667
                            else:
                                  return 2.0
                          else:
                                return 2.0
                else:
                  if pot <= 13.5:
                    if pot <= 10.5:
                      if pot <= 8.5:
                        if pot <= 7.5:
                              return 7.0
                        else:
                          if card <= 0.8793164789676666:
                            if oppscore <= 116.5:
                                  return 7.791666666666667
                            else:
                                  return 6.9411764705882355
                          else:
                            if card <= 0.8880245983600616:
                                  return 7.903225806451613
                            else:
                                  return 8.0
                      else:
                        if card <= 0.8975512087345123:
                          if myscore <= 85.5:
                            if pot <= 9.5:
                                  return 9.0
                            else:
                                  return 5.84
                          else:
                            if myscore <= 169.5:
                                  return 8.433179723502304
                            else:
                                  return 9.5
                        else:
                          if pot <= 9.5:
                                return 9.0
                          else:
                            if card <= 0.8999239504337311:
                                  return 9.428571428571429
                            else:
                                  return 10.0
                    else:
                      if pot <= 11.5:
                        if card <= 0.904791921377182:
                          if oppscore <= 126.0:
                            if oppscore <= 82.5:
                                  return 10.307692307692308
                            else:
                                  return 8.673469387755102
                          else:
                                return 3.2857142857142856
                        else:
                              return 11.0
                      else:
                        if oppscore <= 148.5:
                          if myscore <= 186.0:
                            if pot <= 12.5:
                                  return 11.91044776119403
                            else:
                                  return 12.64516129032258
                          else:
                                return 9.470588235294118
                        else:
                          if card <= 0.925097793340683:
                            if card <= 0.8895914554595947:
                                  return 4.142857142857143
                            else:
                                  return 7.470588235294118
                          else:
                            if card <= 0.9517540037631989:
                                  return 12.076923076923077
                            else:
                                  return 12.363636363636363
                  else:
                    if myscore <= 48.5:
                      if card <= 0.9299667775630951:
                        if myscore <= 24.5:
                          if card <= 0.9180047810077667:
                                return 2.0
                          else:
                                return 3.6
                        else:
                              return 5.0
                      else:
                        if pot <= 21.0:
                          if pot <= 16.5:
                                return 15.545454545454545
                          else:
                                return 18.2
                        else:
                              return 23.692307692307693
                    else:
                      if pot <= 17.5:
                        if myscore <= 182.5:
                          if pot <= 15.5:
                            if myscore <= 85.5:
                                  return 12.208333333333334
                            else:
                                  return 14.392857142857142
                          else:
                            if card <= 0.868660181760788:
                                  return 13.5625
                            else:
                                  return 16.131914893617022
                        else:
                          if card <= 0.9337478578090668:
                                return 3.6666666666666665
                          else:
                                return 15.0
                      else:
                        if card <= 0.8657969534397125:
                          if myscore <= 101.0:
                                return 3.0
                          else:
                                return 11.25
                        else:
                          if oppscore <= 25.5:
                            if card <= 0.9133889973163605:
                                  return 4.357142857142857
                            else:
                                  return 17.75
                          else:
                            if pot <= 22.5:
                                  return 19.157635467980295
                            else:
                                  return 23.722772277227723
        else:
          if card <= 0.9643298089504242:
            if card <= 0.9166665971279144:
                  return 0.0
            else:
              if card <= 0.9168423712253571:
                    return 6.6
              else:
                    return 0.0
          else:
            if myscore <= 116.5:
              if myscore <= 95.5:
                if oppscore <= 105.5:
                      return 8.181818181818182
                else:
                  if pot <= 59.5:
                    if pot <= 42.5:
                          return 0.0
                    else:
                          return 5.666666666666667
                  else:
                        return 0.0
              else:
                    return 0.0
            else:
              if card <= 0.9657995700836182:
                    return 15.6
              else:
                if oppscore <= 76.5:
                      return 0.0
                else:
                  if card <= 0.9700310230255127:
                        return 0.0
                  else:
                        return 18.6
    else:
      if card <= 0.2500005513429642:
        if role <= 0.5:
          if pot <= 3.5:
            if pot <= 2.5:
                  return 2.0
            else:
                  return 4.0
          else:
                return 0.0
        else:
          if pot <= 50.5:
            if pot <= 2.5:
                  return 2.0
            else:
              if pot <= 7.5:
                if pot <= 4.5:
                      return 4.0
                else:
                  if card <= 0.13990847766399384:
                    if card <= 0.09325354918837547:
                      if card <= 0.07346636801958084:
                        if card <= 0.061090653762221336:
                              return 4.0
                        else:
                          if card <= 0.06116638518869877:
                                return 4.2
                          else:
                            if card <= 0.06545846164226532:
                                  return 4.003623188405797
                            else:
                                  return 4.0
                      else:
                        if card <= 0.07354186102747917:
                              return 4.2
                        else:
                          if oppscore <= 63.5:
                            if oppscore <= 62.5:
                                  return 4.02
                            else:
                                  return 4.133333333333334
                          else:
                            if card <= 0.08472819998860359:
                                  return 4.0018518518518515
                            else:
                                  return 4.009815950920245
                    else:
                      if card <= 0.09374038875102997:
                        if myscore <= 130.5:
                          if myscore <= 110.0:
                            if card <= 0.09353404492139816:
                                  return 4.0
                            else:
                                  return 4.222222222222222
                          else:
                                return 4.4
                        else:
                              return 4.0
                      else:
                        if myscore <= 119.5:
                          if card <= 0.12934492528438568:
                            if card <= 0.09869043529033661:
                                  return 4.0
                            else:
                                  return 4.013698630136986
                          else:
                            if card <= 0.12945204973220825:
                                  return 4.2
                            else:
                                  return 4.021403091557669
                        else:
                          if oppscore <= 79.5:
                            if oppscore <= 63.5:
                                  return 4.022947925860548
                            else:
                                  return 4.042553191489362
                          else:
                            if card <= 0.10688883438706398:
                                  return 4.3076923076923075
                            else:
                                  return 4.055555555555555
                  else:
                    if myscore <= 187.5:
                      if card <= 0.19165442883968353:
                        if card <= 0.14000039547681808:
                              return 4.333333333333333
                        else:
                          if oppscore <= 112.5:
                            if card <= 0.16547605395317078:
                                  return 4.030330882352941
                            else:
                                  return 4.045433893684689
                          else:
                            if card <= 0.14044901728630066:
                                  return 4.266666666666667
                            else:
                                  return 4.052822371828069
                      else:
                        if card <= 0.19243158400058746:
                          if oppscore <= 50.0:
                                return 4.545454545454546
                          else:
                            if oppscore <= 111.5:
                                  return 4.064516129032258
                            else:
                                  return 4.32258064516129
                        else:
                          if myscore <= 134.5:
                            if oppscore <= 188.5:
                                  return 4.055989820032721
                            else:
                                  return 4.4
                          else:
                            if myscore <= 180.5:
                                  return 4.086350974930362
                            else:
                                  return 4.194444444444445
                    else:
                      if card <= 0.21791107952594757:
                        if myscore <= 193.5:
                          if card <= 0.17516830563545227:
                            if card <= 0.1657465323805809:
                                  return 4.105263157894737
                            else:
                                  return 4.4
                          else:
                                return 4.0
                        else:
                              return 4.315789473684211
                      else:
                        if card <= 0.22688593715429306:
                              return 4.8
                        else:
                          if oppscore <= 8.5:
                                return 4.6
                          else:
                                return 4.142857142857143
              else:
                if oppscore <= 51.5:
                  if pot <= 9.5:
                    if card <= 0.06084934063255787:
                      if card <= 0.05519183725118637:
                            return 4.0
                      else:
                        if card <= 0.05776390992105007:
                              return 4.8
                        else:
                              return 4.0
                    else:
                      if myscore <= 171.5:
                        if card <= 0.24007095396518707:
                          if card <= 0.19551973044872284:
                            if card <= 0.18869652599096298:
                                  return 4.466666666666667
                            else:
                                  return 5.454545454545454
                          else:
                            if oppscore <= 41.5:
                                  return 4.0
                            else:
                                  return 4.620689655172414
                        else:
                          if myscore <= 156.5:
                                return 4.4
                          else:
                                return 6.153846153846154
                      else:
                        if oppscore <= 24.5:
                          if card <= 0.1431221291422844:
                            if card <= 0.11930480226874352:
                                  return 4.776119402985074
                            else:
                                  return 4.0
                          else:
                            if oppscore <= 12.5:
                                  return 5.478260869565218
                            else:
                                  return 4.7
                        else:
                          if myscore <= 174.5:
                            if card <= 0.14564332365989685:
                                  return 5.2
                            else:
                                  return 4.615384615384615
                          else:
                                return 5.555555555555555
                  else:
                    if card <= 0.20098000019788742:
                      if myscore <= 158.5:
                        if oppscore <= 42.5:
                          if pot <= 24.0:
                                return 4.8
                          else:
                                return 4.0
                        else:
                              return 4.0
                      else:
                            return 4.0
                    else:
                      if pot <= 12.5:
                        if card <= 0.20976170897483826:
                              return 5.0
                        else:
                          if oppscore <= 36.5:
                            if oppscore <= 26.5:
                                  return 4.206896551724138
                            else:
                                  return 4.7368421052631575
                          else:
                                return 4.0
                      else:
                            return 4.0
                else:
                  if card <= 0.1521781161427498:
                    if pot <= 8.5:
                      if card <= 0.06491953879594803:
                        if card <= 0.0546623058617115:
                              return 4.0
                        else:
                          if card <= 0.05512918345630169:
                                return 4.4
                          else:
                                return 4.0
                      else:
                        if card <= 0.06539813429117203:
                              return 5.2
                        else:
                          if myscore <= 130.5:
                            if card <= 0.06753648817539215:
                                  return 4.285714285714286
                            else:
                                  return 4.05984251968504
                          else:
                            if card <= 0.0708671286702156:
                                  return 4.923076923076923
                            else:
                                  return 4.236286919831223
                    else:
                      if card <= 0.11439412459731102:
                            return 4.0
                      else:
                        if card <= 0.11506656184792519:
                              return 4.8
                        else:
                              return 4.0
                  else:
                    if myscore <= 107.5:
                      if card <= 0.1528496891260147:
                            return 4.8
                      else:
                        if oppscore <= 149.5:
                          if myscore <= 52.5:
                            if card <= 0.19155976176261902:
                                  return 5.0
                            else:
                                  return 4.0
                          else:
                            if pot <= 19.0:
                                  return 4.097242380261248
                            else:
                                  return 4.0
                        else:
                              return 4.0
                    else:
                      if card <= 0.15603755414485931:
                        if card <= 0.15470697730779648:
                          if oppscore <= 82.0:
                                return 4.0
                          else:
                                return 5.0
                        else:
                              return 6.545454545454546
                      else:
                        if pot <= 19.0:
                          if myscore <= 108.5:
                            if card <= 0.19157137721776962:
                                  return 4.3076923076923075
                            else:
                                  return 4.7368421052631575
                          else:
                            if card <= 0.23920289427042007:
                                  return 4.210849539406346
                            else:
                                  return 4.032520325203252
                        else:
                              return 4.0
          else:
                return 0.0
      else:
        if pot <= 4.5:
          if pot <= 2.5:
                return 2.0
          else:
                return 4.0
        else:
          if pot <= 50.5:
            if card <= 0.5934454798698425:
              if card <= 0.4780350774526596:
                if pot <= 6.5:
                  if card <= 0.44463396072387695:
                    if card <= 0.3438797891139984:
                      if oppscore <= 193.5:
                        if card <= 0.3138114660978317:
                          if oppscore <= 21.5:
                            if card <= 0.2804019898176193:
                                  return 4.117647058823529
                            else:
                                  return 4.335135135135135
                          else:
                            if card <= 0.28896255791187286:
                                  return 4.079222562585825
                            else:
                                  return 4.103493307215149
                        else:
                          if oppscore <= 76.5:
                            if myscore <= 178.5:
                                  return 4.1902967498822425
                            else:
                                  return 4.33879781420765
                          else:
                            if myscore <= 45.5:
                                  return 4.2266288951841355
                            else:
                                  return 4.132452981192477
                      else:
                        if card <= 0.2879950702190399:
                              return 5.454545454545454
                        else:
                              return 5.0
                    else:
                      if role <= 0.5:
                        if card <= 0.3762940764427185:
                          if myscore <= 102.5:
                            if myscore <= 81.5:
                                  return 4.233396584440228
                            else:
                                  return 4.1390937829293994
                          else:
                            if card <= 0.3442263901233673:
                                  return 4.782608695652174
                            else:
                                  return 4.252140818268316
                        else:
                          if myscore <= 8.5:
                                return 5.4
                          else:
                            if card <= 0.4318397790193558:
                                  return 4.282379412178315
                            else:
                                  return 4.340626848018924
                      else:
                        if card <= 0.37969741225242615:
                          if oppscore <= 10.5:
                            if card <= 0.35317249596118927:
                                  return 4.4
                            else:
                                  return 5.076923076923077
                          else:
                            if card <= 0.34571778774261475:
                                  return 4.260869565217392
                            else:
                                  return 4.154218032390621
                        else:
                          if myscore <= 166.5:
                            if card <= 0.43843451142311096:
                                  return 4.209568535368359
                            else:
                                  return 4.274084124830393
                          else:
                            if card <= 0.4040362387895584:
                                  return 4.459016393442623
                            else:
                                  return 4.209606986899563
                  else:
                    if card <= 0.46646748483181:
                      if card <= 0.4598210006952286:
                        if oppscore <= 161.5:
                          if role <= 0.5:
                            if oppscore <= 158.5:
                                  return 4.43404255319149
                            else:
                                  return 4.0
                          else:
                            if oppscore <= 8.5:
                                  return 5.166666666666667
                            else:
                                  return 4.3382022471910116
                        else:
                          if myscore <= 37.5:
                            if card <= 0.44639188051223755:
                                  return 5.0
                            else:
                                  return 4.547008547008547
                          else:
                                return 5.166666666666667
                      else:
                        if card <= 0.4648965448141098:
                          if card <= 0.4648413062095642:
                            if oppscore <= 177.0:
                                  return 4.54014598540146
                            else:
                                  return 4.133333333333334
                          else:
                                return 5.0
                        else:
                          if myscore <= 97.5:
                            if myscore <= 66.5:
                                  return 4.448979591836735
                            else:
                                  return 4.204081632653061
                          else:
                            if card <= 0.46637168526649475:
                                  return 4.5607476635514015
                            else:
                                  return 4.0
                    else:
                      if oppscore <= 50.5:
                        if card <= 0.4692400395870209:
                          if card <= 0.46905140578746796:
                            if myscore <= 155.5:
                                  return 4.666666666666667
                            else:
                                  return 5.071428571428571
                          else:
                                return 5.454545454545454
                        else:
                          if card <= 0.4745677411556244:
                            if card <= 0.47357913851737976:
                                  return 4.777777777777778
                            else:
                                  return 4.25
                          else:
                            if myscore <= 163.5:
                                  return 4.846153846153846
                            else:
                                  return 5.16
                      else:
                        if card <= 0.4756925106048584:
                          if role <= 0.5:
                            if card <= 0.46971097588539124:
                                  return 4.5683060109289615
                            else:
                                  return 4.696969696969697
                          else:
                            if card <= 0.4666134864091873:
                                  return 5.0
                            else:
                                  return 4.5511651469098275
                        else:
                          if card <= 0.47782979905605316:
                            if oppscore <= 164.5:
                                  return 4.774049217002237
                            else:
                                  return 5.5
                          else:
                            if card <= 0.47792261838912964:
                                  return 4.076923076923077
                            else:
                                  return 4.628571428571429
                else:
                  if pot <= 10.5:
                    if pot <= 8.5:
                      if myscore <= 162.5:
                        if myscore <= 119.5:
                          if myscore <= 8.5:
                            if card <= 0.45123665034770966:
                                  return 5.375
                            else:
                                  return 7.2
                          else:
                            if card <= 0.3613417446613312:
                                  return 4.196040246673158
                            else:
                                  return 4.373166926677067
                        else:
                          if myscore <= 138.5:
                            if card <= 0.3392997831106186:
                                  return 4.329835082458771
                            else:
                                  return 4.521560574948666
                          else:
                            if card <= 0.30129486322402954:
                                  return 4.819875776397516
                            else:
                                  return 4.549728752260398
                      else:
                        if oppscore <= 10.5:
                          if card <= 0.28164201974868774:
                                return 5.0
                          else:
                            if oppscore <= 9.5:
                                  return 6.372881355932203
                            else:
                                  return 5.0
                        else:
                          if card <= 0.39608146250247955:
                            if role <= 0.5:
                                  return 4.724919093851133
                            else:
                                  return 4.960573476702509
                          else:
                            if role <= 0.5:
                                  return 5.45945945945946
                            else:
                                  return 5.005988023952096
                    else:
                      if myscore <= 97.5:
                        if card <= 0.3931948393583298:
                          if role <= 0.5:
                            if myscore <= 66.5:
                                  return 4.402985074626866
                            else:
                                  return 5.056179775280899
                          else:
                            if oppscore <= 115.5:
                                  return 4.742857142857143
                            else:
                                  return 4.216606498194946
                        else:
                          if card <= 0.396475151181221:
                                return 7.2727272727272725
                          else:
                            if card <= 0.46323761343955994:
                                  return 5.304964539007092
                            else:
                                  return 4.6835443037974684
                      else:
                        if role <= 0.5:
                          if oppscore <= 57.5:
                            if card <= 0.42970798909664154:
                                  return 6.63819095477387
                            else:
                                  return 7.56043956043956
                          else:
                            if card <= 0.3344007283449173:
                                  return 5.541095890410959
                            else:
                                  return 6.252747252747253
                        else:
                          if card <= 0.36123161017894745:
                            if myscore <= 180.5:
                                  return 4.855072463768116
                            else:
                                  return 6.181818181818182
                          else:
                            if myscore <= 179.5:
                                  return 5.5
                            else:
                                  return 7.36
                  else:
                    if pot <= 24.5:
                      if pot <= 23.5:
                        if pot <= 18.5:
                          if pot <= 17.5:
                            if oppscore <= 187.5:
                                  return 4.222222222222222
                            else:
                                  return 5.166666666666667
                          else:
                            if card <= 0.4600885957479477:
                                  return 4.987179487179487
                            else:
                                  return 7.5
                        else:
                              return 4.0
                      else:
                        if card <= 0.4232502579689026:
                          if myscore <= 159.5:
                            if myscore <= 123.5:
                                  return 4.390243902439025
                            else:
                                  return 4.0
                          else:
                            if card <= 0.34136757254600525:
                                  return 4.0
                            else:
                                  return 6.580645161290323
                        else:
                          if oppscore <= 87.5:
                            if card <= 0.45358985662460327:
                                  return 11.692307692307692
                            else:
                                  return 4.0
                          else:
                            if card <= 0.46660466492176056:
                                  return 4.0
                            else:
                                  return 8.0
                    else:
                          return 4.0
              else:
                if card <= 0.5269250273704529:
                  if pot <= 10.5:
                    if pot <= 8.5:
                      if card <= 0.5092082321643829:
                        if myscore <= 135.5:
                          if pot <= 7.0:
                            if card <= 0.49022938311100006:
                                  return 4.814498933901919
                            else:
                                  return 5.032464076636509
                          else:
                            if oppscore <= 129.5:
                                  return 4.55
                            else:
                                  return 4.8432432432432435
                        else:
                          if myscore <= 162.5:
                            if pot <= 7.0:
                                  return 5.079787234042553
                            else:
                                  return 5.255605381165919
                          else:
                            if pot <= 6.5:
                                  return 5.265469061876248
                            else:
                                  return 5.8125
                      else:
                        if pot <= 7.5:
                          if oppscore <= 94.5:
                            if myscore <= 192.5:
                                  return 5.313807531380753
                            else:
                                  return 5.833333333333333
                          else:
                            if card <= 0.519287496805191:
                                  return 5.150643451930356
                            else:
                                  return 5.279503105590062
                        else:
                          if oppscore <= 43.5:
                            if oppscore <= 30.5:
                                  return 5.948717948717949
                            else:
                                  return 5.28
                          else:
                            if oppscore <= 66.5:
                                  return 4.916030534351145
                            else:
                                  return 4.601449275362318
                    else:
                      if oppscore <= 59.5:
                        if myscore <= 183.5:
                          if myscore <= 168.5:
                            if card <= 0.48699502646923065:
                                  return 6.3076923076923075
                            else:
                                  return 7.428571428571429
                          else:
                            if card <= 0.5037711560726166:
                                  return 6.8
                            else:
                                  return 5.714285714285714
                        else:
                              return 8.4
                      else:
                        if oppscore <= 86.5:
                          if role <= 0.5:
                            if card <= 0.5119746327400208:
                                  return 6.1
                            else:
                                  return 7.75
                          else:
                            if myscore <= 130.5:
                                  return 6.1
                            else:
                                  return 4.2
                        else:
                          if oppscore <= 180.5:
                            if myscore <= 111.5:
                                  return 5.412742382271468
                            else:
                                  return 4.0
                          else:
                                return 7.0
                  else:
                    if oppscore <= 92.5:
                      if pot <= 23.0:
                        if pot <= 18.5:
                          if pot <= 17.5:
                            if oppscore <= 12.5:
                                  return 5.454545454545454
                            else:
                                  return 4.221498371335505
                          else:
                            if card <= 0.4978182762861252:
                                  return 4.933333333333334
                            else:
                                  return 9.833333333333334
                        else:
                          if card <= 0.4846491068601608:
                            if card <= 0.48229144513607025:
                                  return 4.0
                            else:
                                  return 5.8
                          else:
                                return 4.0
                      else:
                        if pot <= 24.5:
                          if card <= 0.5129258036613464:
                            if card <= 0.49864666163921356:
                                  return 11.272727272727273
                            else:
                                  return 5.176470588235294
                          else:
                                return 14.666666666666666
                        else:
                          if oppscore <= 35.5:
                            if oppscore <= 31.5:
                                  return 4.0
                            else:
                                  return 6.7272727272727275
                          else:
                                return 4.0
                    else:
                      if pot <= 24.5:
                        if pot <= 23.5:
                          if pot <= 19.0:
                            if pot <= 17.5:
                                  return 4.226666666666667
                            else:
                                  return 5.2727272727272725
                          else:
                                return 4.0
                        else:
                          if myscore <= 61.0:
                                return 4.0
                          else:
                            if myscore <= 78.5:
                                  return 9.0
                            else:
                                  return 5.428571428571429
                      else:
                            return 4.0
                else:
                  if pot <= 24.5:
                    if pot <= 23.5:
                      if pot <= 19.5:
                        if pot <= 17.5:
                          if pot <= 11.5:
                            if pot <= 8.5:
                                  return 5.45203957996769
                            else:
                                  return 6.298479087452471
                          else:
                            if card <= 0.5501777529716492:
                                  return 4.204946996466431
                            else:
                                  return 5.215613382899628
                        else:
                          if oppscore <= 99.5:
                            if role <= 0.5:
                                  return 6.32
                            else:
                                  return 9.95
                          else:
                            if role <= 0.5:
                                  return 4.0
                            else:
                                  return 6.0
                      else:
                        if card <= 0.5822447836399078:
                          if oppscore <= 178.5:
                            if myscore <= 159.5:
                                  return 4.0
                            else:
                                  return 4.5
                          else:
                                return 5.333333333333333
                        else:
                          if card <= 0.5840995013713837:
                                return 6.833333333333333
                          else:
                            if oppscore <= 102.0:
                                  return 4.0
                            else:
                                  return 4.75
                    else:
                      if role <= 0.5:
                        if oppscore <= 136.0:
                          if card <= 0.5878030955791473:
                            if card <= 0.5610079169273376:
                                  return 13.454545454545455
                            else:
                                  return 10.285714285714286
                          else:
                                return 18.0
                        else:
                          if myscore <= 25.5:
                                return 4.0
                          else:
                                return 8.615384615384615
                      else:
                            return 4.0
                  else:
                    if card <= 0.5288310050964355:
                          return 6.8
                    else:
                      if card <= 0.5903246998786926:
                        if pot <= 32.5:
                          if myscore <= 140.0:
                                return 4.0
                          else:
                            if pot <= 31.0:
                                  return 4.0
                            else:
                                  return 8.0
                        else:
                              return 4.0
                      else:
                        if role <= 0.5:
                              return 7.8
                        else:
                              return 4.0
            else:
              if pot <= 8.5:
                if pot <= 6.5:
                  if card <= 0.630617618560791:
                    if card <= 0.6118897497653961:
                      if oppscore <= 88.5:
                        if card <= 0.5977062284946442:
                          if card <= 0.5975467264652252:
                            if myscore <= 129.5:
                                  return 5.758620689655173
                            else:
                                  return 5.614457831325301
                          else:
                                return 5.2
                        else:
                          if myscore <= 186.5:
                            if myscore <= 180.5:
                                  return 5.760157273918741
                            else:
                                  return 5.470588235294118
                          else:
                                return 6.0
                      else:
                        if myscore <= 36.5:
                          if card <= 0.6090303659439087:
                            if card <= 0.5998141169548035:
                                  return 5.947368421052632
                            else:
                                  return 5.6716417910447765
                          else:
                                return 6.0
                        else:
                          if card <= 0.5939412415027618:
                            if card <= 0.593678742647171:
                                  return 5.5675675675675675
                            else:
                                  return 5.25
                          else:
                            if card <= 0.5940811038017273:
                                  return 6.0
                            else:
                                  return 5.637213254035684
                    else:
                      if myscore <= 127.5:
                        if card <= 0.6203882992267609:
                          if card <= 0.619999885559082:
                            if role <= 0.5:
                                  return 5.795601552393273
                            else:
                                  return 5.727659574468085
                          else:
                            if card <= 0.6201520264148712:
                                  return 5.333333333333333
                            else:
                                  return 5.757575757575758
                        else:
                          if card <= 0.6305384337902069:
                            if card <= 0.620571106672287:
                                  return 6.0
                            else:
                                  return 5.811320754716981
                          else:
                                return 5.384615384615385
                      else:
                        if card <= 0.6165968477725983:
                          if card <= 0.6162869334220886:
                            if card <= 0.6127785742282867:
                                  return 5.938461538461539
                            else:
                                  return 5.740259740259741
                          else:
                                return 5.285714285714286
                        else:
                          if card <= 0.6180648803710938:
                            if oppscore <= 64.5:
                                  return 6.0
                            else:
                                  return 5.9
                          else:
                            if card <= 0.6191282272338867:
                                  return 5.7611940298507465
                            else:
                                  return 5.8847117794486214
                  else:
                    if card <= 0.684154599905014:
                      if card <= 0.639688104391098:
                        if myscore <= 20.5:
                              return 5.666666666666667
                        else:
                          if card <= 0.639646977186203:
                            if myscore <= 119.5:
                                  return 5.896575821104123
                            else:
                                  return 5.92874109263658
                          else:
                                return 5.6923076923076925
                      else:
                        if card <= 0.6508806049823761:
                          if oppscore <= 157.5:
                            if oppscore <= 52.5:
                                  return 5.913978494623656
                            else:
                                  return 5.953628166595105
                          else:
                            if role <= 0.5:
                                  return 5.802816901408451
                            else:
                                  return 5.963636363636364
                        else:
                          if oppscore <= 44.5:
                            if oppscore <= 43.5:
                                  return 5.944591029023747
                            else:
                                  return 5.793103448275862
                          else:
                            if oppscore <= 102.5:
                                  return 5.975706494794249
                            else:
                                  return 5.959624680125106
                    else:
                      if card <= 0.7108305096626282:
                        if card <= 0.7107858657836914:
                          if oppscore <= 50.5:
                            if card <= 0.7070895433425903:
                                  return 5.978260869565218
                            else:
                                  return 5.909090909090909
                          else:
                            if oppscore <= 187.5:
                                  return 5.9878644867689195
                            else:
                                  return 5.904761904761905
                        else:
                              return 5.8
                      else:
                        if card <= 0.7753681540489197:
                          if card <= 0.7753463387489319:
                            if myscore <= 114.5:
                                  return 5.998385794995965
                            else:
                                  return 5.99159402241594
                          else:
                                return 5.8
                        else:
                          if card <= 0.7931261956691742:
                            if card <= 0.7931065261363983:
                                  return 5.9991071428571425
                            else:
                                  return 5.8
                          else:
                                return 6.0
                else:
                  if card <= 0.749487429857254:
                    if card <= 0.6703226864337921:
                      if myscore <= 137.5:
                        if card <= 0.6251670718193054:
                          if oppscore <= 79.5:
                            if card <= 0.5979514420032501:
                                  return 4.823529411764706
                            else:
                                  return 5.7923497267759565
                          else:
                            if oppscore <= 139.5:
                                  return 5.096418732782369
                            else:
                                  return 5.552238805970149
                        else:
                          if oppscore <= 163.5:
                            if oppscore <= 83.5:
                                  return 6.033254156769596
                            else:
                                  return 5.552941176470588
                          else:
                            if myscore <= 14.5:
                                  return 7.428571428571429
                            else:
                                  return 6.604651162790698
                      else:
                        if myscore <= 169.5:
                          if role <= 0.5:
                            if card <= 0.5962913930416107:
                                  return 7.2
                            else:
                                  return 6.413333333333333
                          else:
                            if card <= 0.6457958817481995:
                                  return 6.009950248756219
                            else:
                                  return 6.408602150537634
                        else:
                          if card <= 0.6369798481464386:
                            if card <= 0.6320736706256866:
                                  return 6.666666666666667
                            else:
                                  return 5.25
                          else:
                            if card <= 0.6412100493907928:
                                  return 7.714285714285714
                            else:
                                  return 6.954545454545454
                    else:
                      if oppscore <= 67.5:
                        if card <= 0.7305555045604706:
                          if myscore <= 163.5:
                            if myscore <= 162.5:
                                  return 6.712727272727273
                            else:
                                  return 5.666666666666667
                          else:
                            if card <= 0.7226094901561737:
                                  return 7.164444444444444
                            else:
                                  return 6.4
                        else:
                          if card <= 0.7481927573680878:
                            if myscore <= 181.5:
                                  return 7.258536585365854
                            else:
                                  return 8.0
                          else:
                            if myscore <= 155.5:
                                  return 6.181818181818182
                            else:
                                  return 6.8
                      else:
                        if card <= 0.7232050001621246:
                          if myscore <= 32.5:
                            if card <= 0.6906535029411316:
                                  return 7.578947368421052
                            else:
                                  return 6.666666666666667
                          else:
                            if oppscore <= 95.5:
                                  return 6.294032023289665
                            else:
                                  return 5.991752577319588
                        else:
                          if myscore <= 108.5:
                            if oppscore <= 173.5:
                                  return 6.434782608695652
                            else:
                                  return 7.555555555555555
                          else:
                            if myscore <= 119.5:
                                  return 7.055555555555555
                            else:
                                  return 6.666666666666667
                  else:
                    if card <= 0.815322071313858:
                      if oppscore <= 57.5:
                        if card <= 0.750835120677948:
                              return 6.545454545454546
                        else:
                          if myscore <= 168.5:
                            if myscore <= 152.5:
                                  return 7.597883597883598
                            else:
                                  return 7.373737373737374
                          else:
                            if card <= 0.7703551054000854:
                                  return 7.573333333333333
                            else:
                                  return 7.811023622047244
                      else:
                        if card <= 0.8025638163089752:
                          if card <= 0.75325807929039:
                            if card <= 0.7500157952308655:
                                  return 8.0
                            else:
                                  return 7.310344827586207
                          else:
                            if card <= 0.7541734874248505:
                                  return 6.235294117647059
                            else:
                                  return 6.958751393534002
                        else:
                          if card <= 0.8142581284046173:
                            if myscore <= 36.5:
                                  return 8.0
                            else:
                                  return 7.457142857142857
                          else:
                            if card <= 0.8150250613689423:
                                  return 6.666666666666667
                            else:
                                  return 6.0
                    else:
                      if card <= 0.828934520483017:
                        if card <= 0.8286283612251282:
                          if oppscore <= 103.5:
                            if myscore <= 164.5:
                                  return 7.831831831831832
                            else:
                                  return 8.0
                          else:
                            if oppscore <= 106.5:
                                  return 7.0
                            else:
                                  return 7.794392523364486
                        else:
                              return 7.2
                      else:
                        if card <= 0.8546469807624817:
                          if myscore <= 32.5:
                            if card <= 0.8413917720317841:
                                  return 8.0
                            else:
                                  return 7.2
                          else:
                            if oppscore <= 94.5:
                                  return 7.90228013029316
                            else:
                                  return 8.0
                        else:
                          if card <= 0.8928206861019135:
                            if card <= 0.8922667801380157:
                                  return 7.979166666666667
                            else:
                                  return 7.703703703703703
                          else:
                            if card <= 0.9002164900302887:
                                  return 7.98876404494382
                            else:
                                  return 8.0
              else:
                if card <= 0.8876053094863892:
                  if card <= 0.8057526051998138:
                    if pot <= 24.5:
                      if pot <= 23.5:
                        if pot <= 18.5:
                          if card <= 0.7007646262645721:
                            if oppscore <= 42.5:
                                  return 8.049484536082474
                            else:
                                  return 6.284820031298905
                          else:
                            if pot <= 12.5:
                                  return 7.872578562204047
                            else:
                                  return 10.418092909535453
                        else:
                          if card <= 0.7245534360408783:
                            if myscore <= 20.5:
                                  return 4.744186046511628
                            else:
                                  return 4.176600441501104
                          else:
                            if pot <= 21.5:
                                  return 4.2471042471042475
                            else:
                                  return 5.489655172413793
                      else:
                        if oppscore <= 121.5:
                          if role <= 0.5:
                            if oppscore <= 30.5:
                                  return 4.0
                            else:
                                  return 19.454545454545453
                          else:
                            if card <= 0.659043937921524:
                                  return 5.538461538461538
                            else:
                                  return 4.0
                        else:
                          if card <= 0.7003940045833588:
                            if card <= 0.6085646748542786:
                                  return 8.0
                            else:
                                  return 4.357142857142857
                          else:
                            if myscore <= 39.5:
                                  return 5.666666666666667
                            else:
                                  return 12.936170212765957
                    else:
                      if pot <= 38.5:
                        if oppscore <= 98.5:
                          if oppscore <= 39.5:
                            if myscore <= 163.5:
                                  return 6.608695652173913
                            else:
                                  return 4.487804878048781
                          else:
                            if card <= 0.7244664132595062:
                                  return 7.021897810218978
                            else:
                                  return 12.442307692307692
                        else:
                          if oppscore <= 150.5:
                            if oppscore <= 137.5:
                                  return 5.260869565217392
                            else:
                                  return 11.454545454545455
                          else:
                            if oppscore <= 171.5:
                                  return 4.0
                            else:
                                  return 4.235294117647059
                      else:
                        if pot <= 49.5:
                          if pot <= 40.5:
                            if myscore <= 130.0:
                                  return 4.0
                            else:
                                  return 5.090909090909091
                          else:
                                return 4.0
                        else:
                          if card <= 0.6369587182998657:
                                return 8.6
                          else:
                                return 4.0
                  else:
                    if pot <= 34.5:
                      if pot <= 12.5:
                        if pot <= 10.5:
                          if card <= 0.8282237648963928:
                            if oppscore <= 171.5:
                                  return 8.789772727272727
                            else:
                                  return 10.0
                          else:
                            if card <= 0.8659868836402893:
                                  return 9.622641509433961
                            else:
                                  return 9.88888888888889
                        else:
                          if oppscore <= 70.5:
                            if myscore <= 164.5:
                                  return 8.786324786324787
                            else:
                                  return 11.282051282051283
                          else:
                            if card <= 0.8098803162574768:
                                  return 9.333333333333334
                            else:
                                  return 10.955414012738853
                      else:
                        if myscore <= 63.5:
                          if pot <= 20.5:
                            if myscore <= 20.5:
                                  return 16.873563218390803
                            else:
                                  return 12.36036036036036
                          else:
                            if myscore <= 36.0:
                                  return 4.12987012987013
                            else:
                                  return 8.324324324324325
                        else:
                          if pot <= 23.5:
                            if pot <= 19.5:
                                  return 14.30607966457023
                            else:
                                  return 10.645435244161359
                          else:
                            if myscore <= 166.5:
                                  return 19.296
                            else:
                                  return 7.6
                    else:
                      if oppscore <= 144.5:
                        if oppscore <= 50.5:
                          if pot <= 40.5:
                            if oppscore <= 39.5:
                                  return 4.0
                            else:
                                  return 8.857142857142858
                          else:
                                return 4.0
                        else:
                          if card <= 0.8553767502307892:
                            if card <= 0.82060706615448:
                                  return 12.705882352941176
                            else:
                                  return 5.56
                          else:
                            if myscore <= 104.5:
                                  return 21.12
                            else:
                                  return 35.166666666666664
                      else:
                            return 4.0
                else:
                  if pot <= 16.5:
                    if pot <= 12.5:
                      if pot <= 10.5:
                            return 10.0
                      else:
                        if card <= 0.8962449729442596:
                          if oppscore <= 78.5:
                            if myscore <= 155.5:
                                  return 8.8
                            else:
                                  return 12.0
                          else:
                            if card <= 0.8931066393852234:
                                  return 12.0
                            else:
                                  return 11.2
                        else:
                          if card <= 0.9104306995868683:
                            if myscore <= 115.5:
                                  return 12.0
                            else:
                                  return 11.483870967741936
                          else:
                                return 12.0
                    else:
                      if pot <= 14.5:
                        if card <= 0.8959372937679291:
                          if oppscore <= 112.0:
                                return 14.0
                          else:
                                return 13.0
                        else:
                              return 14.0
                      else:
                        if card <= 0.9019483923912048:
                          if card <= 0.8994759023189545:
                            if myscore <= 72.0:
                                  return 13.0
                            else:
                                  return 15.612903225806452
                          else:
                                return 12.4
                        else:
                              return 16.0
                  else:
                    if card <= 0.9266459941864014:
                      if myscore <= 50.5:
                        if pot <= 20.5:
                          if card <= 0.9048864245414734:
                                return 19.272727272727273
                          else:
                                return 17.6
                        else:
                          if card <= 0.9236464202404022:
                            if oppscore <= 155.5:
                                  return 8.916666666666666
                            else:
                                  return 5.196078431372549
                          else:
                                return 10.533333333333333
                      else:
                        if oppscore <= 49.5:
                          if pot <= 24.5:
                            if myscore <= 172.5:
                                  return 18.878048780487806
                            else:
                                  return 14.23076923076923
                          else:
                            if pot <= 33.0:
                                  return 10.923076923076923
                            else:
                                  return 5.6
                        else:
                          if pot <= 25.0:
                            if pot <= 23.0:
                                  return 17.074766355140188
                            else:
                                  return 22.596491228070175
                          else:
                            if pot <= 33.0:
                                  return 26.90909090909091
                            else:
                                  return 35.134328358208954
                    else:
                      if pot <= 30.5:
                        if pot <= 22.5:
                          if pot <= 20.5:
                            if pot <= 18.5:
                                  return 18.0
                            else:
                                  return 20.0
                          else:
                                return 22.0
                        else:
                          if pot <= 26.5:
                            if pot <= 24.5:
                                  return 24.0
                            else:
                                  return 26.0
                          else:
                            if pot <= 28.5:
                                  return 28.0
                            else:
                                  return 30.0
                      else:
                        if pot <= 40.5:
                          if pot <= 34.5:
                            if card <= 0.9330589771270752:
                                  return 30.0
                            else:
                                  return 32.76923076923077
                          else:
                            if card <= 0.9342271089553833:
                                  return 34.36363636363637
                            else:
                                  return 38.03389830508475
                        else:
                          if pot <= 47.5:
                            if card <= 0.9320753514766693:
                                  return 32.4
                            else:
                                  return 43.77777777777778
                          else:
                            if pot <= 48.5:
                                  return 48.0
                            else:
                                  return 50.0
          else:
                return 0.0
  else:
    if pot <= 8.5:
      if card <= 0.2500012367963791:
        if role <= 0.5:
          if pot <= 7.5:
            if pot <= 4.5:
              if minbet <= 6.0:
                    return 4.0
              else:
                if card <= 0.1938825249671936:
                  if card <= 0.029940364882349968:
                        return 8.727272727272727
                  else:
                        return 8.0
                else:
                  if card <= 0.21689751744270325:
                        return 9.6
                  else:
                        return 8.0
            else:
              if minbet <= 6.0:
                    return 8.0
              else:
                if card <= 0.18767773360013962:
                      return 8.0
                else:
                      return 8.8
          else:
            if minbet <= 6.0:
                  return 0.0
            else:
              if card <= 0.2162269651889801:
                if card <= 0.04899861849844456:
                  if card <= 0.027286484837532043:
                        return 8.0
                  else:
                        return 8.8
                else:
                      return 8.0
              else:
                    return 8.8
        else:
          if pot <= 4.5:
            if minbet <= 6.0:
                  return 4.0
            else:
                  return 8.0
          else:
            if minbet <= 6.0:
                  return 8.0
            else:
              if card <= 0.15558332204818726:
                    return 8.0
              else:
                if card <= 0.201274573802948:
                      return 8.8
                else:
                      return 8.0
      else:
        if pot <= 4.5:
          if minbet <= 6.0:
                return 4.0
          else:
            if card <= 0.8424232602119446:
              if card <= 0.2680303156375885:
                    return 8.666666666666666
              else:
                if role <= 0.5:
                      return 8.0
                else:
                  if pot <= 3.5:
                        return 8.0
                  else:
                    if card <= 0.6133480072021484:
                      if card <= 0.4638011157512665:
                            return 8.0
                      else:
                            return 8.842105263157896
                    else:
                          return 8.0
            else:
              if card <= 0.8604893088340759:
                    return 9.6
              else:
                if pot <= 2.5:
                      return 8.421052631578947
                else:
                      return 8.0
        else:
          if minbet <= 6.0:
                return 8.0
          else:
            if card <= 0.9503732919692993:
              if card <= 0.5756045877933502:
                    return 8.0
              else:
                if card <= 0.5872866809368134:
                      return 8.8
                else:
                  if pot <= 7.5:
                        return 8.0
                  else:
                    if card <= 0.8680557310581207:
                      if role <= 0.5:
                            return 8.0
                      else:
                        if card <= 0.7174916863441467:
                          if card <= 0.6833613216876984:
                                return 8.0
                          else:
                                return 9.6
                        else:
                              return 8.0
                    else:
                      if card <= 0.8937363922595978:
                            return 8.842105263157896
                      else:
                            return 8.0
            else:
                  return 8.842105263157896
    else:
      if pot <= 20.5:
        if card <= 0.47702358663082123:
          if card <= 0.25000129640102386:
            if role <= 0.5:
              if pot <= 15.5:
                    return 16.0
              else:
                if myscore <= 183.5:
                  if myscore <= 16.5:
                    if card <= 0.04882137104868889:
                          return 3.2
                    else:
                          return 0.0
                  else:
                        return 0.0
                else:
                  if card <= 0.19360096007585526:
                    if card <= 0.10931970551609993:
                          return 0.0
                    else:
                          return 0.8421052631578947
                  else:
                        return 3.2
            else:
              if minbet <= 6.0:
                if card <= 0.12066550925374031:
                  if pot <= 15.5:
                    if card <= 0.11124822124838829:
                      if card <= 0.09020309522747993:
                            return 8.0
                      else:
                        if card <= 0.09034617245197296:
                              return 8.4
                        else:
                          if card <= 0.09540805593132973:
                            if card <= 0.09527211263775826:
                                  return 8.0
                            else:
                                  return 8.4
                          else:
                                return 8.0
                    else:
                      if card <= 0.11148250102996826:
                            return 8.4
                      else:
                        if oppscore <= 50.5:
                          if myscore <= 156.5:
                            if card <= 0.11566521227359772:
                                  return 8.8
                            else:
                                  return 8.0
                          else:
                                return 8.0
                        else:
                          if myscore <= 105.5:
                                return 8.0
                          else:
                            if myscore <= 107.5:
                                  return 8.307692307692308
                            else:
                                  return 8.0
                  else:
                    if card <= 0.07689644023776054:
                          return 8.0
                    else:
                      if card <= 0.08035662770271301:
                        if myscore <= 122.5:
                          if pot <= 18.0:
                            if oppscore <= 114.0:
                                  return 9.6
                            else:
                                  return 9.6
                          else:
                                return 8.0
                        else:
                              return 8.0
                      else:
                        if card <= 0.1025962084531784:
                              return 8.0
                        else:
                          if card <= 0.10341909900307655:
                                return 8.8
                          else:
                            if myscore <= 92.5:
                                  return 8.096385542168674
                            else:
                                  return 8.0
                else:
                  if oppscore <= 18.5:
                    if oppscore <= 17.5:
                      if myscore <= 187.5:
                        if card <= 0.21283923089504242:
                              return 8.0
                        else:
                          if card <= 0.22165916115045547:
                                return 8.4
                          else:
                                return 8.0
                      else:
                        if card <= 0.22628659009933472:
                          if card <= 0.19158200174570084:
                            if card <= 0.1542210578918457:
                                  return 8.0
                            else:
                                  return 8.5
                          else:
                                return 9.666666666666666
                        else:
                              return 8.0
                    else:
                      if card <= 0.2104351595044136:
                        if card <= 0.14979705959558487:
                              return 9.2
                        else:
                              return 9.090909090909092
                      else:
                            return 8.333333333333334
                  else:
                    if myscore <= 12.5:
                      if card <= 0.17021186649799347:
                            return 8.0
                      else:
                        if card <= 0.21863582730293274:
                          if card <= 0.20398540794849396:
                                return 8.4
                          else:
                                return 9.2
                        else:
                              return 8.307692307692308
                    else:
                      if pot <= 15.5:
                        if oppscore <= 23.5:
                          if oppscore <= 21.5:
                            if card <= 0.1990317851305008:
                                  return 8.0
                            else:
                                  return 8.181818181818182
                          else:
                            if card <= 0.1562664657831192:
                                  return 8.0
                            else:
                                  return 8.545454545454545
                        else:
                          if myscore <= 45.5:
                            if oppscore <= 160.5:
                                  return 8.02127659574468
                            else:
                                  return 8.0
                          else:
                            if card <= 0.12090479210019112:
                                  return 8.4
                            else:
                                  return 8.050139275766016
                      else:
                        if myscore <= 20.5:
                          if card <= 0.1660722717642784:
                                return 9.2
                          else:
                                return 8.533333333333333
                        else:
                          if card <= 0.22424832731485367:
                            if oppscore <= 24.5:
                                  return 8.296296296296296
                            else:
                                  return 8.063604240282686
                          else:
                            if oppscore <= 37.0:
                                  return 8.96
                            else:
                                  return 8.18909090909091
              else:
                if pot <= 17.5:
                      return 16.0
                else:
                  if pot <= 18.5:
                        return 18.133333333333333
                  else:
                    if card <= 0.11445681378245354:
                          return 16.0
                    else:
                      if card <= 0.15479470789432526:
                            return 18.4
                      else:
                            return 16.0
          else:
            if minbet <= 6.0:
              if pot <= 16.5:
                if card <= 0.3546112924814224:
                  if pot <= 12.5:
                    if card <= 0.31331463158130646:
                      if pot <= 10.5:
                        if role <= 0.5:
                              return 9.411764705882353
                        else:
                              return 8.666666666666666
                      else:
                        if role <= 0.5:
                          if oppscore <= 12.5:
                                return 9.142857142857142
                          else:
                            if myscore <= 132.5:
                                  return 8.11092091749401
                            else:
                                  return 8.190127970749543
                        else:
                          if myscore <= 12.5:
                                return 8.571428571428571
                          else:
                            if myscore <= 152.5:
                                  return 8.056514913657772
                            else:
                                  return 8.113590263691684
                    else:
                      if oppscore <= 187.5:
                        if role <= 0.5:
                          if myscore <= 186.5:
                            if myscore <= 62.5:
                                  return 8.164948453608247
                            else:
                                  return 8.293680297397769
                          else:
                            if pot <= 11.0:
                                  return 8.4
                            else:
                                  return 9.6
                        else:
                          if card <= 0.31366583704948425:
                                return 8.75
                          else:
                            if card <= 0.31569381058216095:
                                  return 8.037383177570094
                            else:
                                  return 8.198653198653199
                      else:
                        if role <= 0.5:
                              return 10.0
                        else:
                              return 8.4
                  else:
                    if pot <= 15.5:
                      if card <= 0.2986907958984375:
                            return 8.533333333333333
                      else:
                            return 15.2
                    else:
                      if oppscore <= 37.0:
                        if card <= 0.2710001915693283:
                          if card <= 0.25858375430107117:
                                return 8.8
                          else:
                                return 8.0
                        else:
                          if oppscore <= 19.5:
                                return 8.0
                          else:
                            if role <= 0.5:
                                  return 8.816326530612244
                            else:
                                  return 9.517241379310345
                      else:
                        if oppscore <= 178.5:
                          if myscore <= 139.5:
                            if card <= 0.32524867355823517:
                                  return 8.192
                            else:
                                  return 8.341232227488153
                          else:
                            if myscore <= 144.5:
                                  return 8.875
                            else:
                                  return 8.266666666666667
                        else:
                          if role <= 0.5:
                                return 10.133333333333333
                          else:
                                return 8.0
                else:
                  if card <= 0.4607863426208496:
                    if role <= 0.5:
                      if card <= 0.4226800948381424:
                        if myscore <= 13.5:
                          if card <= 0.3893275260925293:
                                return 10.4
                          else:
                                return 8.842105263157896
                        else:
                          if card <= 0.3548748940229416:
                                return 9.333333333333334
                          else:
                            if card <= 0.41258928179740906:
                                  return 8.465496513584997
                            else:
                                  return 8.344632768361581
                      else:
                        if oppscore <= 15.5:
                          if card <= 0.45009176433086395:
                                return 8.941176470588236
                          else:
                                return 10.8
                        else:
                          if myscore <= 16.5:
                            if card <= 0.44337016344070435:
                                  return 9.73913043478261
                            else:
                                  return 9.0
                          else:
                            if myscore <= 40.5:
                                  return 8.38
                            else:
                                  return 8.629558541266794
                    else:
                      if pot <= 9.5:
                            return 10.4
                      else:
                        if card <= 0.35568666458129883:
                          if pot <= 13.0:
                            if oppscore <= 89.0:
                                  return 9.333333333333334
                            else:
                                  return 8.0
                          else:
                                return 11.333333333333334
                        else:
                          if oppscore <= 34.5:
                            if pot <= 12.5:
                                  return 8.445396145610278
                            else:
                                  return 9.181818181818182
                          else:
                            if card <= 0.4128696471452713:
                                  return 8.26460005535566
                            else:
                                  return 8.373641304347826
                  else:
                    if card <= 0.4738371819257736:
                      if card <= 0.4608960896730423:
                        if role <= 0.5:
                              return 10.545454545454545
                        else:
                              return 8.923076923076923
                      else:
                        if pot <= 12.5:
                          if card <= 0.46861758828163147:
                            if card <= 0.4679487496614456:
                                  return 8.727699530516432
                            else:
                                  return 8.294736842105262
                          else:
                            if card <= 0.46872252225875854:
                                  return 10.0
                            else:
                                  return 8.867226890756303
                        else:
                          if myscore <= 159.5:
                            if card <= 0.462376669049263:
                                  return 8.88888888888889
                            else:
                                  return 8.25263157894737
                          else:
                            if myscore <= 167.0:
                                  return 9.882352941176471
                            else:
                                  return 8.0
                    else:
                      if oppscore <= 57.5:
                        if card <= 0.4747961163520813:
                          if role <= 0.5:
                                return 11.0
                          else:
                                return 9.538461538461538
                        else:
                          if card <= 0.4765801876783371:
                            if myscore <= 145.5:
                                  return 10.0
                            else:
                                  return 8.837209302325581
                          else:
                                return 9.777777777777779
                      else:
                        if card <= 0.47663141787052155:
                          if card <= 0.47649990022182465:
                            if oppscore <= 171.5:
                                  return 8.917808219178083
                            else:
                                  return 9.866666666666667
                          else:
                                return 10.133333333333333
                        else:
                          if role <= 0.5:
                                return 8.8
                          else:
                            if card <= 0.4768461436033249:
                                  return 8.0
                            else:
                                  return 8.4
              else:
                if oppscore <= 42.5:
                  if role <= 0.5:
                    if card <= 0.3446716070175171:
                      if card <= 0.25925731658935547:
                            return 12.8
                      else:
                        if card <= 0.31358250975608826:
                          if card <= 0.2769412249326706:
                                return 10.181818181818182
                          else:
                                return 8.0
                        else:
                              return 11.0
                    else:
                      if card <= 0.36228668689727783:
                            return 16.0
                      else:
                        if card <= 0.45409853756427765:
                          if myscore <= 172.5:
                            if myscore <= 161.5:
                                  return 10.0
                            else:
                                  return 13.142857142857142
                          else:
                            if card <= 0.4197845757007599:
                                  return 10.823529411764707
                            else:
                                  return 8.0
                        else:
                              return 13.0
                  else:
                    if card <= 0.411700114607811:
                      if card <= 0.3260727673768997:
                        if myscore <= 176.5:
                              return 11.0
                        else:
                              return 9.2
                      else:
                            return 8.0
                    else:
                      if myscore <= 173.5:
                            return 9.2
                      else:
                            return 12.285714285714286
                else:
                  if card <= 0.32865646481513977:
                    if myscore <= 123.5:
                      if oppscore <= 177.0:
                        if card <= 0.3252677172422409:
                          if oppscore <= 126.5:
                                return 8.0
                          else:
                            if myscore <= 69.5:
                                  return 8.148148148148149
                            else:
                                  return 10.181818181818182
                        else:
                              return 9.090909090909092
                      else:
                            return 9.6
                    else:
                      if oppscore <= 59.5:
                        if card <= 0.2623984068632126:
                              return 9.2
                        else:
                              return 8.0
                      else:
                        if myscore <= 137.5:
                          if card <= 0.2860107570886612:
                            if role <= 0.5:
                                  return 12.0
                            else:
                                  return 8.0
                          else:
                            if card <= 0.30864502489566803:
                                  return 8.0
                            else:
                                  return 9.2
                        else:
                              return 11.272727272727273
                  else:
                    if myscore <= 19.5:
                      if card <= 0.41217853128910065:
                            return 9.6
                      else:
                            return 15.2
                    else:
                      if role <= 0.5:
                        if myscore <= 120.5:
                          if card <= 0.4703260064125061:
                            if card <= 0.34481437504291534:
                                  return 11.5
                            else:
                                  return 9.186311787072244
                          else:
                                return 12.285714285714286
                        else:
                          if oppscore <= 53.5:
                            if card <= 0.4396887570619583:
                                  return 9.0
                            else:
                                  return 10.4
                          else:
                            if card <= 0.44922272861003876:
                                  return 11.411764705882353
                            else:
                                  return 8.8
                      else:
                        if card <= 0.44011756777763367:
                          if myscore <= 132.5:
                            if oppscore <= 108.5:
                                  return 8.25
                            else:
                                  return 9.07865168539326
                          else:
                            if oppscore <= 55.5:
                                  return 8.75
                            else:
                                  return 10.482758620689655
                        else:
                          if card <= 0.4479421228170395:
                                return 12.0
                          else:
                            if myscore <= 110.5:
                                  return 10.297872340425531
                            else:
                                  return 8.352941176470589
            else:
              if pot <= 16.5:
                    return 16.0
              else:
                if card <= 0.43249835073947906:
                  if pot <= 18.5:
                    if card <= 0.31490324437618256:
                          return 16.8
                    else:
                          return 16.5
                  else:
                    if card <= 0.35170088708400726:
                      if card <= 0.29653318226337433:
                            return 18.4
                      else:
                            return 16.0
                    else:
                      if card <= 0.38323062658309937:
                            return 19.2
                      else:
                            return 18.181818181818183
                else:
                      return 21.77777777777778
        else:
          if minbet <= 6.0:
            if card <= 0.6312626302242279:
              if card <= 0.546318918466568:
                if card <= 0.4944349378347397:
                  if oppscore <= 14.5:
                    if oppscore <= 12.5:
                      if card <= 0.48717907071113586:
                            return 10.4
                      else:
                            return 11.2
                    else:
                          return 12.0
                  else:
                    if oppscore <= 177.5:
                      if oppscore <= 73.5:
                        if card <= 0.484128937125206:
                          if pot <= 18.0:
                            if card <= 0.48122698068618774:
                                  return 9.49090909090909
                            else:
                                  return 8.878048780487806
                          else:
                                return 11.333333333333334
                        else:
                          if myscore <= 144.5:
                            if myscore <= 128.5:
                                  return 8.75
                            else:
                                  return 10.339622641509434
                          else:
                            if pot <= 19.5:
                                  return 9.721115537848606
                            else:
                                  return 8.0
                      else:
                        if pot <= 14.0:
                          if card <= 0.4855789542198181:
                            if oppscore <= 124.5:
                                  return 9.24009324009324
                            else:
                                  return 8.917293233082706
                          else:
                            if oppscore <= 160.5:
                                  return 9.484162895927602
                            else:
                                  return 10.0
                        else:
                          if pot <= 18.0:
                            if card <= 0.478317454457283:
                                  return 10.666666666666666
                            else:
                                  return 8.475247524752476
                          else:
                            if card <= 0.48429329693317413:
                                  return 11.5
                            else:
                                  return 8.705882352941176
                    else:
                      if pot <= 14.5:
                        if card <= 0.48272377252578735:
                          if role <= 0.5:
                                return 10.153846153846153
                          else:
                                return 8.727272727272727
                        else:
                          if card <= 0.4877912849187851:
                                return 10.8
                          else:
                            if myscore <= 15.0:
                                  return 10.8
                            else:
                                  return 9.538461538461538
                      else:
                            return 12.727272727272727
                else:
                  if pot <= 15.5:
                    if card <= 0.5103738605976105:
                      if card <= 0.49509552121162415:
                        if oppscore <= 93.5:
                          if role <= 0.5:
                                return 10.31578947368421
                          else:
                            if card <= 0.4947345107793808:
                                  return 11.666666666666666
                            else:
                                  return 10.8
                        else:
                          if myscore <= 85.0:
                            if card <= 0.4946213364601135:
                                  return 10.0
                            else:
                                  return 11.047619047619047
                          else:
                                return 9.647058823529411
                      else:
                        if myscore <= 97.5:
                          if card <= 0.4994800090789795:
                            if card <= 0.49901194870471954:
                                  return 9.716738197424892
                            else:
                                  return 8.689655172413794
                          else:
                            if card <= 0.5102215111255646:
                                  return 9.976311336717428
                            else:
                                  return 8.4
                        else:
                          if oppscore <= 70.5:
                            if card <= 0.5051750540733337:
                                  return 9.749333333333333
                            else:
                                  return 10.071428571428571
                          else:
                            if role <= 0.5:
                                  return 10.457627118644067
                            else:
                                  return 10.07531380753138
                    else:
                      if oppscore <= 183.5:
                        if card <= 0.5265681445598602:
                          if card <= 0.5264862179756165:
                            if card <= 0.5104867219924927:
                                  return 11.428571428571429
                            else:
                                  return 10.22655048692978
                          else:
                                return 8.8
                        else:
                          if oppscore <= 112.5:
                            if card <= 0.5460347831249237:
                                  return 10.483130904183536
                            else:
                                  return 9.333333333333334
                          else:
                            if oppscore <= 113.5:
                                  return 9.4
                            else:
                                  return 10.314553990610328
                      else:
                        if oppscore <= 185.5:
                              return 11.777777777777779
                        else:
                          if card <= 0.5275412201881409:
                                return 11.2
                          else:
                            if role <= 0.5:
                                  return 10.0
                            else:
                                  return 11.0
                  else:
                    if myscore <= 20.5:
                      if pot <= 16.5:
                            return 13.090909090909092
                      else:
                            return 18.8
                    else:
                      if pot <= 16.5:
                        if oppscore <= 16.5:
                              return 12.571428571428571
                        else:
                          if role <= 0.5:
                            if myscore <= 163.5:
                                  return 9.090909090909092
                            else:
                                  return 10.580645161290322
                          else:
                            if card <= 0.539293646812439:
                                  return 8.597014925373134
                            else:
                                  return 9.209302325581396
                      else:
                        if oppscore <= 20.5:
                              return 16.0
                        else:
                          if myscore <= 149.0:
                            if myscore <= 140.5:
                                  return 10.218009478672986
                            else:
                                  return 8.521739130434783
                          else:
                            if card <= 0.505787581205368:
                                  return 9.5
                            else:
                                  return 13.73913043478261
              else:
                if pot <= 15.5:
                  if card <= 0.6028433442115784:
                    if card <= 0.5756925046443939:
                      if role <= 0.5:
                        if pot <= 11.5:
                              return 11.789473684210526
                        else:
                          if card <= 0.5470908284187317:
                            if card <= 0.5469378530979156:
                                  return 11.176470588235293
                            else:
                                  return 12.0
                          else:
                            if card <= 0.5473964214324951:
                                  return 10.222222222222221
                            else:
                                  return 10.884834663625998
                      else:
                        if card <= 0.5640848875045776:
                          if oppscore <= 26.5:
                            if oppscore <= 17.5:
                                  return 11.5
                            else:
                                  return 11.0
                          else:
                            if myscore <= 163.5:
                                  return 10.631693989071039
                            else:
                                  return 9.485714285714286
                        else:
                          if myscore <= 72.5:
                            if card <= 0.5672027468681335:
                                  return 11.2
                            else:
                                  return 10.387596899224807
                          else:
                            if myscore <= 75.5:
                                  return 11.578947368421053
                            else:
                                  return 10.94646680942184
                    else:
                      if card <= 0.6027385890483856:
                        if oppscore <= 179.5:
                          if myscore <= 25.5:
                            if role <= 0.5:
                                  return 11.2
                            else:
                                  return 9.647058823529411
                          else:
                            if card <= 0.5768714249134064:
                                  return 11.394736842105264
                            else:
                                  return 11.06598334401025
                        else:
                          if card <= 0.5863974392414093:
                            if oppscore <= 186.5:
                                  return 12.0
                            else:
                                  return 9.666666666666666
                          else:
                            if oppscore <= 185.5:
                                  return 11.2
                            else:
                                  return 12.6
                      else:
                            return 9.666666666666666
                  else:
                    if oppscore <= 99.5:
                      if card <= 0.6209698617458344:
                        if card <= 0.6202668249607086:
                          if oppscore <= 12.5:
                                return 12.0
                          else:
                            if card <= 0.6199898719787598:
                                  return 11.44486692015209
                            else:
                                  return 12.0
                        else:
                          if oppscore <= 81.5:
                            if card <= 0.6206277906894684:
                                  return 11.529411764705882
                            else:
                                  return 10.76923076923077
                          else:
                                return 10.461538461538462
                      else:
                        if card <= 0.6311995983123779:
                          if myscore <= 145.5:
                            if myscore <= 109.5:
                                  return 11.777777777777779
                            else:
                                  return 11.547368421052632
                          else:
                            if card <= 0.6287986040115356:
                                  return 11.72340425531915
                            else:
                                  return 12.0
                        else:
                              return 10.8
                    else:
                      if card <= 0.617077499628067:
                        if card <= 0.6141857206821442:
                          if card <= 0.6034527122974396:
                            if oppscore <= 150.0:
                                  return 10.222222222222221
                            else:
                                  return 12.0
                          else:
                            if card <= 0.6044885814189911:
                                  return 11.636363636363637
                            else:
                                  return 11.228668941979523
                        else:
                          if myscore <= 50.5:
                            if role <= 0.5:
                                  return 10.857142857142858
                            else:
                                  return 9.904761904761905
                          else:
                            if card <= 0.6145623028278351:
                                  return 10.181818181818182
                            else:
                                  return 11.166666666666666
                      else:
                        if myscore <= 25.5:
                          if card <= 0.6205248236656189:
                                return 11.272727272727273
                          else:
                            if card <= 0.6274233162403107:
                                  return 12.0
                            else:
                                  return 11.666666666666666
                        else:
                          if myscore <= 29.5:
                                return 10.588235294117647
                          else:
                            if card <= 0.6184816360473633:
                                  return 11.710144927536232
                            else:
                                  return 11.382475660639777
                else:
                  if oppscore <= 20.5:
                    if card <= 0.6046936511993408:
                      if card <= 0.5619717240333557:
                            return 9.6
                      else:
                        if card <= 0.581284761428833:
                              return 13.454545454545455
                        else:
                              return 10.0
                    else:
                          return 15.75
                  else:
                    if myscore <= 24.5:
                      if pot <= 16.5:
                        if role <= 0.5:
                              return 12.0
                        else:
                              return 8.0
                      else:
                            return 14.947368421052632
                    else:
                      if card <= 0.5944828689098358:
                        if card <= 0.5931957960128784:
                          if oppscore <= 139.5:
                            if pot <= 18.0:
                                  return 9.556164383561644
                            else:
                                  return 10.076923076923077
                          else:
                            if myscore <= 45.0:
                                  return 9.8
                            else:
                                  return 10.936708860759493
                        else:
                          if card <= 0.5941023528575897:
                                return 8.0
                          else:
                                return 8.8
                      else:
                        if card <= 0.5996581315994263:
                          if myscore <= 64.5:
                                return 13.333333333333334
                          else:
                            if card <= 0.5981819033622742:
                                  return 10.285714285714286
                            else:
                                  return 12.275862068965518
                        else:
                          if card <= 0.6062652170658112:
                            if card <= 0.602628082036972:
                                  return 9.975308641975309
                            else:
                                  return 8.976744186046512
                          else:
                            if myscore <= 143.5:
                                  return 10.204255319148936
                            else:
                                  return 11.26923076923077
            else:
              if pot <= 12.5:
                if card <= 0.6645710170269012:
                  if card <= 0.6407396793365479:
                    if card <= 0.6406221985816956:
                      if myscore <= 120.5:
                        if oppscore <= 110.5:
                          if card <= 0.6390200257301331:
                            if card <= 0.6382653415203094:
                                  return 11.607476635514018
                            else:
                                  return 12.0
                          else:
                            if card <= 0.6394734382629395:
                                  return 10.461538461538462
                            else:
                                  return 11.555555555555555
                        else:
                          if myscore <= 84.5:
                            if oppscore <= 118.5:
                                  return 11.428571428571429
                            else:
                                  return 11.798882681564246
                          else:
                                return 12.0
                      else:
                        if card <= 0.6399356126785278:
                          if card <= 0.6385544836521149:
                            if oppscore <= 63.5:
                                  return 11.868544600938968
                            else:
                                  return 11.758620689655173
                          else:
                                return 12.0
                        else:
                          if card <= 0.6402519643306732:
                                return 11.142857142857142
                          else:
                                return 12.0
                    else:
                          return 11.11111111111111
                  else:
                    if card <= 0.6643129885196686:
                      if myscore <= 127.5:
                        if oppscore <= 73.5:
                              return 11.333333333333334
                        else:
                          if oppscore <= 164.5:
                            if card <= 0.6589436829090118:
                                  return 11.836158192090396
                            else:
                                  return 11.92079207920792
                          else:
                            if myscore <= 22.5:
                                  return 11.870967741935484
                            else:
                                  return 12.0
                      else:
                        if myscore <= 153.5:
                          if card <= 0.6558022797107697:
                            if oppscore <= 60.5:
                                  return 12.0
                            else:
                                  return 11.972413793103449
                          else:
                            if card <= 0.6574749052524567:
                                  return 11.657142857142857
                            else:
                                  return 11.948717948717949
                        else:
                          if myscore <= 154.5:
                                return 11.428571428571429
                          else:
                            if role <= 0.5:
                                  return 11.957446808510639
                            else:
                                  return 11.847133757961783
                    else:
                      if oppscore <= 108.0:
                        if card <= 0.6644000709056854:
                              return 11.6
                        else:
                              return 12.0
                      else:
                            return 11.2
                else:
                  if card <= 0.7004381716251373:
                    if card <= 0.7003541588783264:
                      if oppscore <= 81.5:
                        if oppscore <= 27.5:
                          if card <= 0.6817663908004761:
                            if card <= 0.678991973400116:
                                  return 11.940298507462687
                            else:
                                  return 10.8
                          else:
                                return 12.0
                        else:
                          if oppscore <= 61.5:
                            if card <= 0.6674264073371887:
                                  return 11.9375
                            else:
                                  return 12.0
                          else:
                            if oppscore <= 63.5:
                                  return 11.868852459016393
                            else:
                                  return 11.97948717948718
                      else:
                        if myscore <= 117.5:
                          if role <= 0.5:
                            if myscore <= 112.5:
                                  return 11.981873111782477
                            else:
                                  return 11.870967741935484
                          else:
                            if card <= 0.6928357779979706:
                                  return 11.944167497507477
                            else:
                                  return 11.875862068965517
                        else:
                          if role <= 0.5:
                            if card <= 0.6783535182476044:
                                  return 11.6
                            else:
                                  return 12.0
                          else:
                                return 11.368421052631579
                    else:
                          return 11.2
                  else:
                    if card <= 0.8032105565071106:
                      if card <= 0.8031547963619232:
                        if oppscore <= 128.5:
                          if card <= 0.7148006856441498:
                            if card <= 0.7146987915039062:
                                  return 11.98489425981873
                            else:
                                  return 11.6
                          else:
                            if myscore <= 72.5:
                                  return 11.954022988505747
                            else:
                                  return 11.9939706067077
                        else:
                          if myscore <= 55.5:
                                return 12.0
                          else:
                            if myscore <= 56.5:
                                  return 11.951807228915662
                            else:
                                  return 12.0
                      else:
                            return 11.6
                    else:
                      if myscore <= 180.5:
                        if card <= 0.8231720626354218:
                          if card <= 0.8230787515640259:
                                return 12.0
                          else:
                                return 11.6
                        else:
                              return 12.0
                      else:
                        if oppscore <= 18.5:
                              return 12.0
                        else:
                          if card <= 0.8711743354797363:
                                return 11.6
                          else:
                                return 12.0
              else:
                if card <= 0.8144887387752533:
                  if card <= 0.7335428297519684:
                    if pot <= 16.5:
                      if card <= 0.67113196849823:
                        if myscore <= 108.5:
                          if oppscore <= 164.5:
                            if card <= 0.6683937311172485:
                                  return 9.614678899082568
                            else:
                                  return 10.782608695652174
                          else:
                            if card <= 0.6582189500331879:
                                  return 12.48
                            else:
                                  return 9.846153846153847
                        else:
                          if card <= 0.6700146198272705:
                            if role <= 0.5:
                                  return 11.16
                            else:
                                  return 10.3841059602649
                          else:
                                return 8.0
                      else:
                        if myscore <= 183.5:
                          if role <= 0.5:
                            if myscore <= 31.0:
                                  return 12.952380952380953
                            else:
                                  return 11.163444639718804
                          else:
                            if myscore <= 118.5:
                                  return 10.336088154269973
                            else:
                                  return 10.968325791855204
                        else:
                          if card <= 0.7031105756759644:
                                return 13.6
                          else:
                                return 13.6
                    else:
                      if oppscore <= 20.5:
                        if role <= 0.5:
                              return 15.0
                        else:
                          if card <= 0.6786076724529266:
                                return 16.0
                          else:
                                return 18.90909090909091
                      else:
                        if oppscore <= 138.5:
                          if myscore <= 148.5:
                            if card <= 0.6824056506156921:
                                  return 9.76271186440678
                            else:
                                  return 11.401069518716577
                          else:
                            if card <= 0.715254545211792:
                                  return 12.727272727272727
                            else:
                                  return 16.307692307692307
                        else:
                          if myscore <= 55.5:
                            if card <= 0.7030280232429504:
                                  return 12.857142857142858
                            else:
                                  return 15.304347826086957
                          else:
                                return 17.0
                  else:
                    if myscore <= 178.5:
                      if myscore <= 20.5:
                        if pot <= 17.5:
                          if card <= 0.7637617886066437:
                                return 14.545454545454545
                          else:
                                return 13.555555555555555
                        else:
                          if card <= 0.7783573567867279:
                                return 16.4
                          else:
                                return 17.6
                      else:
                        if card <= 0.8045998811721802:
                          if role <= 0.5:
                            if pot <= 18.0:
                                  return 12.419263456090652
                            else:
                                  return 13.847715736040609
                          else:
                            if card <= 0.7886265218257904:
                                  return 12.379518072289157
                            else:
                                  return 11.540229885057471
                        else:
                          if card <= 0.8098519742488861:
                            if card <= 0.8070503771305084:
                                  return 13.5
                            else:
                                  return 14.576271186440678
                          else:
                            if card <= 0.810358077287674:
                                  return 10.4
                            else:
                                  return 12.8
                    else:
                      if pot <= 17.0:
                        if myscore <= 182.5:
                              return 12.0
                        else:
                          if role <= 0.5:
                                return 14.4
                          else:
                            if card <= 0.7760135531425476:
                                  return 14.666666666666666
                            else:
                                  return 16.0
                      else:
                        if card <= 0.7817043960094452:
                              return 18.8
                        else:
                              return 18.8
                else:
                  if pot <= 16.5:
                    if card <= 0.8344195187091827:
                      if card <= 0.8181815147399902:
                        if myscore <= 124.0:
                          if card <= 0.816146582365036:
                            if card <= 0.8153235018253326:
                                  return 12.8
                            else:
                                  return 16.0
                          else:
                            if myscore <= 91.5:
                                  return 13.142857142857142
                            else:
                                  return 10.4
                        else:
                          if myscore <= 146.5:
                                return 16.0
                          else:
                                return 14.0
                      else:
                        if myscore <= 174.5:
                          if role <= 0.5:
                            if myscore <= 106.5:
                                  return 14.74698795180723
                            else:
                                  return 15.586206896551724
                          else:
                            if myscore <= 132.5:
                                  return 14.867924528301886
                            else:
                                  return 14.0
                        else:
                              return 16.0
                    else:
                      if card <= 0.874859094619751:
                        if card <= 0.8437050580978394:
                          if card <= 0.8431525826454163:
                            if oppscore <= 159.0:
                                  return 15.616438356164384
                            else:
                                  return 14.4
                          else:
                                return 14.285714285714286
                        else:
                          if card <= 0.8744085431098938:
                            if role <= 0.5:
                                  return 15.863945578231293
                            else:
                                  return 15.694656488549619
                          else:
                                return 14.4
                      else:
                        if card <= 0.905166894197464:
                          if card <= 0.904743105173111:
                            if myscore <= 41.5:
                                  return 15.6
                            else:
                                  return 15.954631379962192
                          else:
                                return 15.2
                        else:
                              return 16.0
                  else:
                    if card <= 0.8862656056880951:
                      if card <= 0.8308210670948029:
                        if myscore <= 163.0:
                          if oppscore <= 60.5:
                                return 19.076923076923077
                          else:
                            if card <= 0.8187848329544067:
                                  return 18.5
                            else:
                                  return 15.135135135135135
                        else:
                              return 14.461538461538462
                      else:
                        if card <= 0.8830634951591492:
                          if myscore <= 117.5:
                            if card <= 0.8469032943248749:
                                  return 16.5
                            else:
                                  return 18.742857142857144
                          else:
                            if role <= 0.5:
                                  return 19.675675675675677
                            else:
                                  return 18.472727272727273
                        else:
                              return 16.210526315789473
                    else:
                      if card <= 0.9047615826129913:
                        if myscore <= 85.5:
                          if myscore <= 62.5:
                                return 20.0
                          else:
                            if myscore <= 73.5:
                                  return 18.8
                            else:
                                  return 17.6
                        else:
                              return 20.0
                      else:
                            return 20.0
          else:
            if pot <= 16.5:
                  return 16.0
            else:
              if card <= 0.6061629951000214:
                if pot <= 18.5:
                      return 23.555555555555557
                else:
                  if pot <= 19.5:
                        return 20.363636363636363
                  else:
                    if card <= 0.5607975423336029:
                          return 23.333333333333332
                    else:
                          return 21.333333333333332
              else:
                if card <= 0.9344835877418518:
                  if role <= 0.5:
                    if card <= 0.7348339557647705:
                          return 24.0
                    else:
                      if card <= 0.8118070960044861:
                            return 24.88888888888889
                      else:
                            return 24.0
                  else:
                        return 24.0
                else:
                      return 24.8
      else:
        if card <= 0.9259720742702484:
          if minbet <= 6.0:
            if card <= 0.8024338483810425:
              if pot <= 36.5:
                if card <= 0.6505124270915985:
                  if card <= 0.5601697862148285:
                    if pot <= 35.5:
                      if card <= 0.2719110697507858:
                        if card <= 0.1919330134987831:
                              return 8.0
                        else:
                          if card <= 0.20083197951316833:
                                return 9.6
                          else:
                            if oppscore <= 72.5:
                                  return 8.170212765957446
                            else:
                                  return 8.0
                      else:
                        if pot <= 28.5:
                          if oppscore <= 74.5:
                            if myscore <= 134.5:
                                  return 10.507462686567164
                            else:
                                  return 8.91566265060241
                          else:
                            if myscore <= 112.5:
                                  return 8.621794871794872
                            else:
                                  return 8.0
                        else:
                          if pot <= 32.5:
                                return 8.0
                          else:
                            if card <= 0.3060828596353531:
                                  return 12.666666666666666
                            else:
                                  return 8.311111111111112
                    else:
                      if card <= 0.3007363826036453:
                        if myscore <= 74.5:
                          if oppscore <= 145.5:
                                return 10.8
                          else:
                                return 8.0
                        else:
                              return 8.0
                      else:
                        if oppscore <= 100.5:
                          if oppscore <= 47.5:
                            if card <= 0.4660450667142868:
                                  return 8.0
                            else:
                                  return 10.8
                          else:
                            if card <= 0.34395381808280945:
                                  return 23.272727272727273
                            else:
                                  return 14.222222222222221
                        else:
                          if card <= 0.34153905510902405:
                                return 11.5
                          else:
                            if oppscore <= 131.5:
                                  return 9.217391304347826
                            else:
                                  return 8.0
                  else:
                    if oppscore <= 24.5:
                          return 19.789473684210527
                    else:
                      if pot <= 35.5:
                        if myscore <= 25.0:
                              return 15.272727272727273
                        else:
                          if myscore <= 163.5:
                            if role <= 0.5:
                                  return 8.788177339901479
                            else:
                                  return 9.608938547486034
                          else:
                            if pot <= 28.5:
                                  return 13.647058823529411
                            else:
                                  return 9.061224489795919
                      else:
                        if myscore <= 64.0:
                              return 8.0
                        else:
                          if myscore <= 152.0:
                            if card <= 0.6045605540275574:
                                  return 14.588235294117647
                            else:
                                  return 25.818181818181817
                          else:
                                return 10.545454545454545
                else:
                  if oppscore <= 167.5:
                    if pot <= 34.5:
                      if oppscore <= 29.5:
                        if pot <= 24.5:
                          if card <= 0.7275993227958679:
                            if pot <= 23.5:
                                  return 22.545454545454547
                            else:
                                  return 14.4
                          else:
                                return 21.866666666666667
                        else:
                          if card <= 0.679532527923584:
                                return 20.727272727272727
                          else:
                            if card <= 0.7381544411182404:
                                  return 28.0
                            else:
                                  return 24.75
                      else:
                        if card <= 0.7326157093048096:
                          if role <= 0.5:
                            if myscore <= 167.5:
                                  return 10.314720812182742
                            else:
                                  return 15.076923076923077
                          else:
                            if pot <= 26.0:
                                  return 11.705263157894738
                            else:
                                  return 15.098591549295774
                        else:
                          if pot <= 32.5:
                            if pot <= 26.0:
                                  return 13.797101449275363
                            else:
                                  return 16.6
                          else:
                                return 23.75
                    else:
                      if card <= 0.7615802884101868:
                        if myscore <= 154.5:
                          if myscore <= 118.0:
                            if card <= 0.6752749085426331:
                                  return 13.090909090909092
                            else:
                                  return 18.11111111111111
                          else:
                                return 26.666666666666668
                        else:
                          if card <= 0.7190611660480499:
                                return 10.153846153846153
                          else:
                                return 13.6
                      else:
                        if card <= 0.7777752876281738:
                              return 29.53846153846154
                        else:
                          if card <= 0.7932385802268982:
                                return 36.0
                          else:
                                return 30.4
                  else:
                    if card <= 0.7042034566402435:
                      if myscore <= 28.5:
                        if myscore <= 24.5:
                              return 20.8
                        else:
                              return 26.285714285714285
                      else:
                            return 10.857142857142858
                    else:
                      if pot <= 28.5:
                        if pot <= 24.5:
                          if card <= 0.7504630088806152:
                                return 22.4
                          else:
                                return 20.8
                        else:
                          if card <= 0.7616211771965027:
                                return 28.0
                          else:
                                return 24.363636363636363
                      else:
                        if card <= 0.7406140267848969:
                              return 29.6
                        else:
                              return 32.0
              else:
                if pot <= 48.5:
                  if pot <= 47.5:
                    if card <= 0.7459772825241089:
                      if myscore <= 42.5:
                        if card <= 0.6727034151554108:
                          if pot <= 41.5:
                                return 8.0
                          else:
                            if card <= 0.4070739448070526:
                                  return 8.0
                            else:
                                  return 10.571428571428571
                        else:
                          if card <= 0.7003559470176697:
                                return 14.4
                          else:
                                return 8.0
                      else:
                            return 8.0
                    else:
                      if card <= 0.7483788132667542:
                            return 15.2
                      else:
                        if card <= 0.7648057639598846:
                          if card <= 0.75645512342453:
                                return 8.0
                          else:
                            if oppscore <= 113.5:
                                  return 12.952380952380953
                            else:
                                  return 8.0
                        else:
                          if card <= 0.7829530239105225:
                            if card <= 0.7786070704460144:
                                  return 8.0
                            else:
                                  return 11.2
                          else:
                                return 8.0
                  else:
                    if role <= 0.5:
                      if card <= 0.4326854646205902:
                            return 8.0
                      else:
                        if card <= 0.7198084890842438:
                          if card <= 0.6819826066493988:
                            if oppscore <= 124.0:
                                  return 18.19607843137255
                            else:
                                  return 10.962962962962964
                          else:
                                return 28.0
                        else:
                              return 8.0
                    else:
                          return 8.0
                else:
                  if myscore <= 131.5:
                        return 8.0
                  else:
                    if card <= 0.7736099660396576:
                      if pot <= 67.5:
                        if pot <= 52.5:
                          if card <= 0.5567470192909241:
                                return 8.0
                          else:
                            if card <= 0.5968203544616699:
                                  return 12.4
                            else:
                                  return 8.0
                        else:
                              return 8.0
                      else:
                        if card <= 0.6488560736179352:
                              return 8.0
                        else:
                              return 12.285714285714286
                    else:
                      if oppscore <= 63.5:
                            return 8.0
                      else:
                            return 13.6
            else:
              if pot <= 40.5:
                if myscore <= 41.5:
                  if pot <= 28.5:
                    if pot <= 24.5:
                          return 24.0
                    else:
                          return 28.0
                  else:
                    if card <= 0.8127890825271606:
                          return 29.23076923076923
                    else:
                      if pot <= 32.5:
                        if card <= 0.8583561182022095:
                              return 29.6
                        else:
                              return 32.0
                      else:
                        if oppscore <= 161.5:
                              return 40.0
                        else:
                          if card <= 0.8466539084911346:
                                return 37.142857142857146
                          else:
                            if card <= 0.8678658902645111:
                                  return 33.6
                            else:
                                  return 36.75
                else:
                  if myscore <= 159.5:
                    if card <= 0.9007895290851593:
                      if pot <= 38.0:
                        if pot <= 34.0:
                          if card <= 0.8233705163002014:
                            if pot <= 30.0:
                                  return 19.076923076923077
                            else:
                                  return 12.0
                          else:
                            if pot <= 26.0:
                                  return 20.643356643356643
                            else:
                                  return 24.028985507246375
                        else:
                          if card <= 0.8473721742630005:
                                return 36.0
                          else:
                            if card <= 0.8640238046646118:
                                  return 30.4
                            else:
                                  return 36.0
                      else:
                        if card <= 0.8199668824672699:
                          if card <= 0.8141392767429352:
                                return 8.0
                          else:
                                return 11.2
                        else:
                          if myscore <= 139.5:
                            if role <= 0.5:
                                  return 14.808510638297872
                            else:
                                  return 20.444444444444443
                          else:
                            if oppscore <= 49.5:
                                  return 11.2
                            else:
                                  return 10.461538461538462
                    else:
                      if pot <= 30.0:
                        if pot <= 26.0:
                              return 24.0
                        else:
                              return 28.0
                      else:
                        if card <= 0.9124361276626587:
                          if oppscore <= 96.5:
                                return 27.428571428571427
                          else:
                                return 34.0
                        else:
                          if card <= 0.9214030802249908:
                                return 37.714285714285715
                          else:
                                return 33.6
                  else:
                    if pot <= 28.5:
                      if pot <= 24.5:
                        if myscore <= 175.5:
                              return 21.0
                        else:
                          if role <= 0.5:
                                return 24.0
                          else:
                                return 23.157894736842106
                      else:
                            return 28.0
                    else:
                      if pot <= 32.5:
                        if pot <= 31.5:
                              return 32.0
                        else:
                              return 27.2
                      else:
                        if card <= 0.8536472320556641:
                          if card <= 0.8386001884937286:
                            if card <= 0.8244871199131012:
                                  return 38.0
                            else:
                                  return 34.8
                          else:
                                return 25.09090909090909
                        else:
                          if oppscore <= 36.5:
                                return 36.0
                          else:
                                return 40.0
              else:
                if pot <= 56.5:
                  if myscore <= 57.0:
                    if card <= 0.9110784232616425:
                      if card <= 0.8068042993545532:
                            return 12.0
                      else:
                        if pot <= 44.5:
                          if card <= 0.8630851805210114:
                                return 8.0
                          else:
                                return 11.6
                        else:
                              return 8.0
                    else:
                      if card <= 0.9171768426895142:
                            return 11.6
                      else:
                            return 15.6
                  else:
                    if card <= 0.8462074100971222:
                      if myscore <= 136.5:
                        if oppscore <= 86.5:
                          if card <= 0.8189379274845123:
                                return 26.181818181818183
                          else:
                                return 13.142857142857142
                        else:
                          if role <= 0.5:
                            if card <= 0.8197733461856842:
                                  return 16.0
                            else:
                                  return 11.6
                          else:
                                return 8.0
                      else:
                        if card <= 0.8367095291614532:
                              return 8.0
                        else:
                              return 13.0
                    else:
                      if myscore <= 144.5:
                        if pot <= 46.0:
                          if card <= 0.9044589996337891:
                            if oppscore <= 77.5:
                                  return 13.538461538461538
                            else:
                                  return 23.6
                          else:
                            if card <= 0.9160381257534027:
                                  return 34.18181818181818
                            else:
                                  return 44.0
                        else:
                          if card <= 0.8778070211410522:
                                return 31.636363636363637
                          else:
                            if card <= 0.8981601297855377:
                                  return 49.142857142857146
                            else:
                                  return 36.0
                      else:
                        if card <= 0.920669674873352:
                          if card <= 0.8574444651603699:
                                return 19.6
                          else:
                            if pot <= 52.5:
                                  return 13.018181818181818
                            else:
                                  return 8.0
                        else:
                              return 27.2
                else:
                  if card <= 0.9098516702651978:
                    if card <= 0.8557991683483124:
                          return 8.0
                    else:
                      if oppscore <= 116.5:
                        if pot <= 72.5:
                          if myscore <= 129.0:
                                return 34.18181818181818
                          else:
                            if pot <= 67.0:
                                  return 8.0
                            else:
                                  return 16.571428571428573
                        else:
                          if oppscore <= 101.5:
                            if card <= 0.8942990899085999:
                                  return 8.0
                            else:
                                  return 9.904761904761905
                          else:
                            if oppscore <= 104.5:
                                  return 20.4
                            else:
                                  return 8.0
                      else:
                            return 8.0
                  else:
                    if oppscore <= 93.5:
                      if myscore <= 112.0:
                            return 43.27272727272727
                      else:
                        if card <= 0.9210881888866425:
                              return 8.0
                        else:
                              return 18.90909090909091
                    else:
                      if pot <= 80.5:
                        if card <= 0.9197281897068024:
                          if myscore <= 71.5:
                                return 18.90909090909091
                          else:
                                return 22.0
                        else:
                              return 8.0
                      else:
                            return 8.0
          else:
            if card <= 0.5637210011482239:
              if card <= 0.4761413633823395:
                if minbet <= 12.0:
                  if card <= 0.34375250339508057:
                    if card <= 0.279303714632988:
                      if pot <= 47.5:
                        if role <= 0.5:
                          if myscore <= 41.0:
                            if oppscore <= 164.5:
                                  return 17.6
                            else:
                                  return 16.0
                          else:
                            if oppscore <= 99.0:
                                  return 16.193548387096776
                            else:
                                  return 16.0
                        else:
                          if card <= 0.1055254153907299:
                                return 16.0
                          else:
                            if card <= 0.10635554417967796:
                                  return 16.8
                            else:
                                  return 16.03955500618047
                      else:
                        if pot <= 49.0:
                          if card <= 0.17389531433582306:
                                return 16.0
                          else:
                                return 20.266666666666666
                        else:
                              return 16.0
                    else:
                      if card <= 0.2798038423061371:
                            return 18.4
                      else:
                        if myscore <= 29.5:
                          if card <= 0.3182104527950287:
                                return 17.6
                          else:
                                return 16.0
                        else:
                          if pot <= 40.5:
                            if pot <= 39.0:
                                  return 16.25486725663717
                            else:
                                  return 16.8
                          else:
                                return 16.0
                  else:
                    if myscore <= 161.5:
                      if myscore <= 38.5:
                        if pot <= 25.0:
                          if myscore <= 36.5:
                            if card <= 0.4635780304670334:
                                  return 16.715447154471544
                            else:
                                  return 18.133333333333333
                          else:
                                return 19.2
                        else:
                          if card <= 0.44143418967723846:
                                return 17.88235294117647
                          else:
                                return 24.727272727272727
                      else:
                        if card <= 0.43897952139377594:
                          if role <= 0.5:
                            if card <= 0.3475797772407532:
                                  return 18.0
                            else:
                                  return 16.69965477560414
                          else:
                            if pot <= 35.5:
                                  return 16.409448818897637
                            else:
                                  return 16.0
                        else:
                          if card <= 0.43942974507808685:
                                return 20.0
                          else:
                            if pot <= 50.0:
                                  return 16.9728
                            else:
                                  return 16.0
                    else:
                      if pot <= 25.0:
                        if card <= 0.46912655234336853:
                          if role <= 0.5:
                            if card <= 0.40445055067539215:
                                  return 17.29032258064516
                            else:
                                  return 16.266666666666666
                          else:
                            if card <= 0.4282947778701782:
                                  return 16.0
                            else:
                                  return 16.615384615384617
                        else:
                              return 19.333333333333332
                      else:
                        if oppscore <= 31.5:
                              return 25.333333333333332
                        else:
                          if card <= 0.38656409084796906:
                                return 21.6
                          else:
                                return 18.181818181818183
                else:
                  if card <= 0.22789599001407623:
                    if role <= 0.5:
                      if myscore <= 148.0:
                            return 0.0
                      else:
                            return 2.909090909090909
                    else:
                          return 32.0
                  else:
                    if card <= 0.25229670107364655:
                          return 25.6
                    else:
                          return 32.0
              else:
                if minbet <= 12.0:
                  if pot <= 31.5:
                    if card <= 0.5146717429161072:
                      if card <= 0.4957883954048157:
                        if oppscore <= 166.5:
                          if myscore <= 168.5:
                            if card <= 0.476939395070076:
                                  return 16.533333333333335
                            else:
                                  return 18.141263940520446
                          else:
                                return 19.764705882352942
                        else:
                              return 21.6
                      else:
                        if card <= 0.5133596360683441:
                          if myscore <= 131.5:
                            if card <= 0.5121297836303711:
                                  return 19.52820512820513
                            else:
                                  return 21.53846153846154
                          else:
                            if card <= 0.5029584169387817:
                                  return 19.586206896551722
                            else:
                                  return 17.2972972972973
                        else:
                          if myscore <= 127.5:
                                return 16.941176470588236
                          else:
                                return 18.4
                    else:
                      if card <= 0.5614886283874512:
                        if card <= 0.5270280838012695:
                          if card <= 0.5187243521213531:
                            if myscore <= 81.5:
                                  return 20.0
                            else:
                                  return 21.647058823529413
                          else:
                            if card <= 0.5205324292182922:
                                  return 18.105263157894736
                            else:
                                  return 19.514018691588785
                        else:
                          if card <= 0.5596449971199036:
                            if myscore <= 42.5:
                                  return 21.666666666666668
                            else:
                                  return 20.505175983436853
                          else:
                            if card <= 0.5608874559402466:
                                  return 18.434782608695652
                            else:
                                  return 20.363636363636363
                      else:
                        if card <= 0.5627252757549286:
                              return 23.384615384615383
                        else:
                              return 21.714285714285715
                  else:
                    if oppscore <= 157.5:
                      if oppscore <= 38.5:
                            return 24.444444444444443
                      else:
                        if card <= 0.5140092968940735:
                          if pot <= 71.0:
                            if card <= 0.509796530008316:
                                  return 16.528301886792452
                            else:
                                  return 21.0
                          else:
                            if pot <= 89.0:
                                  return 27.636363636363637
                            else:
                                  return 16.0
                        else:
                          if pot <= 49.0:
                            if card <= 0.5488713979721069:
                                  return 17.814432989690722
                            else:
                                  return 16.390243902439025
                          else:
                                return 16.0
                    else:
                          return 25.41176470588235
                else:
                  if card <= 0.5528789460659027:
                    if card <= 0.5352261066436768:
                          return 32.0
                    else:
                          return 33.6
                  else:
                        return 36.0
            else:
              if pot <= 40.5:
                if minbet <= 12.0:
                  if card <= 0.7996316850185394:
                    if pot <= 30.5:
                      if card <= 0.6248591840267181:
                        if card <= 0.6107213199138641:
                          if card <= 0.5647793710231781:
                                return 24.0
                          else:
                            if oppscore <= 49.5:
                                  return 22.515463917525775
                            else:
                                  return 21.714285714285715
                        else:
                          if myscore <= 34.5:
                                return 20.363636363636363
                          else:
                            if card <= 0.6244653165340424:
                                  return 22.85185185185185
                            else:
                                  return 20.8
                      else:
                        if card <= 0.647958368062973:
                          if card <= 0.6464706063270569:
                            if card <= 0.6394617259502411:
                                  return 23.11111111111111
                            else:
                                  return 23.649122807017545
                          else:
                            if oppscore <= 77.5:
                                  return 23.333333333333332
                            else:
                                  return 21.714285714285715
                        else:
                          if pot <= 24.5:
                            if card <= 0.6695284247398376:
                                  return 23.81449275362319
                            else:
                                  return 23.961202715809893
                          else:
                            if oppscore <= 29.5:
                                  return 30.4
                            else:
                                  return 24.533333333333335
                    else:
                      if myscore <= 159.5:
                        if myscore <= 40.5:
                          if pot <= 32.5:
                            if card <= 0.6754079759120941:
                                  return 20.266666666666666
                            else:
                                  return 25.6
                          else:
                                return 35.2
                        else:
                          if card <= 0.7361932694911957:
                            if myscore <= 110.5:
                                  return 18.696629213483146
                            else:
                                  return 17.545454545454547
                          else:
                            if card <= 0.7538527250289917:
                                  return 23.515151515151516
                            else:
                                  return 20.682926829268293
                      else:
                        if pot <= 32.5:
                          if card <= 0.712448000907898:
                                return 18.823529411764707
                          else:
                                return 24.470588235294116
                        else:
                          if card <= 0.6655319929122925:
                                return 35.63636363636363
                          else:
                                return 31.428571428571427
                  else:
                    if pot <= 24.5:
                          return 24.0
                    else:
                      if card <= 0.8321849703788757:
                        if myscore <= 47.0:
                              return 30.4
                        else:
                          if pot <= 39.5:
                            if card <= 0.824908435344696:
                                  return 24.627450980392158
                            else:
                                  return 30.0
                          else:
                                return 19.2
                      else:
                        if pot <= 33.5:
                          if card <= 0.847964733839035:
                            if role <= 0.5:
                                  return 27.733333333333334
                            else:
                                  return 31.058823529411764
                          else:
                            if card <= 0.8714566826820374:
                                  return 31.11111111111111
                            else:
                                  return 32.0
                        else:
                          if card <= 0.8922371864318848:
                            if card <= 0.874197781085968:
                                  return 35.2
                            else:
                                  return 30.4
                          else:
                                return 40.0
                else:
                  if oppscore <= 41.0:
                    if card <= 0.7802923619747162:
                          return 33.6
                    else:
                          return 33.23076923076923
                  else:
                    if oppscore <= 157.0:
                          return 32.0
                    else:
                          return 33.142857142857146
              else:
                if card <= 0.7604404389858246:
                  if pot <= 64.5:
                    if card <= 0.6948757469654083:
                      if pot <= 54.5:
                        if pot <= 47.5:
                          if card <= 0.6235122680664062:
                                return 41.6
                          else:
                                return 48.0
                        else:
                          if card <= 0.6433142125606537:
                            if pot <= 48.5:
                                  return 26.823529411764707
                            else:
                                  return 18.5
                          else:
                            if pot <= 48.5:
                                  return 32.0
                            else:
                                  return 48.0
                      else:
                        if card <= 0.6007288098335266:
                              return 16.0
                        else:
                          if card <= 0.6519605219364166:
                            if oppscore <= 94.5:
                                  return 24.8
                            else:
                                  return 19.076923076923077
                          else:
                                return 16.0
                    else:
                      if myscore <= 135.0:
                        if oppscore <= 131.5:
                          if card <= 0.7372924983501434:
                                return 39.27272727272727
                          else:
                                return 25.6
                        else:
                          if card <= 0.7252977192401886:
                                return 44.8
                          else:
                                return 52.30769230769231
                      else:
                        if pot <= 58.5:
                              return 46.666666666666664
                        else:
                              return 56.0
                  else:
                    if pot <= 73.0:
                      if myscore <= 80.0:
                        if card <= 0.6468831598758698:
                              return 16.0
                        else:
                              return 21.6
                      else:
                        if myscore <= 128.5:
                              return 32.8
                        else:
                              return 22.22222222222222
                    else:
                      if card <= 0.593903660774231:
                        if pot <= 87.5:
                              return 16.0
                        else:
                              return 30.545454545454547
                      else:
                            return 16.0
                else:
                  if pot <= 81.0:
                    if pot <= 49.0:
                      if card <= 0.7853046655654907:
                            return 38.15384615384615
                      else:
                        if role <= 0.5:
                          if oppscore <= 117.0:
                            if card <= 0.8423882126808167:
                                  return 38.15384615384615
                            else:
                                  return 45.333333333333336
                          else:
                                return 48.0
                        else:
                              return 48.0
                    else:
                      if card <= 0.8058980107307434:
                        if pot <= 74.0:
                          if card <= 0.7844474613666534:
                            if card <= 0.7712705135345459:
                                  return 61.6
                            else:
                                  return 63.27272727272727
                          else:
                                return 47.2
                        else:
                              return 26.666666666666668
                      else:
                        if pot <= 66.5:
                          if oppscore <= 72.0:
                            if pot <= 57.0:
                                  return 56.0
                            else:
                                  return 65.45454545454545
                          else:
                            if myscore <= 72.0:
                                  return 59.42857142857143
                            else:
                                  return 46.666666666666664
                        else:
                          if card <= 0.8711213767528534:
                            if myscore <= 115.5:
                                  return 61.64705882352941
                            else:
                                  return 76.44444444444444
                          else:
                            if pot <= 72.5:
                                  return 72.0
                            else:
                                  return 80.0
                  else:
                    if pot <= 88.5:
                      if oppscore <= 102.0:
                            return 20.5
                      else:
                        if oppscore <= 112.5:
                              return 38.15384615384615
                        else:
                              return 23.272727272727273
                    else:
                          return 16.0
        else:
          if pot <= 48.5:
            if pot <= 32.5:
              if pot <= 24.5:
                    return 24.0
              else:
                if pot <= 28.5:
                  if myscore <= 28.5:
                        return 29.454545454545453
                  else:
                    if myscore <= 168.5:
                          return 28.0
                    else:
                          return 28.705882352941178
                else:
                      return 32.0
            else:
              if pot <= 40.5:
                if pot <= 36.5:
                  if card <= 0.9475046098232269:
                        return 36.53333333333333
                  else:
                        return 36.0
                else:
                  if myscore <= 159.5:
                        return 40.0
                  else:
                    if oppscore <= 39.5:
                          return 40.0
                    else:
                          return 40.8
              else:
                if pot <= 44.5:
                  if minbet <= 6.0:
                        return 44.0
                  else:
                        return 48.0
                else:
                      return 48.0
          else:
            if pot <= 76.5:
              if pot <= 60.5:
                if pot <= 56.5:
                  if card <= 0.9339625835418701:
                        return 50.18181818181818
                  else:
                    if pot <= 52.5:
                      if oppscore <= 141.0:
                            return 52.0
                      else:
                            return 52.705882352941174
                    else:
                          return 56.0
                else:
                  if role <= 0.5:
                        return 60.0
                  else:
                    if card <= 0.9524966776371002:
                          return 61.2
                    else:
                          return 60.333333333333336
              else:
                if card <= 0.9276424050331116:
                      return 43.2
                else:
                  if pot <= 68.5:
                    if pot <= 64.5:
                          return 64.0
                    else:
                      if pot <= 66.5:
                            return 68.92307692307692
                      else:
                        if card <= 0.9485796093940735:
                              return 68.4
                        else:
                              return 68.0
                  else:
                    if pot <= 72.5:
                          return 72.0
                    else:
                      if card <= 0.9400517642498016:
                            return 76.0
                      else:
                        if card <= 0.9519914984703064:
                              return 76.8
                        else:
                              return 76.3076923076923
            else:
              if card <= 0.9291077554225922:
                    return 18.75
              else:
                if pot <= 89.5:
                  if pot <= 80.5:
                        return 80.0
                  else:
                    if card <= 0.9364272654056549:
                          return 78.4
                    else:
                      if pot <= 84.5:
                        if card <= 0.9520106315612793:
                              return 84.0
                        else:
                          if pot <= 83.5:
                                return 84.28571428571429
                          else:
                                return 85.2
                      else:
                        if pot <= 87.5:
                              return 88.0
                        else:
                              return 89.55555555555556
                else:
                  if pot <= 96.5:
                    if card <= 0.9362777471542358:
                          return 85.6
                    else:
                      if pot <= 92.5:
                        if card <= 0.9631130695343018:
                              return 92.53333333333333
                        else:
                              return 92.0
                      else:
                            return 96.0
                  else:
                    if card <= 0.9425273239612579:
                          return 100.0
                    else:
                          return 101.26315789473684
else:
  if oppscore <= 85.5:
    if myscore <= 148.5:
      if myscore <= 128.5:
        if oppscore <= 79.5:
          if oppscore <= 75.5:
            if oppscore <= 73.5:
              if minbet <= 1.5:
                if myscore <= 127.5:
                      return 127.0
                else:
                      return 128.0
              else:
                    return 128.0
            else:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if myscore <= 125.5:
                        return 125.0
                  else:
                        return 126.0
                else:
                      return 126.0
              else:
                    return 128.0
          else:
            if myscore <= 122.5:
              if minbet <= 3.0:
                if oppscore <= 78.5:
                      return 122.0
                else:
                  if minbet <= 1.5:
                        return 121.0
                  else:
                        return 122.0
              else:
                if minbet <= 6.0:
                      return 124.0
                else:
                      return 128.0
            else:
              if minbet <= 6.0:
                if minbet <= 1.5:
                  if oppscore <= 76.5:
                        return 124.0
                  else:
                        return 123.0
                else:
                      return 124.0
              else:
                    return 128.0
        else:
          if myscore <= 116.5:
            if minbet <= 6.0:
              if myscore <= 115.5:
                if minbet <= 1.5:
                      return 115.0
                else:
                      return 116.0
              else:
                    return 116.0
            else:
                  return 120.0
          else:
            if myscore <= 118.5:
              if minbet <= 3.0:
                if myscore <= 117.5:
                  if minbet <= 1.5:
                        return 117.0
                  else:
                        return 118.0
                else:
                      return 118.0
              else:
                    return 120.0
            else:
              if minbet <= 1.5:
                if myscore <= 119.5:
                      return 119.0
                else:
                      return 120.0
              else:
                    return 120.0
      else:
        if myscore <= 138.5:
          if oppscore <= 67.5:
            if oppscore <= 63.5:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if oppscore <= 62.5:
                        return 138.0
                  else:
                        return 137.0
                else:
                      return 138.0
              else:
                if minbet <= 6.0:
                      return 140.0
                else:
                      return 144.0
            else:
              if oppscore <= 65.5:
                if minbet <= 1.5:
                  if myscore <= 135.5:
                        return 135.0
                  else:
                        return 136.0
                else:
                      return 136.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if myscore <= 133.5:
                          return 133.0
                    else:
                          return 134.0
                  else:
                        return 134.0
                else:
                      return 136.0
          else:
            if minbet <= 6.0:
              if myscore <= 130.5:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if myscore <= 129.5:
                          return 129.0
                    else:
                          return 130.0
                  else:
                        return 130.0
                else:
                      return 132.0
              else:
                if minbet <= 1.5:
                  if myscore <= 131.5:
                        return 131.0
                  else:
                        return 132.0
                else:
                      return 132.0
            else:
              if pot <= 20.0:
                    return 136.0
              else:
                    return 136.8
        else:
          if oppscore <= 55.5:
            if minbet <= 6.0:
              if oppscore <= 53.5:
                if minbet <= 1.5:
                  if myscore <= 147.5:
                        return 147.0
                  else:
                        return 148.0
                else:
                      return 148.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if oppscore <= 54.5:
                          return 146.0
                    else:
                          return 145.0
                  else:
                        return 146.0
                else:
                      return 148.0
            else:
              if card <= 0.9806146025657654:
                    return 152.8
              else:
                    return 152.0
          else:
            if oppscore <= 59.5:
              if oppscore <= 57.5:
                if minbet <= 1.5:
                  if myscore <= 143.5:
                        return 143.0
                  else:
                        return 144.0
                else:
                      return 144.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if oppscore <= 58.5:
                          return 142.0
                    else:
                          return 141.0
                  else:
                        return 142.0
                else:
                      return 144.0
            else:
              if minbet <= 6.0:
                if minbet <= 1.5:
                  if oppscore <= 60.5:
                        return 140.0
                  else:
                        return 139.0
                else:
                      return 140.0
              else:
                    return 144.0
    else:
      if myscore <= 168.5:
        if myscore <= 158.5:
          if oppscore <= 47.5:
            if myscore <= 156.5:
              if minbet <= 6.0:
                if oppscore <= 45.5:
                  if minbet <= 1.5:
                    if myscore <= 155.5:
                          return 155.0
                    else:
                          return 156.0
                  else:
                        return 156.0
                else:
                  if minbet <= 3.0:
                    if pot <= 3.5:
                      if myscore <= 153.5:
                            return 153.0
                      else:
                            return 154.0
                    else:
                      if pot <= 4.5:
                            return 154.0
                      else:
                        if oppscore <= 46.5:
                              return 154.0
                        else:
                          if card <= 0.9809970557689667:
                                return 153.9
                          else:
                                return 153.94736842105263
                  else:
                        return 156.0
              else:
                    return 160.0
            else:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if myscore <= 157.5:
                        return 157.0
                  else:
                        return 158.0
                else:
                      return 158.0
              else:
                    return 160.0
          else:
            if myscore <= 150.5:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if oppscore <= 50.5:
                        return 150.0
                  else:
                        return 149.0
                else:
                      return 150.0
              else:
                    return 152.0
            else:
              if minbet <= 1.5:
                if myscore <= 151.5:
                      return 151.0
                else:
                      return 152.0
              else:
                    return 152.0
        else:
          if myscore <= 164.5:
            if myscore <= 160.5:
              if minbet <= 1.5:
                if myscore <= 159.5:
                      return 159.0
                else:
                      return 160.0
              else:
                    return 160.0
            else:
              if minbet <= 6.0:
                if myscore <= 162.5:
                  if minbet <= 3.0:
                    if pot <= 3.5:
                      if oppscore <= 38.5:
                            return 162.0
                      else:
                            return 161.0
                    else:
                          return 162.0
                  else:
                        return 164.0
                else:
                  if minbet <= 1.5:
                    if oppscore <= 36.5:
                          return 164.0
                    else:
                          return 163.0
                  else:
                        return 164.0
              else:
                    return 168.0
          else:
            if oppscore <= 33.5:
              if minbet <= 1.5:
                if oppscore <= 32.5:
                      return 168.0
                else:
                      return 167.0
              else:
                    return 168.0
            else:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if myscore <= 165.5:
                        return 165.0
                  else:
                        return 166.0
                else:
                      return 166.0
              else:
                    return 168.0
      else:
        if myscore <= 182.5:
          if myscore <= 176.5:
            if oppscore <= 27.5:
              if oppscore <= 25.5:
                if minbet <= 1.5:
                  if myscore <= 175.5:
                        return 175.0
                  else:
                        return 176.0
                else:
                      return 176.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if oppscore <= 26.5:
                          return 174.0
                    else:
                          return 173.0
                  else:
                        return 174.0
                else:
                      return 176.0
            else:
              if minbet <= 6.0:
                if oppscore <= 29.5:
                  if minbet <= 1.5:
                    if myscore <= 171.5:
                          return 171.0
                    else:
                          return 172.0
                  else:
                        return 172.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                      if myscore <= 169.5:
                            return 169.0
                      else:
                            return 170.0
                    else:
                          return 170.0
                  else:
                        return 172.0
              else:
                    return 176.0
          else:
            if myscore <= 180.5:
              if minbet <= 6.0:
                if oppscore <= 21.5:
                  if oppscore <= 20.5:
                        return 180.0
                  else:
                    if minbet <= 1.5:
                          return 179.0
                    else:
                          return 180.0
                else:
                  if minbet <= 3.0:
                    if oppscore <= 22.5:
                          return 178.0
                    else:
                      if minbet <= 1.5:
                            return 177.0
                      else:
                            return 178.0
                  else:
                        return 180.0
              else:
                    return 184.0
            else:
              if minbet <= 3.0:
                if myscore <= 181.5:
                  if minbet <= 1.5:
                        return 181.0
                  else:
                        return 182.0
                else:
                      return 182.0
              else:
                    return 184.0
        else:
          if myscore <= 189.5:
            if oppscore <= 15.5:
              if myscore <= 186.5:
                if minbet <= 3.0:
                  if oppscore <= 14.5:
                        return 186.0
                  else:
                    if minbet <= 1.5:
                          return 185.0
                    else:
                          return 186.0
                else:
                  if pot <= 10.0:
                        return 188.0
                  else:
                        return 189.0909090909091
              else:
                if oppscore <= 11.5:
                  if minbet <= 1.5:
                        return 189.0
                  else:
                    if card <= 0.9914244711399078:
                          return 190.4
                    else:
                          return 190.4
                else:
                  if pot <= 10.0:
                    if myscore <= 187.5:
                      if minbet <= 1.5:
                            return 187.0
                      else:
                            return 188.0
                    else:
                          return 188.0
                  else:
                        return 189.11111111111111
            else:
              if minbet <= 1.5:
                if myscore <= 183.5:
                      return 183.0
                else:
                      return 184.0
              else:
                    return 184.0
          else:
            if oppscore <= 6.5:
              if myscore <= 196.5:
                if minbet <= 6.0:
                  if oppscore <= 5.5:
                    if oppscore <= 4.5:
                          return 196.0
                    else:
                      if minbet <= 1.5:
                            return 195.0
                      else:
                            return 196.0
                  else:
                    if pot <= 5.0:
                          return 194.0
                    else:
                      if card <= 0.9901058673858643:
                            return 194.72727272727272
                      else:
                            return 195.0
                else:
                      return 200.0
              else:
                if minbet <= 3.0:
                  if oppscore <= 1.5:
                        return 199.46666666666667
                  else:
                    if oppscore <= 2.5:
                          return 198.0
                    else:
                          return 197.35294117647058
                else:
                      return 200.0
            else:
              if myscore <= 192.5:
                if myscore <= 191.5:
                  if minbet <= 3.0:
                    if myscore <= 190.5:
                          return 190.0
                    else:
                      if pot <= 2.5:
                            return 191.0
                      else:
                            return 191.4
                  else:
                        return 192.0
                else:
                      return 192.0
              else:
                if minbet <= 1.5:
                      return 193.0
                else:
                  if card <= 0.9820673167705536:
                        return 194.6
                  else:
                        return 195.0
  else:
    if myscore <= 76.5:
      if oppscore <= 151.5:
        if oppscore <= 135.5:
          if myscore <= 70.5:
            if myscore <= 68.5:
              if minbet <= 6.0:
                if oppscore <= 133.5:
                  if minbet <= 1.5:
                    if oppscore <= 132.5:
                          return 68.0
                    else:
                          return 67.0
                  else:
                        return 68.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                      if oppscore <= 134.5:
                            return 66.0
                      else:
                            return 65.0
                    else:
                          return 66.0
                  else:
                        return 68.0
              else:
                    return 72.0
            else:
              if minbet <= 3.0:
                if minbet <= 1.5:
                  if myscore <= 69.5:
                        return 69.0
                  else:
                        return 70.0
                else:
                      return 70.0
              else:
                    return 72.0
          else:
            if oppscore <= 127.5:
              if oppscore <= 125.5:
                if minbet <= 6.0:
                  if minbet <= 1.5:
                    if myscore <= 75.5:
                          return 75.0
                    else:
                          return 76.0
                  else:
                        return 76.0
                else:
                      return 80.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if myscore <= 73.5:
                          return 73.0
                    else:
                          return 74.0
                  else:
                        return 74.0
                else:
                  if minbet <= 6.0:
                        return 76.0
                  else:
                        return 80.0
            else:
              if minbet <= 1.5:
                if myscore <= 71.5:
                      return 71.0
                else:
                      return 72.0
              else:
                if pot <= 28.0:
                      return 72.0
                else:
                      return 72.72727272727273
        else:
          if oppscore <= 143.5:
            if oppscore <= 139.5:
              if myscore <= 62.5:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if oppscore <= 138.5:
                          return 62.0
                    else:
                          return 61.0
                  else:
                        return 62.0
                else:
                      return 64.0
              else:
                if minbet <= 1.5:
                  if oppscore <= 136.5:
                        return 64.0
                  else:
                        return 63.0
                else:
                      return 64.0
            else:
              if minbet <= 6.0:
                if oppscore <= 141.5:
                  if minbet <= 1.5:
                    if myscore <= 59.5:
                          return 59.0
                    else:
                          return 60.0
                  else:
                        return 60.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                      if myscore <= 57.5:
                            return 57.0
                      else:
                            return 58.0
                    else:
                          return 58.0
                  else:
                        return 60.0
              else:
                    return 64.0
          else:
            if myscore <= 52.5:
              if minbet <= 6.0:
                if oppscore <= 149.5:
                  if minbet <= 1.5:
                    if myscore <= 51.5:
                          return 51.0
                    else:
                          return 52.0
                  else:
                        return 52.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                      if myscore <= 49.5:
                            return 49.0
                      else:
                            return 50.0
                    else:
                          return 50.0
                  else:
                        return 52.0
              else:
                    return 56.0
            else:
              if oppscore <= 145.5:
                if minbet <= 1.5:
                  if myscore <= 55.5:
                        return 55.0
                  else:
                        return 56.0
                else:
                      return 56.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if myscore <= 53.5:
                          return 53.0
                    else:
                          return 54.0
                  else:
                        return 54.0
                else:
                      return 56.0
      else:
        if oppscore <= 171.5:
          if oppscore <= 159.5:
            if oppscore <= 155.5:
              if oppscore <= 153.5:
                if minbet <= 1.5:
                  if oppscore <= 152.5:
                        return 48.0
                  else:
                        return 47.0
                else:
                      return 48.0
              else:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                        return 45.31578947368421
                  else:
                        return 46.0
                else:
                      return 48.0
            else:
              if minbet <= 6.0:
                if oppscore <= 157.5:
                  if pot <= 2.5:
                        return 43.705882352941174
                  else:
                        return 44.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                          return 41.473684210526315
                    else:
                          return 42.0
                  else:
                        return 44.0
              else:
                    return 48.0
          else:
            if oppscore <= 166.5:
              if oppscore <= 163.5:
                if myscore <= 38.5:
                  if minbet <= 3.0:
                    if pot <= 3.0:
                          return 37.57142857142857
                    else:
                          return 38.0
                  else:
                        return 40.0
                else:
                  if pot <= 3.5:
                    if oppscore <= 160.5:
                          return 40.0
                    else:
                          return 39.0
                  else:
                        return 40.0
              else:
                if minbet <= 6.0:
                  if oppscore <= 165.5:
                    if pot <= 3.0:
                          return 35.7
                    else:
                          return 36.0
                  else:
                    if minbet <= 3.0:
                          return 34.0
                    else:
                          return 36.0
                else:
                      return 40.0
            else:
              if myscore <= 32.5:
                if minbet <= 3.0:
                  if myscore <= 30.5:
                    if pot <= 3.5:
                          return 29.4
                    else:
                          return 30.0
                  else:
                    if minbet <= 1.5:
                          return 31.53846153846154
                    else:
                          return 32.0
                else:
                      return 32.0
              else:
                if minbet <= 3.0:
                  if card <= 0.9876253008842468:
                        return 33.78947368421053
                  else:
                        return 33.92857142857143
                else:
                  if card <= 0.9822885394096375:
                        return 36.4
                  else:
                        return 36.0
        else:
          if oppscore <= 183.5:
            if oppscore <= 175.5:
              if minbet <= 6.0:
                if oppscore <= 173.5:
                  if minbet <= 1.5:
                        return 27.285714285714285
                  else:
                        return 28.0
                else:
                  if minbet <= 3.0:
                    if minbet <= 1.5:
                          return 25.470588235294116
                    else:
                          return 26.0
                  else:
                        return 28.0
              else:
                    return 32.0
            else:
              if myscore <= 20.5:
                if pot <= 14.0:
                  if oppscore <= 181.5:
                    if oppscore <= 180.5:
                          return 20.0
                    else:
                      if pot <= 5.0:
                            return 19.733333333333334
                      else:
                            return 20.0
                  else:
                    if pot <= 7.0:
                      if oppscore <= 182.5:
                            return 18.0
                      else:
                            return 17.76923076923077
                    else:
                          return 20.0
                else:
                      return 22.133333333333333
              else:
                if minbet <= 3.0:
                  if oppscore <= 177.5:
                    if myscore <= 23.5:
                          return 23.833333333333332
                    else:
                          return 24.0
                  else:
                    if minbet <= 1.5:
                          return 21.727272727272727
                    else:
                          return 22.0
                else:
                      return 24.0
          else:
            if myscore <= 8.5:
              if myscore <= 4.5:
                if minbet <= 3.0:
                      return 2.923076923076923
                else:
                  if pot <= 3.0:
                        return 4.4
                  else:
                        return 4.0
              else:
                if myscore <= 6.5:
                  if minbet <= 3.0:
                        return 5.928571428571429
                  else:
                        return 8.0
                else:
                  if oppscore <= 192.5:
                        return 8.0
                  else:
                        return 7.8
            else:
              if myscore <= 12.5:
                if minbet <= 3.0:
                  if oppscore <= 189.5:
                    if card <= 0.9852176606655121:
                          return 11.8
                    else:
                      if card <= 0.9946108162403107:
                            return 12.0
                      else:
                            return 11.9
                  else:
                    if oppscore <= 190.5:
                          return 10.0
                    else:
                          return 9.416666666666666
                else:
                  if pot <= 9.0:
                        return 12.0
                  else:
                        return 13.23076923076923
              else:
                if minbet <= 3.0:
                  if myscore <= 14.5:
                    if minbet <= 1.5:
                          return 13.6
                    else:
                          return 14.0
                  else:
                    if oppscore <= 184.5:
                          return 16.0
                    else:
                          return 15.6
                else:
                      return 16.0
    else:
      if oppscore <= 103.5:
        if myscore <= 104.5:
          if myscore <= 100.5:
            if myscore <= 98.5:
              if minbet <= 3.0:
                if oppscore <= 102.5:
                      return 98.0
                else:
                  if minbet <= 1.5:
                        return 97.0
                  else:
                        return 98.0
              else:
                if minbet <= 6.0:
                      return 100.0
                else:
                      return 104.44444444444444
            else:
              if minbet <= 6.0:
                if oppscore <= 100.5:
                      return 100.0
                else:
                  if minbet <= 1.5:
                        return 99.0
                  else:
                        return 100.0
              else:
                    return 104.0
          else:
            if oppscore <= 97.5:
              if oppscore <= 96.5:
                    return 104.0
              else:
                if minbet <= 1.5:
                      return 103.0
                else:
                      return 104.0
            else:
              if minbet <= 3.0:
                if myscore <= 101.5:
                  if minbet <= 1.5:
                        return 101.0
                  else:
                        return 102.0
                else:
                      return 102.0
              else:
                    return 104.0
        else:
          if myscore <= 109.5:
            if myscore <= 106.5:
              if minbet <= 3.0:
                if oppscore <= 94.5:
                      return 106.0
                else:
                  if minbet <= 1.5:
                        return 105.0
                  else:
                        return 106.0
              else:
                if minbet <= 6.0:
                      return 108.0
                else:
                      return 112.0
            else:
              if oppscore <= 91.5:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                        return 109.0
                  else:
                        return 110.0
                else:
                      return 112.0
              else:
                if minbet <= 6.0:
                  if oppscore <= 92.5:
                        return 108.0
                  else:
                    if minbet <= 1.5:
                          return 107.0
                    else:
                          return 108.0
                else:
                      return 112.0
          else:
            if myscore <= 112.5:
              if myscore <= 110.5:
                if minbet <= 3.0:
                      return 110.0
                else:
                      return 112.0
              else:
                if oppscore <= 88.5:
                      return 112.0
                else:
                  if minbet <= 1.5:
                        return 111.0
                  else:
                        return 112.0
            else:
              if minbet <= 3.0:
                if myscore <= 113.5:
                  if minbet <= 1.5:
                        return 113.0
                  else:
                        return 114.0
                else:
                      return 114.0
              else:
                if minbet <= 6.0:
                      return 116.0
                else:
                      return 120.0
      else:
        if myscore <= 88.5:
          if oppscore <= 117.5:
            if oppscore <= 115.5:
              if myscore <= 86.5:
                if minbet <= 3.0:
                  if myscore <= 85.5:
                    if minbet <= 1.5:
                          return 85.0
                    else:
                          return 86.0
                  else:
                        return 86.0
                else:
                      return 88.0
              else:
                if myscore <= 87.5:
                  if minbet <= 1.5:
                        return 87.0
                  else:
                        return 88.0
                else:
                      return 88.0
            else:
              if minbet <= 6.0:
                if oppscore <= 116.5:
                      return 84.0
                else:
                  if minbet <= 1.5:
                        return 83.0
                  else:
                        return 84.0
              else:
                    return 88.0
          else:
            if oppscore <= 119.5:
              if minbet <= 3.0:
                if oppscore <= 118.5:
                      return 82.0
                else:
                  if minbet <= 1.5:
                        return 81.0
                  else:
                        return 82.0
              else:
                if minbet <= 6.0:
                      return 84.0
                else:
                      return 88.0
            else:
              if myscore <= 78.5:
                if minbet <= 3.0:
                  if minbet <= 1.5:
                    if myscore <= 77.5:
                          return 77.0
                    else:
                          return 78.0
                  else:
                        return 78.0
                else:
                      return 80.0
              else:
                if oppscore <= 120.5:
                      return 80.0
                else:
                  if minbet <= 1.5:
                        return 79.0
                  else:
                        return 80.0
        else:
          if myscore <= 92.5:
            if oppscore <= 109.5:
              if minbet <= 6.0:
                if oppscore <= 108.5:
                      return 92.0
                else:
                  if minbet <= 1.5:
                        return 91.0
                  else:
                        return 92.0
              else:
                    return 96.0
            else:
              if minbet <= 3.0:
                if myscore <= 89.5:
                  if minbet <= 1.5:
                        return 89.0
                  else:
                        return 90.0
                else:
                      return 90.0
              else:
                if minbet <= 6.0:
                      return 92.0
                else:
                      return 96.0
          else:
            if oppscore <= 105.5:
              if oppscore <= 104.5:
                    return 96.0
              else:
                if minbet <= 1.5:
                      return 95.0
                else:
                      return 96.0
            else:
              if minbet <= 3.0:
                if oppscore <= 106.5:
                      return 94.0
                else:
                  if minbet <= 1.5:
                        return 93.0
                  else:
                        return 94.0
              else:
                    return 96.0

