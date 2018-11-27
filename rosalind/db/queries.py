import logging
import datetime
import pandas as pd

from rosalind.db.connection import RosalindDatabase
from rosalind.db.types import ExperimentStatus, ClientStatus
from rosalind.db.schema import AuthorizedUsers, Experiments, ClientPool


def get_user(rosalind_connection: RosalindDatabase, user_id) -> AuthorizedUsers:
    session = rosalind_connection.session_creator()

    user = (session.query(AuthorizedUsers)
            .filter(AuthorizedUsers.id == user_id).scalar())

    session.close()

    return user


def get_experiment(rosalind_connection: RosalindDatabase, experiment_id) -> Experiments:
    session = rosalind_connection.session_creator()

    experiment = (session.query(Experiments)
                  .filter(Experiments.id == str(experiment_id)).scalar())

    session.close()

    return experiment


def get_experiments_by_status(rosalind_connection: RosalindDatabase,
                              status: str):
    session = rosalind_connection.session_creator()

    experiments = (session.query(Experiments)
                   .filter(Experiments.status == status)
                   .order_by(Experiments.updated_date.desc()).all())

    session.close()

    return experiments

def get_experiments_by_group_id(rosalind_connection: RosalindDatabase,
                                group_id: str):
    session = rosalind_connection.session_creator()

    experiments = (session.query(Experiments)
                   .filter(Experiments.group_id == group_id)
                   .order_by(Experiments.updated_date.desc()).all())

    session.close()

    return experiments



def get_experiments_by_status_df(rosalind_connection: RosalindDatabase,
                                 status: str,
                                 limit=None):
    session = rosalind_connection.session_creator()

    if not limit:
        experiments_df = pd.read_sql(session.query(Experiments)
                                     .filter(Experiments.status == status)
                                     .order_by(Experiments.updated_date.desc())
                                     .statement, session.bind)
    else:
        experiments_df = pd.read_sql(session.query(Experiments)
                                     .filter(Experiments.status == status)
                                     .order_by(Experiments.updated_date.desc())
                                     .limit(limit).statement, session.bind)

    session.close()

    return experiments_df


def create_experiment(rosalind_connection: RosalindDatabase,
                      experiment_id,
                      group_id,
                      model,
                      env_id,
                      owner,
                      total_timesteps,
                      log_dir,
                      model_params):
    session = rosalind_connection.session_creator()

    try:
        session.add(Experiments(
            id=str(experiment_id),
            group_id=str(group_id),
            model=model,
            env_id=env_id,
            status=ExperimentStatus.PENDING.name,
            total_timesteps=total_timesteps,
            owner=owner.id,
            logs=log_dir,
            model_params=model_params))

        session.commit()


    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_experiment(rosalind_connection: RosalindDatabase,
                      experiment_id,
                      fields: dict):
    session = rosalind_connection.session_creator()

    try:
        (session.query(Experiments)
         .filter(Experiments.id == experiment_id)
         .update(fields))
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def find_and_reserve_client(rosalind_connection: RosalindDatabase,
                            experiment_id: str) -> str:
    session = rosalind_connection.session_creator()

    client_address = None
    try:
        # this prevents other proccesses from accessing this table while we claim a client.
        session.execute("LOCK client_pool in ACCESS EXCLUSIVE mode;")
        client = session.query(ClientPool).filter(ClientPool.status == ClientStatus.AVALIABLE.name).first()

        if client:
            client.status = ClientStatus.OCCUPIED.name
            client.current_experiment = experiment_id
            client_address = client.address
            session.merge(client)

        session.commit()
    except:
        client_address = None
        session.rollback()
        logging.exception("Unable to reserve Client! For experiment {}".format(experiment_id))

    finally:
        session.close()
    return client_address


def update_client(rosalind_connection: RosalindDatabase,
                  client_address: str, fields: dict):
    session = rosalind_connection.session_creator()

    try:
        (session.query(ClientPool)
         .filter(ClientPool.address == client_address)
         .update(fields))

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_client(rosalind_connection: RosalindDatabase,
                  client_address: str):
    session = rosalind_connection.session_creator()

    try:
        session.add(ClientPool(
            address=client_address,
            status=ClientStatus.AVALIABLE.name,
            start_date=datetime.datetime.utcnow()
        ))

        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
