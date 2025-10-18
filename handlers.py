from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from database.db import SessionLocal
from database.models import User, MessageLog

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    """
        Стартовая команда
    """

    session = SessionLocal()

    tg_id = message.from_user.id
    user = session.query(User).filter(User.telegram_id == tg_id).first()

    if not user:
        user = User(
            telegram_id = tg_id,
            username = message.from_user.username,
            first_name = message.from_user.first_name
        )
        session.add(user)
        session.commit()

        await message.answer("👤 Регистрация успешна.")

    else:
        await message.answer("✅ Вы уже зарегистрированы")

    session.close()

@router.message(Command('bio'))
async def bio(message: types.Message):
    session = SessionLocal()

    tg_id = message.from_user.id
    user = session.query(User).filter(User.telegram_id == tg_id).first()

    if user:
        await message.answer(
            f'Ваш никнейм: {user.first_name}\n'
            f'Ваш юзернейм: {user.username}\n'
            f'Ваш ID: {user.telegram_id}\n'
            f'Дата регистрации: {user.registered_at}\n'
        )

    else:
        await message.answer("❌ Вы не зарегистрированы.")

    session.close()

@router.message(Command('history'))
async def history(message: types.Message):
    session = SessionLocal()

    tg_id = message.from_user.id
    user = session.query(User).filter(User.telegram_id == tg_id).first()

    if user:
        messages = (
                    session.query(MessageLog).
                    filter(MessageLog.user_id == user.id).
                    order_by(MessageLog.message_time.desc()).
                    limit(3).
                    all()
        )
        if messages:
            text='\n'.join([f'{msg.message_time}: {msg.text}' for msg in messages])
            await message.answer(f'Последние 3 сообщения:\n{text}')

        else:
            await message.answer("Ваша история сообщений пуста.")

    else:
        await message.answer("Вы не зарегистрированы.")

    session.close()