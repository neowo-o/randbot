import os
import json
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # токен в Secrets
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ======= СПИСОК ИМЕН =======
names = ["хизя", "омар нажмик", "омар", "исма", "расул", "ислам"]
vote_stats = {name: 0 for name in names}

# ===================
# ===== КОМАНДЫ =====
# ===================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("бот четко работает! используй /help для списка команд")

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.answer(
        "/random — перемешать имена\n"
        "/vote — создать голосование\n"
        "/addname <имя> — добавить имя\n"
        "/removename <имя> — удалить имя\n"
        "/listnames — показать список имен\n"
        "/leaderboard — топ голосов\n"
        "/stats — общая статистика"
    )

@dp.message_handler(commands=["random"])
async def random_cmd(message: types.Message):
    import random
    shuffled = names.copy()
    random.shuffle(shuffled)
    text = "\n".join(f"{i+1}. {name}" for i, name in enumerate(shuffled))
    await message.answer(f"🎲:\n{text}")

@dp.message_handler(commands=["addname"])
async def add_name(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("использование: /addname имя")
        return
    name = parts[1].strip()
    if name in names:
        await message.answer("асад имя уже ани и")
        return
    names.append(name)
    vote_stats[name] = 0
    await message.answer(f"имя '{name}' добавлено")

@dp.message_handler(commands=["removename"])
async def remove_name(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("использование: /removename имя")
        return
    name = parts[1].strip()
    if name not in names:
        await message.answer("асад имя адишь")
        return
    names.remove(name)
    vote_stats.pop(name, None)
    await message.answer(f"имя '{name}' удалено")

@dp.message_handler(commands=["listnames"])
async def list_names(message: types.Message):
    text = "\n".join(f"- {n}" for n in names)
    await message.answer(f"список имен:\n{text}")

@dp.message_handler(commands=["vote"])
async def vote_cmd(message: types.Message):
    await message.answer_poll(
        question="вуш",
        options=names,
        is_anonymous=False
    )

@dp.message_handler(commands=["leaderboard"])
async def leaderboard_cmd(message: types.Message):
    if not vote_stats:
        await message.answer("статистика пока пустая.")
        return
    sorted_stats = sorted(vote_stats.items(), key=lambda x: -x[1])
    text = "\n".join([f"{i+1}. {name} — {count}" for i, (name, count) in enumerate(sorted_stats)])
    await message.answer(f"🏆 четкий гадиймар:\n{text}")

@dp.message_handler(commands=["stats"])
async def stats_cmd(message: types.Message):
    total_votes = sum(vote_stats.values())
    text = "\n".join(f"{name}: {count}" for name, count in vote_stats.items())
    await message.answer(f"📊 общая статистика (всего голосов: {total_votes}):\n{text}")

# ===================
# ===== FLASK =======
# ===================

app = Flask(__name__)

@app.route("/")
def alive():
    return "Bot is alive"

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = types.Update(**request.get_json())
    Dispatcher.set_current(dp)
    dp.update = update
    return Dispatcher.set_current(dp).process_update(update)

# ===================
# ===== RUN =======
# ===================

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=8080)

