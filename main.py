import telebot
from keep_alive import keep_alive
import random

# ==== CONFIG ====
TOKEN = "8212751693:AAHebJ3KKwKlOuk1s4rBcPnmGCQrSQq0N64"
bot = telebot.TeleBot(TOKEN)

# ==== DATA ====
names = ["хизя", "омар нажмик", "омар", "исма", "расул", "ислам"]
vote_stats = {name: 0 for name in names}

# =========================
#       BOT COMMANDS
# =========================

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, "бот четко. /help для списка команд.")

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id,
        "/random — перемешать имена\n"
        "/vote — создать голосование\n"
        "/addname <имя> — добавить имя\n"
        "/removename <имя> — удалить имя\n"
        "/listnames — список имен\n"
        "/leaderboard — топ по голосам\n"
        "/stats — общая статистика"
    )

@bot.message_handler(commands=['random'])
def cmd_random(message):
    shuffled = names.copy()
    random.shuffle(shuffled)
    text = "\n".join([f"{i+1}. {name}" for i, name in enumerate(shuffled)])
    bot.send_message(message.chat.id, "🎲:\n\n" + text)

@bot.message_handler(commands=['addname'])
def cmd_addname(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "используй: /addname <имя>")
        return
    name = parts[1].strip()
    if name in names:
        bot.send_message(message.chat.id, "уже есть такое имя")
        return
    names.append(name)
    vote_stats[name] = 0
    bot.send_message(message.chat.id, f"имя '{name}' добавлено")

@bot.message_handler(commands=['removename'])
def cmd_removename(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "используй: /removename <имя>")
        return
    name = parts[1].strip()
    if name not in names:
        bot.send_message(message.chat.id, "такого имени нет")
        return
    names.remove(name)
    vote_stats.pop(name, None)
    bot.send_message(message.chat.id, f"имя '{name}' удалено")

@bot.message_handler(commands=['listnames'])
def cmd_list(message):
    text = "\n".join(f"- {n}" for n in names)
    bot.send_message(message.chat.id, "текущий список имен:\n\n" + text)

@bot.message_handler(commands=['leaderboard'])
def cmd_leaderboard(message):
    if not vote_stats:
        bot.send_message(message.chat.id, "статистика пуста")
        return
    sorted_stats = sorted(vote_stats.items(), key=lambda x: -x[1])
    text = "\n".join([f"{i+1}. {name} — {count}" for i, (name, count) in enumerate(sorted_stats)])
    bot.send_message(message.chat.id, "🏆 лидеры:\n\n" + text)

@bot.message_handler(commands=['stats'])
def cmd_stats(message):
    total_votes = sum(vote_stats.values())
    text = "\n".join([f"{name}: {count}" for name, count in vote_stats.items()])
    bot.send_message(message.chat.id, f"📊 общая статистика (всего голосов: {total_votes}):\n\n" + text)

# =========================
#        KEEP-ALIVE
# =========================
keep_alive()

# =========================
#        RUN BOT
# =========================
bot.infinity_polling()
