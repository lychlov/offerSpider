# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     js_shot
   Description :
   Author :       Lychlov
   date：          2018/9/23
-------------------------------------------------
   Change Activity:
                   2018/9/23:
-------------------------------------------------
"""
import js2py
import execjs

document = {'cookie':''}
p='''
y="0su".slice(0,1) +  '' + "9m".charAt(0) +  '' +''+String.fromCharCode(0x31) +  '' +''+"b" + String.fromCharCode(51) + "0sucur".charAt(0)+String.fromCharCode(57) + "b".slice(0,1) +  '' +''+"5" + "9" + "" +"fsec".substr(0,1) + '3f2a'.substr(3, 1) +String.fromCharCode(0x34) +  '' + 'f' +   '' +String.fromCharCode(0x38) + "f".slice(0,1) +  '' + 'V0'.slice(1,2)+"5sucur".charAt(0)+String.fromCharCode(56) + "bsec".substr(0,1) + "7" + "b" + "9".slice(0,1) + "5sec".substr(0,1) + String.fromCharCode(0x62) +  '' +''+'QpB0'.substr(3, 1) + '' + "1" + '9z9c'.substr(3, 1) +"8".slice(0,1) + '9' +  'Hv43'.substr(3, 1) +"" +"0sec".substr(0,1) + '';cookie='ssuc'.charAt(0)+ 'usucu'.charAt(0)  +'csuc'.charAt(0)+ 'suu'.charAt(2)+'rsuc'.charAt(0)+ 'i'+'_'+'csuc'.charAt(0)+ 'ls'.charAt(0)+'o'+'us'.charAt(0)+'sucurid'.charAt(6)+'sup'.charAt(2)+'r'+'osucuri'.charAt(0) + 'xsucuri'.charAt(0) + 'y'+'_'+''+'u'+'u'+''+'isuc'.charAt(0)+ 'sud'.charAt(2)+'su_'.charAt(2)+'sucu1'.charAt(4)+ 's0'.charAt(1)+'sucu5'.charAt(4)+ 'sucur4'.charAt(5) + 'sucurib'.charAt(6)+'a'+'sub'.charAt(2)+'d'+'asuc'.charAt(0)+ "=" + y + ';path=/;max-age=86400'; 
'''
js = "var s={},u,c,U,r,i,l=0,a,e=eval,w=String.fromCharCode,sucuri_cloudproxy_js='',S='eD0nMG1TMycuc3Vic3RyKDMsIDEpICsgJycgKycnKyJkIi5zbGljZSgwLDEpICsgImRzdWN1ciIuY2hhckF0KDApKyJkbCIuY2hhckF0KDApICsgICcnICsgCiI1c3VjdXIiLmNoYXJBdCgwKSsnMCcgKyAgICcnICsnMmUnLnNsaWNlKDEsMikrJzgnICsgICI0IiArICIiICsiY3N1Ii5zbGljZSgwLDEpICsgIjRzdWN1ciIuY2hhckF0KDApKyIiICsndUdlJy5jaGFyQXQoMikrJz0yJy5zbGljZSgxLDIpK1N0cmluZy5mcm9tQ2hhckNvZGUoMHg2MikgKyAnNCcgKyAgJzYnICsgICAnJyArJ2YnICsgICI0ayIuY2hhckF0KDApICsgICcnICsgCiJkdyIuY2hhckF0KDApICsgIjAiICsgIjEiICsgIiIgKydmJyArICBTdHJpbmcuZnJvbUNoYXJDb2RlKDB4MzMpICsgIjgiLnNsaWNlKDAsMSkgKyAgJycgKyAKImNzdWN1ciIuY2hhckF0KDApKyAnJyArJ2UnICsgICIzbSIuY2hhckF0KDApICsgICcnICsgCiI5c3UiLnNsaWNlKDAsMSkgKyAiIiArU3RyaW5nLmZyb21DaGFyQ29kZSgweDMyKSArICdWeD41Jy5zdWJzdHIoMywgMSkgKyAnJyArIjNzdWN1ciIuY2hhckF0KDApKyJhIiArICAnJyArJyc7ZG9jdW1lbnQuY29va2llPSdzc3VjdXJpJy5jaGFyQXQoMCkgKyAndXMnLmNoYXJBdCgwKSsnYycrJ3VzdScuY2hhckF0KDApICsnc3VjdXJyJy5jaGFyQXQoNSkgKyAnaScrJ19zdScuY2hhckF0KDApICsnc3VjdXJpYycuY2hhckF0KDYpKydsJy5jaGFyQXQoMCkrJ29zdWN1Jy5jaGFyQXQoMCkgICsnc3UnLmNoYXJBdCgxKSsnc3VjdXJkJy5jaGFyQXQoNSkgKyAncCcuY2hhckF0KDApKydyJysnJysnc3VjdXJpbycuY2hhckF0KDYpKyd4c3VjdScuY2hhckF0KDApICArJ3lzJy5jaGFyQXQoMCkrJ18nKyd1JysndScrJ2knKydkJysnX3N1Y3VyJy5jaGFyQXQoMCkrICc3Jysnc3VjdXJjJy5jaGFyQXQoNSkgKyAnOScrJzNzJy5jaGFyQXQoMCkrJ2RzdWN1cmknLmNoYXJBdCgwKSArICczJy5jaGFyQXQoMCkrJzZzdScuY2hhckF0KDApICsnN3N1YycuY2hhckF0KDApKyAnOXMnLmNoYXJBdCgwKSsiPSIgKyB4ICsgJztwYXRoPS87bWF4LWFnZT04NjQwMCc7IGxvY2F0aW9uLnJlbG9hZCgpOw==';L=S.length;U=0;r='';var A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';for(u=0;u<64;u++){s[A.charAt(u)]=u;}for(i=0;i<L;i++){c=s[S.charAt(i)];U=(U<<6)+c;l+=6;while(l>=8){((a=(U>>>(l-=8))&0xff)||(i<(L-2)))&&(r+=w(a));}}e(r);"
js_deal=js2py.eval_js(p)
print(js_deal)
# js2py.translate_file('test.js', 'example.py')
# execjs.eval('''p=String.fromCharCode(56) + "6sec".substr(0,1) + "f" + 'VrC0'.substr(3, 1) +'87'.slice(1,2)+ '' +''+'JhP7'.substr(3, 1) + '' +'7' +  '?e'.slice(1,2)+"esucur".charAt(0)+'<v48'.substr(3, 1) +"" +String.fromCharCode(101) + '8' +  "e" +  '' +''+"1" + "" +"2r".charAt(0) + 'u@f'.charAt(2)+ '' +''+"3" +  '' +"esucur".charAt(0)+"esec".substr(0,1) + String.fromCharCode(0x37) + "6" + "" +"5" + "d" + "" +"1su".slice(0,1) + "" +String.fromCharCode(49) + "1" + '2' +  "c" + "csec".substr(0,1) + "bi".charAt(0) + String.fromCharCode(0x37) + ':f'.slice(1,2)+'';''')
