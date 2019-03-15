# import pandas as pd
# data = pd.read_csv('networkData.csv')
# deepak = data.sort_values('slno')
# deepak.to_csv('data.csv',index = False)

from googletrans import Translator

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
for i in range(1000):
    if i%300==0:
        translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
    k = translator.translate('شرکت شبکه الکترونیکی پرداخت کارت شاپرک - صفحه اصلی')
    print(i, k.text)