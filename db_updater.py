from models import Transport, TransferTasks, get_engine, create_session
from datetime import datetime

def create_new_transport(u_number, storage_id, model_id, x, y, customer, manager):
    """Создает новую машину в базе данных"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Создаем новый объект Transport
        new_transport = Transport(
            uNumber=u_number,
            storage_id=storage_id,
            model_id=model_id,
            x=x,
            y=y,
            customer=customer,
            manager=manager
        )
        session.add(new_transport)
        session.commit()
        print(f"Машина {u_number} успешно создана.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании машины: {e}")
        return 0
    finally:
        session.close()

def update_storage(u_number, new_storage):
    """Обновляет менеджера в базе данных и фиксирует изменение в tasks_transport_transfer"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Ищем машину по uNumber
        transport = session.query(Transport).filter_by(uNumber=u_number).first()
        if not transport:
            print(f"Машина с номером {u_number} не найдена.")
            return 0

        # Сохраняем старое значение
        old_storage = transport.storage_id

        # Обновляем менеджера
        transport.storage_id = new_storage

        # Добавляем задачу в TransferTasks
        transfer_task = TransferTasks(
            uNumber=u_number,
            old_manager=transport.manager,
            new_manager=transport.manager,
            old_storage=old_storage,
            new_storage=new_storage,
            old_client=transport.customer,
            new_client=transport.customer,
            date=int(datetime.now().timestamp())
        )
        session.add(transfer_task)
        session.commit()
        print(f"Менеджер для машины {u_number} успешно обновлен.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении менеджера: {e}")
        return 0
    finally:
        session.close()

def update_manager(u_number, new_manager):
    """Обновляет менеджера в базе данных и фиксирует изменение в tasks_transport_transfer"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Ищем машину по uNumber
        transport = session.query(Transport).filter_by(uNumber=u_number).first()
        if not transport:
            print(f"Машина с номером {u_number} не найдена.")
            return 0

        # Сохраняем старое значение
        old_manager = transport.manager

        # Обновляем менеджера
        transport.manager = new_manager

        # Добавляем задачу в TransferTasks
        transfer_task = TransferTasks(
            uNumber=u_number,
            old_manager=old_manager,
            new_manager=new_manager,
            old_storage=transport.storage_id,
            new_storage=transport.storage_id,
            old_client=transport.customer,
            new_client=transport.customer,
            date=int(datetime.now().timestamp())
        )
        session.add(transfer_task)
        session.commit()
        print(f"Менеджер для машины {u_number} успешно обновлен.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении менеджера: {e}")
        return 0
    finally:
        session.close()

def update_client(u_number, new_client):
    """Обновляет клиента в базе данных и фиксирует изменение в tasks_transport_transfer"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Ищем машину по uNumber
        transport = session.query(Transport).filter_by(uNumber=u_number).first()
        if not transport:
            print(f"Машина с номером {u_number} не найдена.")
            return 0

        # Сохраняем старое значение
        old_client = transport.customer

        # Обновляем клиента
        transport.customer = new_client

        # Добавляем задачу в TransferTasks
        transfer_task = TransferTasks(
            uNumber=u_number,
            old_manager=transport.manager,
            new_manager=transport.manager,
            old_storage=transport.storage_id,
            new_storage=transport.storage_id,
            old_client=old_client,
            new_client=new_client,
            date=int(datetime.now().timestamp())
        )
        session.add(transfer_task)
        session.commit()
        print(f"Клиент для машины {u_number} успешно обновлен.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении клиента: {e}")
        return 0
    finally:
        session.close()

def update_coordinates(u_number, x, y):
    """Обновляет координаты машины в базе данных и фиксирует изменение в tasks_transport_transfer"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Ищем машину по uNumber
        transport = session.query(Transport).filter_by(uNumber=u_number).first()
        if not transport:
            print(f"Машина с номером {u_number} не найдена.")
            return 0

        # Сохраняем старые координаты
        old_x = transport.x
        old_y = transport.y

        # Обновляем координаты
        transport.x = x
        transport.y = y

        # Добавляем задачу в TransferTasks
        transfer_task = TransferTasks(
            uNumber=u_number,
            old_manager=transport.manager,
            new_manager=transport.manager,
            old_storage=transport.storage_id,
            new_storage=transport.storage_id,
            old_client=transport.customer,
            new_client=transport.customer,
            date=int(datetime.now().timestamp())
        )
        session.add(transfer_task)
        session.commit()
        print(f"Координаты для машины {u_number} успешно обновлены.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении координат: {e}")
        return 0
    finally:
        session.close()
