# Teneo Community Node BOT
Teneo Community Node BOT

Kengaytmani bu yerdan yuklab oling: [Teneo Community Node](https://chromewebstore.google.com/detail/teneo-community-node/emcclcoaglgcpoognfiggmhnhgabppkm) | Referal koddan foydalaning: sWb27

## Xususiyat

  - Hisob ma'lumotlarini avtomatik olish
  - Agar siz 1 tani tanlasangiz, avtomatik proksi bilan avtomatik ishga tushirish [foydalaning [Monosans Proxy](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt)]
  - Agar siz 2 ta tanlasangiz, qo‘lda proksi bilan avtomatik ishga tushirish [shaxsiy proksini manual_proxy.txt ga joylashtirish]
  - Agar siz 3 ni tanlasangiz, proksisiz avtomatik ishga tushirish
  - Tugunlarni avtomatik ulash va Ping yuborish
  - Avtomatik xabarlarni har 15 daqiqada qabul qilish
  - Mavzular bilan ko'p hisoblar

## Shart

Python3.9 dan yuqori va PIP o'rnatilganligiga ishonch hosil qiling.

## O'rnatish

1. **Repozitoriy klonlash:**
   ```bash
   git clone https://github.com/JMSM0707/T-FARM.git
      ```
   ```bash
   cd T-FARM-main
   ```

2. **O'rnatish talablari:**
   ```bash
   python INSTALL.BAT yoki pip install -r requirements.txt #yoki pip3 install -r requirements.txt
   ```

## Konfiguratsiya

- **accounts.json:** Siz faylni accounts.json loyiha katalogida topasiz. accounts.json unda skript formatiga mos keladigan ma'lumotlar mavjudligiga ishonch hosil qiling, aks holda skript ishlamaydi. Mana fayl formatlariga misollar:

  ```bash
    [
        {
            "Email": "pochta adresingiz 1",
            "Password": "teneo parolingiz 1"
        },
        {
            "Email": "pochta adresingiz 2",
            "Password": "teneo parolingiz 2"
        }
    ]
  ```
- **manual_proxy.txt:** Siz faylni manual_proxy.txt loyiha katalogida topasiz. manual_proxy.txt unda skript formatiga mos keladigan ma'lumotlar mavjudligiga ishonch hosil qiling aks holda skript ishlamaydi. Mana fayl formatlariga misollar:

  ```bash
  http://user:pass@ip:port
  socks4://user:pass@ip:port
  socks5://user:pass@ip:port)
  ```

## Ishga tushurish

 ```bash
python bot.py #yoki python3 bot.py
 ```

## Yopish

Ushbu omborga tashrif buyurganingiz uchun tashakkur, kuzatishlar va yulduzchalar shaklida hissa qo'shishni unutmang. Savollaringiz bo'lsa, muammolarga duch kelsangiz yoki yaxshilash bo'yicha takliflaringiz bo'lsa, men bilan bog'laning yoki ushbu GitHub omborida muammoni oching.

**JMSM0707**
