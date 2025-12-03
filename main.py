import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from keep_alive import keep_alive

# ==== CONFIG ====
TOKEN = "8212751693:AAHebJ3KKwKlOuk1s4rBcPnmGCQrSQq0N64"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==== DATA ====
names = ["хизя", "омар нажмик", "омар", "исма", "расул", "ислам"]
vote_stats = {name: 0 for name in names}

# =========================
#       BOT COMMANDS
# =========================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("бот четко. /help для списка команд.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "/random — перемешать имена\n"
        "/vote — создать голосование\n"
        "/addname <имя> — добавить имя\n"
        "/removename <имя> — удалить имя\n"
        "/listnames — список имен\n"
        "/leaderboard — топ по голосам\n"
        "/stats — общая статистика"
    )

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    shuffled = names.copy()
    random.shuffle(shuffled)
    text = "\n".join([f"{i+1}. {name}" for i, name in enumerate(shuffled)])
    await message.answer("🎲:\n\n" + text)

@dp.message(Command("vote"))
async def cmd_vote(message: types.Message):
    await message.answer_poll(
        question="ВУШ",
        options=names,
        is_anonymous=False
    )

@dp.message(Command("addname"))
async def cmd_addname(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("используй: /addname <имя>")
        return
    name = parts[1].strip()
    if name in names:
        await message.answer("уже есть такое имя")
        return
    names.append(name)
    vote_stats[name] = 0
    await message.answer(f"имя '{name}' добавлено")

@dp.message(Command("removename"))
async def cmd_removename(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("используй: /removename <имя>")
        return
    name = parts[1].strip()
    if name not in names:
        await message.answer("такого имени нет")
        return
    names.remove(name)
    vote_stats.pop(name, None)
    await message.answer(f"имя '{name}' удалено")

@dp.message(Command("listnames"))
async def cmd_list(message: types.Message):
    text = "\n".join(f"- {n}" for n in names)
    await message.answer("текущий список имен:\n\n" + text)

@dp.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message):
    if not vote_stats:
        await message.answer("статистика пуста")
        return
    sorted_stats = sorted(vote_stats.items(), key=lambda x: -x[1])
    text = "\n".join([f"{i+1}. {name} — {count}" for i, (name, count) in enumerate(sorted_stats)])
    await message.answer("🏆 лидеры:\n\n" + text)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    total_votes = sum(vote_stats.values())
    text = "\n".join([f"{name}: {count}" for name, count in vote_stats.items()])
    await message.answer(f"📊 общая статистика (всего голосов: {total_votes}):\n\n" + text)

# =========================
#        KEEP-ALIVE
# =========================
keep_alive()  # запуск веб-сервера для UptimeRobot

# =========================
#        RUN BOT
# =========================
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
