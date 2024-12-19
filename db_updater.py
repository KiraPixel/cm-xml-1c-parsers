from models import Transport, TransferTasks, get_engine, create_session, TransportModel, Storage
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


def create_new_storage(storage_id, storage_name, storage_type, region, address, organization):
    """Создает новую машину в базе данных"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Создаем новый объект Transport
        new_storage = Storage(
            id=storage_id,
            name=storage_name,
            type=storage_type,
            region=region,
            address=address,
            organization=organization,
        )
        session.add(new_storage)
        session.commit()
        print(f"Склад {storage_id} - {storage_name} успешно создан.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании склада: {e}")
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


def update_transport(u_number, transport_model_id):
    """Обновляет модель в базе данных"""
    engine = get_engine()
    session = create_session(engine)

    try:
        # Ищем машину по uNumber
        transport = session.query(Transport).filter_by(uNumber=u_number).first()
        if not transport:
            print(f"Машина с номером {u_number} не найдена.")
            return 0

        # Проверяем есть ли такая модель
        model_check = session.query(TransportModel).filter_by(id=transport_model_id).first()
        if model_check:
            # Обновляем модель
            transport.model_id = transport_model_id
            print(f"Модель ТС для машины {u_number} успешно обновлен.")
            session.commit()
            return 1
        else:
            # Модели нет
            print(f"Ошибка при обновлении модели тс {u_number} - {transport_model_id}")
            session.commit()
            return 0
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении модели тс: {e}")
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

        # Обновляем координаты
        transport.x = x
        transport.y = y
        session.commit()
        print(f"Координаты для машины {u_number} успешно обновлены.")
        return 1
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении координат: {e}")
        return 0
    finally:
        session.close()
