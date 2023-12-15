from aiogram import executor
from create_bot import dp

if __name__ == '__main__':
    from handlers import client, other, admin, FSM
    from handlers.admin import message_admins

    client.registers_handlers_clients(dp)
    FSM.registers_handlers_fsm(dp)
    admin.registers_handlers_admin(dp)
    other.registers_handlers_other(dp)

    executor.start_polling(dp, on_startup=message_admins, skip_updates=True)
