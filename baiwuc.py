from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import telegram

# 存储用户的消息ID
user_messages = {}

# 示例类别和商户数据
categories = {
    "美食 🍜": [
        {"id": "1", "name": "99美食小屋🛖", "address": "亚太城", "Link": "https://t.me/jj99meishi", "specialty": "中餐", "order_link": "jj99ms2", "image": "https://photos.app.goo.gl/j6kjyY6V6nZqBoF77", "contact": "@jj99ms2"},
        {"id": "2", "name": "一日三餐🍜", "address": "亚太城", "Link": "https://t.me/yirisancan112", "specialty": "快餐", "order_link": "https://order.com/yirisancan", "image": "https://photos.app.goo.gl/Xfe885Bff131wRX26", "contact": "@yirisancan"},
        {"id": "3", "name": "邻里美食🍳", "address": "亚太城", "Link": "https://t.me/linli777", "specialty": "快餐", "order_link": "https://order.com/linli", "image": "https://photos.app.goo.gl/cE4R6A2km6BEAEpZ6", "contact": "@linli77"},
        {"id": "4", "name": "Um由米早点+快餐🥪", "address": "亚太城", "Link": "https://t.me/umxiaochi88899", "specialty": "快餐", "order_link": "https://order.com/umxiaochi", "image": "https://photos.app.goo.gl/GTERF61JnTBkcyX5A", "contact": "@umxiaochi888"},
        {"id": "5", "name": "🛠广告位招租🛠", "address": "亚太城", "Link": "https://t.me/yuan1355", "specialty": "💕阿源管理员💕", "order_link": "https://t.me/yuan1355", "image": "https://photos.app.goo.gl/HB81w3gwyDZDuWpn8", "contact": "@yuan1355"}
    ],
    "酒店 🏨": [
        {"id": "1", "name": "華星酒店🏩", "address": "亚太城", "Link": "https://t.me/Huaxingjiudian118899", "stars": 3, "order_link": "https://order.com/Huaxingjiudian", "image": "https://photos.app.goo.gl/f2Ud6pWtW8TGYPVeA", "contact": "@HXJD888888"},
        {"id": "2", "name": "浩峰宾馆🏩", "address": "亚太城", "Link": "https://t.me/HAOFENG100", "stars": 3, "order_link": "https://order.com/HAOFENG", "image": "https://photos.app.goo.gl/sUkTZ3oBifMjc9iv5", "contact": "@HaoFengMotel"},
        {"id": "3", "name": "亚太微笑酒店公寓🏨", "address": "亚太城", "Link": "https://t.me/yataiweixiaojiudian", "stars": 3, "order_link": "https://order.com/yataiweixiao", "image": "https://photos.app.goo.gl/864hW3aTGFWP919w6", "contact": "@weixiaojiudian"},
        {"id": "4", "name": "九月酒店🏨", "address": "亚太城", "Link": "https://t.me/jyjd16666888", "stars": 3, "order_link": "https://order.com/jyjd", "image": "https://photos.app.goo.gl/CLio6erMSu3gFSe29", "contact": "@jiuyuejiudian00001"},
        {"id": "5", "name": "SMM酒店🏨", "address": "亚太城", "Link": "https://t.me/smm6666666", "stars": 3, "order_link": "https://order.com/SMM", "image": "https://photos.app.goo.gl/73syVenPgUdJFWrJ8", "contact": "@SMMMotel"},
        {"id": "6", "name": "广告位招租🏨", "address": "亚太城", "Link": "@yuan1355", "stars": 666, "order_link": "https://order.com/yuan1355", "image": "https://photos.app.goo.gl/ZmydR4M6z6FvfqZz7", "contact": "@yuan1355"}
    ],
    "购物 🛍": [
        {"id": "1", "name": "云端小卖铺☁️", "address": "亚太城", "Link": "https://t.me/yunduan878787", "specialty": "小卖铺", "order_link": "https://order.com/yunduan", "image": "https://photos.app.goo.gl/TB6KsRAT43wzvR6y7", "contact": "@yunduan7777"},
        {"id": "2", "name": "甜心烘焙花艺社🛒", "address": "亚太城", "Link": "https://t.me/tianxin8888", "specialty": "其它", "order_link": "https://order.com/tianxin", "image": "https://photos.app.goo.gl/nNdriubaNVnYRqX78", "contact": "@tianxin8866"},
        {"id": "3", "name": "云里雾里电子烟专卖🛒", "address": "亚太城", "Link": "https://t.me/ylwl888", "specialty": "电子烟", "order_link": "https://order.com/ylwl", "image": "https://photos.app.goo.gl/oBDefWT9H2gU7wWb6", "contact": "@zhengzhi1122"},
        {"id": "4", "name": "亚太环球数码🛒", "address": "亚太城", "Link": "https://t.me/hqsm8866", "specialty": "数码产品", "order_link": "https://order.com/hqsm", "image": "https://photos.app.goo.gl/oBDefWT9H2gU7wWb6", "contact": "@HQSM8888"},
        {"id": "5", "name": "龙龙服装百货🛒", "address": "亚太城", "Link": "https://t.me/llfzbh520", "specialty": "服装", "order_link": "https://order.com/llfzbh", "image": "https://photos.app.goo.gl/tETKCvBoM5NX95tg9", "contact": "@nvf520"},
        {"id": "6", "name": "广告位招租🛒", "address": "亚太城", "Link": "https://t.me/yuan1355", "order_link": "https://order.com/yuan1355", "stars": 666, "image": "https://path_to_image_8.jpg", "contact": "@yuan1355"}
    ],
    "医疗 🏥": [
        {"id": "1", "name": "协和国际医院 🏥", "address": "亚太城", "Link": "https://t.me/xhgjyy", "specialty": "医院 🏥", "order_link": "https://order.com/xhgjyy", "image": "https://photos.app.goo.gl/Q3N7G8SBA6zHbaZ78", "contact": "@zsmz001 "},
        {"id": "2", "name": "安溪医院 🏥", "address": "亚太城", "Link": "https://t.me/anxiyiyuan111", "specialty": "医院 🏥", "order_link": "https://order.com/anxiyiyuan", "image": "https://photos.app.goo.gl/GQfAUeDLs242dobM6", "contact": "@axyy120"},
        {"id": "3", "name": "亚太亨通门诊 🏥", "address": "亚太城", "Link": "https://t.me/hentong888", "specialty": "诊所 🩺", "order_link": "https://order.com/hentong", "image": "https://photos.app.goo.gl/AmKQs3iDrEGx1jAk6", "contact": "@htmz889"},
        {"id": "4", "name": "中医养生治疗 💊", "address": "亚太城", "Link": "https://t.me/zyysg5588", "specialty": "中医 💊", "order_link": "https://order.com/zyysg", "image": "https://photos.app.goo.gl/UxihWQXS6jEZctSw9", "contact": "@zyg9999"}
    ]
}

# 显示商家信息
def show_store_info(update: Update, context):
    query = update.callback_query
    query.answer()

    # 获取回调数据中的类别和商户ID
    data = query.data.split("_")
    category_name = data[1]
    store_id = data[2]

    # 查找商家信息
    store = next(
        (store for store in categories.get(category_name, []) if store["id"] == store_id),
        None
    )

    if store:
        # 获取商家联系信息，确保它是有效的 URL
        contact_link = store.get("contact", "")

        # 如果 contact 是以 "@" 开头，转换为 Telegram 链接
        if contact_link.startswith("@"):
            contact_link = f"https://t.me/{contact_link[1:]}"
        # 如果 contact 不是有效的 URL（没有 http 或 https），则做进一步的处理
        elif not contact_link.startswith("http"):
            # 这里可以根据需要处理，比如抛出一个错误或日志输出
            contact_link = "https://t.me/default"  # 可以设置一个默认的链接，或者跳过按钮

        # 创建返回按钮和其他按钮
        keyboard = [
            [InlineKeyboardButton("🏠 返回主菜单", callback_data="return_main")],
            [InlineKeyboardButton("🔗 访问商家", url=store.get("Link", "#"))],  # 商家主页链接
            [InlineKeyboardButton("📞 联系商家", url=contact_link)]  # 商家联系方式
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # 调试输出生成的 URL
        print(f"生成的联系商家链接: {contact_link}")  # 打印生成的 URL 以便调试

        # 构建商家信息文本
        store_info = f"🌟{store['name']}🌟\n地址: {store['address']}\n"
        store_info += f"特色: {store.get('specialty', '未提供特色')}"

        # 如果图片存在，发送图片
        if store.get("image"):
            context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=store["image"],
                caption=store_info,
                reply_markup=reply_markup
            )
        else:
            query.edit_message_text(store_info, reply_markup=reply_markup)



# 搜索商户
def search_stores(update: Update, context):
    query = update.message.text.lower()  # 获取用户输入的文本并转小写
    matching_stores = []  # 用于存放匹配的商户

    # 遍历所有类别和商户，寻找匹配项
    for category, stores in categories.items():
        for store in stores:
            # 检查商户的各字段是否包含查询文本
            if (query in store['name'].lower() or  # 商户名称匹配
                query in store.get('address', '').lower() or  # 地址匹配
                query in store.get('specialty', '').lower()):  # 特色匹配
                matching_stores.append(store)

    # 如果找到匹配的商户
    if matching_stores:
        keyboard = []
        for store in matching_stores:
            keyboard.append([InlineKeyboardButton(store["name"], callback_data=f"store_{category}_{store['id']}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"找到以下匹配的商户：", reply_markup=reply_markup)
    else:
        # 如果没有找到商户，提供返回主菜单的选项或查看所有商户
        keyboard = [
            [InlineKeyboardButton("✨ 试试看点击这里开始搜索吧✨", callback_data="return_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("未找到匹配的商户，请尝试其他关键词。", reply_markup=reply_markup)

# 显示所有商户
def show_all_stores(update: Update, context):
    query = update.callback_query
    query.answer()

    # 创建所有商户的按钮
    keyboard = []
    for category, stores in categories.items():
        for store in stores:
            keyboard.append([InlineKeyboardButton(store["name"], callback_data=f"store_{category}_{store['id']}")])

    # 添加返回主菜单的按钮
    keyboard.append([InlineKeyboardButton("🔙 返回主菜单", callback_data="return_main")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = query.edit_message_text("以下是所有商户：", reply_markup=reply_markup)

    # 存储消息ID
    user_messages[query.message.chat_id] = [message.message_id]

# 主菜单 - 分类
def start(update: Update, context):
    keyboard = []
    
    # 创建两列布局的分类按钮
    categories_list = list(categories.keys())
    for i in range(0, len(categories_list), 2):
        row = [
            InlineKeyboardButton(categories_list[i], callback_data=f"category_{categories_list[i]}"),
        ]
        if i + 1 < len(categories_list):
            row.append(InlineKeyboardButton(categories_list[i + 1], callback_data=f"category_{categories_list[i + 1]}"))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 判断是消息还是回调查询
    if update.message:  # 用户发送了文本消息
        message = update.message.reply_text("请选择分类：", reply_markup=reply_markup)
        user_messages[update.message.chat_id] = [message.message_id]
    elif update.callback_query:  # 用户点击了按钮
        message = update.callback_query.message.reply_text("请选择分类：", reply_markup=reply_markup)
        user_messages[update.callback_query.message.chat_id] = [message.message_id]

# 显示商家列表
def show_stores(update: Update, context):
    query = update.callback_query
    query.answer()

    # 获取分类名
    category_name = query.data.split("_")[1]
    stores = categories.get(category_name, [])

    # 生成商家按钮（每行两个）
    keyboard = []
    for i in range(0, len(stores), 2):
        row = [
            InlineKeyboardButton(stores[i]["name"], callback_data=f"store_{category_name}_{stores[i]['id']}"),
        ]
        if i + 1 < len(stores):
            row.append(InlineKeyboardButton(stores[i + 1]["name"], callback_data=f"store_{category_name}_{stores[i + 1]['id']}"))
        keyboard.append(row)

    # 添加返回主菜单的按钮
    keyboard.append([InlineKeyboardButton("🔙 返回主菜单", callback_data="return_main")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = query.edit_message_text(f"请选择【{category_name}】中的商家：", reply_markup=reply_markup)

    # 存储所有消息ID
    if query.message.chat_id not in user_messages:
        user_messages[query.message.chat_id] = []
    user_messages[query.message.chat_id].append(message.message_id)

# 返回主菜单并删除消息记录
def return_to_main(update: Update, context):
    query = update.callback_query
    query.answer()

    chat_id = query.message.chat_id
    
    # 确保只有在存储了消息ID时才删除消息
    if chat_id in user_messages and user_messages[chat_id]:
        for message_id in user_messages[chat_id]:
            try:
                context.bot.delete_message(chat_id, message_id)
            except telegram.error.BadRequest as e:
                print(f"Error deleting message {message_id}: {e}")
        
        # 清空存储的消息ID
        user_messages[chat_id] = []

    # 重新发送主菜单
    start(update, context)

# 捕获用户输入的错误指令并提示
def handle_unknown(update: Update, context):
    update.message.reply_text(
        "无法识别的指令，请通过 **/start** 开始查找商品。",
        parse_mode="Markdown"
    )

# 主函数
def main():
    updater = Updater("8038399366:AAGO4zrLLilJ2tGSi_4YGaDQwaR3uGD6J3g", use_context=True)
    dp = updater.dispatcher

    # 命令处理
    dp.add_handler(CommandHandler("start", start))

    # 回调处理
    dp.add_handler(CallbackQueryHandler(show_stores, pattern="^category_"))
    dp.add_handler(CallbackQueryHandler(show_store_info, pattern="^store_"))
    dp.add_handler(CallbackQueryHandler(return_to_main, pattern="^return_main$"))

    # 捕获未知消息
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_stores))

    # 启动机器人
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()