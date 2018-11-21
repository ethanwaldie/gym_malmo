import logging
import pandas as pd

from rosalind.db.connection import ExperimentResultsDatabase
from rosalind.db.types import ExperimentStatus, ClientStatus
from rosalind.db.schema import AuthorizedUsers, Experiments, ClientPool


def get_user(experiments_connection: ExperimentResultsDatabase, user_id) -> AuthorizedUsers:
    session = experiments_connection.session_creator()

    user = (session.query(AuthorizedUsers)
            .filter(AuthorizedUsers.id == user_id).scalar())

    session.close()

    return user


def get_experiment(experiments_connection: ExperimentResultsDatabase, experiment_id) -> Experiments:
    session = experiments_connection.session_creator()

    experiment = (session.query(Experiments)
                  .filter(Experiments.id == str(experiment_id)).scalar())

    session.close()

    return experiment


def get_running_experiments_df(experiments_connection: ExperimentResultsDatabase):
    session = experiments_connection.session_creator()

    experiments_df = pd.read_sql(session.query(Experiments)
                                  .filter(Experiments.status == ExperimentStatus.RUNNING.name)
                                  .statement, session.bind)

    session.close()

    return experiments_df


def get_recent_completed_experiments_df(experiments_connection: ExperimentResultsDatabase):
    session = experiments_connection.session_creator()

    experiments_df =  pd.read_sql(session.query(Experiments)
                   .filter(Experiments.status == ExperimentStatus.COMPLETED.name)
                   .order_by(Experiments.updated_date.desc())
                   .limit(5).statement, session.bind)

    session.close()

    return experiments_df


def create_experiment(experiments_connection: ExperimentResultsDatabase,
                      experiment_id,
                      group_id,
                      model,
                      env_id,
                      owner,
                      total_timesteps,
                      log_dir,
                      model_params):
    session = experiments_connection.session_creator()

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


def update_experiment(experiments_connection: ExperimentResultsDatabase,
                      experiment_id,
                      fields: dict):
    session = experiments_connection.session_creator()

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


def find_and_reserve_client(experiments_connection: ExperimentResultsDatabase,
                            experiment_id:str) -> str:

    session = experiments_connection.session_creator()

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



def update_client(experiments_connection: ExperimentResultsDatabase,
                  client_address: str, fields: dict):
    session = experiments_connection.session_creator()

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
