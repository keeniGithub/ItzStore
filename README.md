<img src="https://cdn.discordapp.com/attachments/871062118533845073/1135974437800382484/itzstorelogo.png" style="width: 310">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white) 
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Do not judge strictly, this is my first major bot, if you want to write something you would like to change or add, you can write to me at [Telegram](https://t.me/itzkeeni).

### Navigation
<dl>
    <dt>• <a href="#install">Install</a></dt>
    <dt>• <a href="#setting">Setting up configurations</a></dt>
        <dd>• <a href="#tokenbot">Token bot</a></dd>
        <dd>• <a href="#payok">PayOk</a></dd>
    <dt>• <a href="#profile">Profile</a></dt>
        <dd>• <a href="#balance">Balance</a></dd>
    <dt>• <a href="#promo">Promo codes</a></dt>
        <dd>• <a href="#howaddpromo">How to add promo?</a></dd>   
    <dt>• <a href="#Shop">Shop</a></dt>
        <dd>• <a href="#SteamRu">Steam ru</a></dd>
    <dt>• <a href="#orders">Orders</a></dt>
    <dt>• <a href="#guarantee">Shop Guarantee</a></dt>
    <dt>• <a href="#info">Information</a></dt>
    <dt>• <a href="#admin">ADMIN</a></dt>
        <dd>• <a href="#panel">ADMIN PANEL</a></dd>
        <dd>• <a href="#checkOrder">Check order</a></dd>
        <dd>• <a href="#ban">Account Ban</a></dd>
    <dt>• <a href="#other">Other</a></dt>
        <dd>• <a href="#HelpForAdmin">Administrator help info</a></dd>  
        <dd>• <a href="#db">DataBase</a></dd>
        <dd>• <a href="#stop">/stop</a></dd>
    <dt>• <a href="#otherLink">Other link</a></dt>
</dl>



# Short description
## This is a shop bot written in PythonTelegramBotAPI (telebot). The bot is needed to purchase Steam RU, Steam EU, Steam US, Xbox US, PS Store US gift keys and in the future this list will only be supplemented. The bot has a profile where your Id, your balance, the amount of money spent and finally the number of purchases are recorded in the database. There are also promo codes for which you get money.

<h3> P.s the bot should still have gift keys for Apple, but for technical reasons they are not yet available</h3>

# Installing all required libraries and APIs
<a name="install"></a>
<h3>Install Telebot</h3>

- Use pip3

```
$ pip install pyTelegramBotAPI
```

- Use git

```
$ git clone https://github.com/eternnoir/pyTelegramBotAPI.git
$ cd pyTelegramBotAPI
$ python setup.py install
```

<h3>Install PyPayments (For PayOk)</h3>
<h4>PyPaymnets — is a Python wrapper for API of different payment providers. It is designed to be a simple and easy to use library for developers to integrate payment into their applications.</h4>

- Use pip3

```
$ pip install pypayment
```

- Git install is missing

# Setting up configurations
<a name="setting"></a>
## Token bot
<a name="tokenbot"></a>
### In `tokenbot.py` In the Your Token field, enter your token received from [BotFather](https://t.me/botfather)

```python
# tokenbot.py
token = "Your Token"
```

## PayOK
<a name="payok"></a>
### In the main `shop.py` file, line 227 indicates your data received on the [PayOk](https://payok.io) website

```python
# shop.py
PayOkPayment.authorize("Api-key", "Api-ID", "Shop-ID", "Secret-key",
                            payment_type=PayOkPaymentType.CARD,
                            currency=PayOkCurrency.RUB,
                            success_url="https://sites.google.com/view/itzstorealerts/ok")
```

#### api-key - PayOk [API Key](https://payok.io/cabinet/api.php)

#### api-id - PayOk [API ID](https://payok.io/cabinet/api.php)

#### shop-id - PayOk [Shop ID](https://payok.io/cabinet/main.php)

#### secret-key - PayOk [Shop secret key](https://payok.io/cabinet/main.php)

# Profile

<a name="profile"></a>

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1135984108376432710/image.png">

### As mentioned earlier, the profile displays your id, balance, amount of money spent and number of purchases. Also in the profile you can replenish the balance or enter a promo code. The user information button is available only with the Admin status (write just below)

## Balance

<a name="balance"></a>

### When replenishing the balance, the amount must be more than 100 Russian rubles.

### 60 minutes are given for payment, after their expiration the link becomes invalid

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1135985323013316699/image.png">

<br>

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1135985460305461388/image.png" style="width 10px">

### In the future, we will most likely switch to Lava or AnyPay

# Promo codes

<a name="promo"></a>

### A system of promotional codes for which the user will receive a couple of rubles on his balance.

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136002665801855136/image.png">

## How to add a promo code?

<a name="howaddpromo"></a>

### 1. Go to the admin panel `/admin`
### 2. Click on add promo
### 3. Enter the data and your promotional code is recorded in the database

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136003697776803961/image.png">

# Shop

<a name="Shop"></a>

### In the store you can buy items for Steam, Xbox, PS Store and later for Apple.

## Steam ru

<a name="SteamRu"></a>

### Top-ups for Steam Russia can be for any amount up to 100 to 15,000 rubles. Also, unlike others, replenishment is carried out instantly, and not with a gift key. And on Steam Russia there is a 15% commission on your top-up amount

# Orders
## After each purchase, you are given a receipt, where the order number, product, amount, time of purchase and the buyer are written. This is required to place an order. You can also check the check and its information in the admin panel.
<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136009912296677487/image.png">
<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136009974225588284/image.png">

# Shop Guarantee
## ItzStore Provides guarantees for all goods until they are purchased or credited. You won't get banned for buying from us! Everything is bought officially from official stores.

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136006104061595678/image.png">

<br>

# Information
### The help is located on instructions on how to activate a particular service, on technical support and our telegram channel
<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136007133813559366/image.png">

### For administration will be displayed only with the status of Admin

# ADMIN 
## ADMIN PANEL
### In the admin panel you can: 
- Top up user balance
- Subtract user balance
- Block user
- Unblock user
- Check order
- Add promo
- Edit promo (coming soon)
- Add/remove administrator (works only for ItzKeeni - me, but you can just change the values ​​in the database)
### (I will not stop at simple functionality and promo, because this is already clear)

### You can open the admin panel with the `/admin` command

## Check order
### As mentioned above, we have an order system where information and an order number are written to you. You can just check it for the credibility of the information

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136011136190394508/image.png">

## Account blocking
### We have an account lockout system where the user can't do anything. To unlock it, you will need to contact technical support. You can block your account through the admin panel

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136011757018677298/image.png">

### In the future, we will make it possible to write the reasons for blocking.

# Other
## Administrator help info
### Even with the admin status, you have access to help for the administration and information about any user
### Help describes information about orders
<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136012879770959893/image.png">

## User information
### In the profile there was a button for checking information and the user. There you enter id and all information about it is written to you

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136013743424295033/image.png">

# DataBase
### Our store uses a Sqlite3 database. The database has 3 tables:
- For users
- For Orders
- For promo codes.

<img src="https://cdn.discordapp.com/attachments/871062118533845073/1136014372641177750/image.png">

### Migration to Mysql or MongoDB is being considered

# `/Stop`
### This command is also available only for Itzkeeni - me. It is needed for an emergency stop of the bot, by calling a function with incorrect syntax

```python
# 451 line in shop.py
if call.data == 'bot_stop':
            print("session the close")
            sql.execute()
```

<hr>

### This was my first big bot, and my first big readme. As I wrote at the beginning, you can write to me in Telegram about wishes and shortcomings )
<h1 align="center">Other link</h1>

<div align="center">

[Bstore](https://t.me/thebelkin)
|
[telegram](https://t.me/kenyka)
|
[YouTube](https://www.youtube.com/channel/UCM6InRH22Xno8nywrZnbhLA)
|
[GGdash](https://discord.gg/r6gCRR75Un)
</div>
